from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import os

app = FastAPI()

MODEL_PATH = os.getenv("MODEL_PATH", "/app/models/dialogpt-medium")
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForCausalLM.from_pretrained(MODEL_PATH)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    inputs = tokenizer(request.message + tokenizer.eos_token, return_tensors="pt")
    reply_ids = model.generate(**inputs, max_length=100)
    reply = tokenizer.decode(reply_ids[:, inputs.input_ids.shape[-1]:][0], skip_special_tokens=True)
    return {"response": reply}