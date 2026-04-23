
from transformers import AutoModelForCausalLM, AutoTokenizer
import os

model_name = "microsoft/DialoGPT-medium"
save_path = "./models/dialogpt-medium"

os.makedirs(save_path, exist_ok=True)
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

tokenizer.save_pretrained(save_path)
model.save_pretrained(save_path)
