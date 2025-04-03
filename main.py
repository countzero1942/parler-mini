#!/usr/bin/env python3
import argparse
import torch
import os
import time
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer
import soundfile as sf
import names

def generate_voice(text, voice_name=None, voice_index=None, is_female=True, output_file=None, description_template=None):
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
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    
    # Load model and tokenizer
    model_name = "parler-tts/parler-tts-mini-v1"
    model = ParlerTTSForConditionalGeneration.from_pretrained(model_name).to(device)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    # Determine voice to use
    if voice_name:
        name = voice_name
    elif voice_index is not None:
        name = names.get_female(voice_index) if is_female else names.get_male(voice_index)
    else:
        # Default to first female voice
        name = names.get_female(0)
    
    # Create description
    if not description_template:
        description_template = "delivers a slightly expressive and animated speech with a moderate speed and pitch. The recording is of very high quality, with the speaker's voice sounding clear and very close up."
    
    description = f"{name}'s voice {description_template}"
    
    # Generate audio
    input_ids = tokenizer(description, return_tensors="pt").input_ids.to(device)
    prompt_input_ids = tokenizer(text, return_tensors="pt").input_ids.to(device)
    
    print(f"Generating speech with voice: {name}")
    print(f"Text: {text}")
    print(f"Description: {description}")
    
    generation = model.generate(input_ids=input_ids, prompt_input_ids=prompt_input_ids)
    audio_arr = generation.cpu().numpy().squeeze()
    
    # Save to file if specified
    if output_file:
        sf.write(output_file, audio_arr, model.config.sampling_rate)
        print(f"Audio saved to: {output_file}")
    
    return audio_arr, model.config.sampling_rate

def generate_all_voices(text, is_female=True, output_dir="voices", description_template=None):
    """
    Generate the same text with all available voices and save to files.
    
    Args:
        text (str): The text to convert to speech
        is_female (bool): Whether to use female voices (True) or male voices (False)
        output_dir (str): Directory to save the output audio files
        description_template (str, optional): Template for voice description
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Determine which voice set to use
    voices = names.females if is_female else names.males
    gender = "female" if is_female else "male"
    
    # Load model and tokenizer (only once for efficiency)
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    
    model_name = "parler-tts/parler-tts-mini-v1"
    model = ParlerTTSForConditionalGeneration.from_pretrained(model_name).to(device)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    # Generate for each voice
    for i, person in enumerate(voices):
        name = person['name']
        
        # Create description
        if not description_template:
            description_template = "delivers a slightly expressive and animated speech with a moderate speed and pitch. The recording is of very high quality, with the speaker's voice sounding clear and very close up."
        
        description = f"{name}'s voice {description_template}"
        
        # Generate audio
        input_ids = tokenizer(description, return_tensors="pt").input_ids.to(device)
        prompt_input_ids = tokenizer(text, return_tensors="pt").input_ids.to(device)
        
        print(f"Generating speech with {gender} voice [{i}]: {name}")
        
        # Measure generation time
        start_time = time.perf_counter()
        generation = model.generate(input_ids=input_ids, prompt_input_ids=prompt_input_ids)
        end_time = time.perf_counter()
        generation_time = end_time - start_time
        print(f"Generation time: {generation_time:.2f} seconds")
        
        audio_arr = generation.cpu().numpy().squeeze()
        
        # Save to file
        output_file = os.path.join(output_dir, f"{gender}_{i}_{name}.wav")
        sf.write(output_file, audio_arr, model.config.sampling_rate)
        print(f"Audio saved to: {output_file}")



def stuff():
    parser = argparse.ArgumentParser(description="Parler TTS Voice Generator")
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Single voice generation parser
    single_parser = subparsers.add_parser("generate", help="Generate speech with a single voice")
    single_parser.add_argument("text", help="Text to convert to speech")
    single_parser.add_argument("--name", help="Name of the voice to use")
    single_parser.add_argument("--index", type=int, help="Index of the voice to use")
    single_parser.add_argument("--male", action="store_true", help="Use male voice (default is female)")
    single_parser.add_argument("--output", "-o", default="output.wav", help="Output file path")
    single_parser.add_argument("--description", help="Custom voice description template")
    
    # All voices generation parser
    all_parser = subparsers.add_parser("generate-all", help="Generate speech with all voices")
    all_parser.add_argument("text", help="Text to convert to speech")
    all_parser.add_argument("--male", action="store_true", help="Use male voices (default is female)")
    all_parser.add_argument("--output-dir", "-o", default="voices", help="Output directory")
    all_parser.add_argument("--description", help="Custom voice description template")
    
    # List voices parser
    list_parser = subparsers.add_parser("list", help="List available voices")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Execute command
    if args.command == "generate":
        generate_voice(
            args.text,
            voice_name=args.name,
            voice_index=args.index,
            is_female=not args.male,
            output_file=args.output,
            description_template=args.description
        )
    elif args.command == "generate-all":
        generate_all_voices(
            args.text,
            is_female=not args.male,
            output_dir=args.output_dir,
            description_template=args.description
        )
    elif args.command == "list":
        names.print_names()
    else:
        # Default to showing help
        parser.print_help()



def main():
    prompt = f"Hey! Are you feeling freaky today? I'm feeling freakin' freaky!"
    generate_all_voices(prompt, is_female=True)

if __name__ == "__main__":
    main()
