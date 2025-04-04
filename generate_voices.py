import torch
import os
import time
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer
import soundfile as sf
import names
from names import Sex, Person


def generateVoice(
	text: str,
	person: Person,
	description_template=None,
	output_file='output.wav',
):
	"""
	Generate speech using the Parler TTS model with a specified voice.

	Args:
	    text (str): The text to convert to speech
	    voice_name (str, optional): Name of the voice to use
	    voice_index (int, optional): Index of the voice to use (from the male/female arrays)
	    is_female (bool): Whether to use female voices (True) or male voices (False)
	    output_file (str, optional): Path to save the output audio file
	    description_template (str, optional): Template for voice description

	Returns:
	    tuple: (audio_array, sampling_rate)
	"""
	# Determine device
	device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
	print(f'Using device: {device}')

	# Load model and tokenizer
	model_name = 'parler-tts/parler-tts-mini-v1'
	model = ParlerTTSForConditionalGeneration.from_pretrained(model_name).to(
		device
	)
	tokenizer = AutoTokenizer.from_pretrained(model_name)

	# Determine voice to use
	name = person.name

	# Create description
	if not description_template:
		description_template = (
			'delivers a slightly expressive and animated speech '
			+ 'with a moderate speed and pitch. The recording is of very high quality, '
			+ "with the speaker's voice sounding clear and very close up."
		)

	description = f"{name}'s voice {description_template}"

	# Generate audio
	input_ids = tokenizer(description, return_tensors='pt').input_ids.to(device)
	prompt_input_ids = tokenizer(text, return_tensors='pt').input_ids.to(device)

	print(f'Generating speech with voice: {name}')
	print(f'Text: {text}')
	print(f'Description: {description}')

	generation = model.generate(
		input_ids=input_ids, prompt_input_ids=prompt_input_ids
	)
	audio_arr = generation.cpu().numpy().squeeze()

	# Save to file if specified
	if output_file:
		sf.write(output_file, audio_arr, model.config.sampling_rate)
		print(f'Audio saved to: {output_file}')

	return audio_arr, model.config.sampling_rate


def generateAllVoices(
	text, sex: Sex = Sex.Either, output_dir='voices', description_template=None
):
	"""
	Generate the same text with all available voices and save to files.

	Args:
	    text (str): The text to convert to speech
	    sex (Sex): The sex of the voices to use
	    output_dir (str): Directory to save the output audio files
	    description_template (str, optional): Template for voice description
	"""
	# Create output directory if it doesn't exist
	os.makedirs(output_dir, exist_ok=True)

	# Determine which voice set to use
	voices = names.people.getNamesBySex(sex)

	# Load model and tokenizer (only once for efficiency)
	device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
	print(f'Using device: {device}')

	model_name = 'parler-tts/parler-tts-mini-v1'
	model = ParlerTTSForConditionalGeneration.from_pretrained(model_name).to(
		device
	)
	tokenizer = AutoTokenizer.from_pretrained(model_name)

	# Generate for each voice
	for i, name in enumerate(voices):
		# Create description
		if not description_template:
			description_template = (
				'delivers a slightly expressive and animated speech '
				+ 'with a moderate speed and pitch. The recording is of very high quality, '
				+ "with the speaker's voice sounding clear and very close up."
			)

		description = f"{name}'s voice {description_template}"

		# Generate audio
		input_ids = tokenizer(description, return_tensors='pt').input_ids.to(
			device
		)
		prompt_input_ids = tokenizer(text, return_tensors='pt').input_ids.to(
			device
		)

		print(f'Generating speech with {sex} voice [{i}]: {name}')

		# Measure generation time
		start_time = time.perf_counter()
		generation = model.generate(
			input_ids=input_ids, prompt_input_ids=prompt_input_ids
		)
		end_time = time.perf_counter()
		generation_time = end_time - start_time
		print(f'Generation time: {generation_time:.2f} seconds')

		audio_arr = generation.cpu().numpy().squeeze()

		# Save to file
		output_file = os.path.join(output_dir, f'{sex}_{i}_{name}.wav')
		sf.write(output_file, audio_arr, model.config.sampling_rate)
		print(f'Audio saved to: {output_file}')
