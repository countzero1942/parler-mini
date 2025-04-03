# Parler Mini TTS Voice Generator

A Python application for generating text-to-speech audio using the Parler TTS Mini model with various voice profiles.

## Features

- Generate speech with a specific voice by name or index
- Generate the same text with all available voices
- List all available voices with their indices
- Support for both male and female voices
- Customizable voice descriptions

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/parler-mini.git
   cd parler-mini
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```
   pip install torch parler_tts transformers soundfile
   ```

## Usage

### Generate speech with a single voice

```bash
python main.py generate "Your text here" --name "Jon" --output "output.wav"
```

or

```bash
python main.py generate "Your text here" --index 2 --male --output "output.wav"
```

### Generate speech with all voices

```bash
python main.py generate-all "Your text here" --output-dir "voices_folder"
```

### List all available voices

```bash
python main.py list
```

### CLI Options

For a full list of options:

```bash
python main.py --help
```

## Project Structure

- `main.py` - Main script with CLI interface
- `names.py` - Contains voice data and utility functions
- `rnd-voice.py` - Simple script for generating a random voice
- `all-voices.py` - Script for generating all voices

## Voice Customization

You can customize the voice description template to change the characteristics of the generated speech:

```bash
python main.py generate "Hello world" --description "speaks with a deep, resonant voice at a slow pace with clear articulation"
```

## License

MIT

## Acknowledgments

- This project uses the [Parler TTS Mini](https://huggingface.co/parler-tts/parler-tts-mini-v1) model
