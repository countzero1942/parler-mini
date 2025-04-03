import torch
from parler_tts import ParlerTTSForConditionalGeneration
from torch.nn import attention
from transformers import AutoTokenizer
import soundfile as sf
import names

names.print_names()

device = "cuda:0" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

model_name = "parler-tts/parler-tts-mini-v1"
model = ParlerTTSForConditionalGeneration.from_pretrained(model_name).to(device)
tokenizer = AutoTokenizer.from_pretrained(model_name)



name = names.get_female(3)

prompt = f"Hey, are you feeling freaky today? I'm feeling freakin' freaky!"
description = f"{name}'s voice delivers a slightly expressive and animated speech with a moderate speed and pitch. The recording is of very high quality, with the speaker's voice sounding clear and very close up."

input_ids = tokenizer(description, return_tensors="pt").input_ids.to(device)
prompt_input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)

generation = model.generate(input_ids=input_ids, 
	prompt_input_ids=prompt_input_ids)
audio_arr = generation.cpu().numpy().squeeze()
sf.write("test.wav", audio_arr, model.config.sampling_rate)
