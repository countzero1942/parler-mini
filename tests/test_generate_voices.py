#!/usr/bin/env python3
import pytest
import os
import numpy as np
from unittest.mock import patch, MagicMock
from names import Sex, people
import generate_voices


@pytest.fixture
def mock_tts_components():
	"""Create mocks for the TTS components."""
	model = MagicMock()
	model.config.sampling_rate = 24000

	# Create a simple numpy array for testing
	audio_array = np.zeros(24000)

	# Setup the mock to return the array directly
	model.generate.return_value = MagicMock()
	model.generate.return_value.cpu.return_value = MagicMock()
	model.generate.return_value.cpu.return_value.numpy.return_value = MagicMock()
	model.generate.return_value.cpu.return_value.numpy.return_value.squeeze.return_value = audio_array
	
	tokenizer = MagicMock()
	tokenizer.return_value = MagicMock()
	tokenizer.return_value.input_ids = MagicMock()
	
	return model, tokenizer


def test_voice_selection_by_sex():
	"""Test that the correct voices are selected based on sex."""
	# Get the list of voice names for each sex
	male_voices = people.getNamesBySex(Sex.Male)
	female_voices = people.getNamesBySex(Sex.Female)
	all_voices = people.getNamesBySex(Sex.Either)

	# Verify we have the expected voices
	assert len(male_voices) > 0, 'No male voices found'
	assert len(female_voices) > 0, 'No female voices found'
	assert len(all_voices) > 0, 'No voices found'

	# Verify that male and female voices are subsets of all voices
	assert set(male_voices).issubset(set(all_voices))
	assert set(female_voices).issubset(set(all_voices))

	# Verify that male and female voices are distinct
	assert not set(male_voices).intersection(set(female_voices))


def test_person_name_in_description():
	"""Test that a person's name is included in the voice description."""
	# Get a test person
	test_person = people.males[0]
	test_text = 'Test speech'
	description_template = 'custom description template'

	# Create a mock tokenizer that we can inspect
	mock_tokenizer = MagicMock()
	mock_tokenizer.return_value = MagicMock()

	# Mock external dependencies to avoid actual TTS generation
	with patch('generate_voices.ParlerTTSForConditionalGeneration.from_pretrained'), \
		patch('generate_voices.AutoTokenizer.from_pretrained', return_value=mock_tokenizer), \
		patch('generate_voices.torch.cuda.is_available', return_value=False), \
		patch('generate_voices.sf.write'):
		
		# Call the function with a custom description template
		generate_voices.generateVoice(
			test_text, test_person, description_template, output_file=None
		)

		# Verify the description contains the person's name and template
		# The first call to the tokenizer is with the description
		description = mock_tokenizer.call_args_list[0][0][0]
		assert test_person.name in description, (
			f"Person name '{test_person.name}' not found in description: {description}"
		)
		assert description_template in description, (
			f"Template '{description_template}' not found in description: {description}"
		)


def test_output_directory_creation(tmp_path):
	"""Test that the output directory is created when generating all voices."""
	# Setup test parameters
	test_text = 'Test all voices'
	output_dir = str(tmp_path / 'test_voices')

	# Create mock objects
	mock_model = MagicMock()
	mock_model.config.sampling_rate = 24000
	mock_model.generate.return_value = MagicMock()

	mock_tokenizer = MagicMock()

	# Mock all external dependencies to avoid actual TTS generation
	with patch('generate_voices.ParlerTTSForConditionalGeneration.from_pretrained', return_value=mock_model), \
		patch('generate_voices.AutoTokenizer.from_pretrained', return_value=mock_tokenizer), \
		patch('generate_voices.sf.write'), \
		patch('generate_voices.torch.cuda.is_available', return_value=False):
		
		# Call the function with a limited set (Female only for faster test)
		generate_voices.generateAllVoices(test_text, sex=Sex.Female, output_dir=output_dir)

		# Verify the output directory was created
		assert os.path.exists(output_dir), 'Output directory was not created'
