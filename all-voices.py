import torch
from parler_tts import ParlerTTSForConditionalGeneration
from torch.nn import attention
from transformers import AutoTokenizer
import soundfile as sf
import names


def generate_all_voices(prompt: str, description: str, is_female: bool):

   device = "cuda:0" if torch.cuda.is_available() else "cpu"
   print(f"Using device: {device}")

   model_name = "parler-tts/parler-tts-mini-v1"
   model = ParlerTTSForConditionalGeneration.from_pretrained(model_name).to(device)
   tokenizer = AutoTokenizer.from_pretrained(model_name)

   use_names = names.females if is_female else names.males

   for i in range(len(use_names)):
      name = use_names[i]
      full_description = f"{name}'s voice " + description
      input_ids = tokenizer(full_description, return_tensors="pt").input_ids.to(device)
      prompt_input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)

      generation = model.generate(input_ids=input_ids, 
         prompt_input_ids=prompt_input_ids, attention_mask=attention.attention_mask)
      audio_arr = generation.cpu().numpy().squeeze()
      sf.write(f"{name}.wav", audio_arr, model.config.sampling_rate)
