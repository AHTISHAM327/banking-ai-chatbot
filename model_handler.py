
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import os

# Docker will pass this as an env variable
MODEL_PATH = os.getenv("MODEL_PATH", "./models/dialogpt-medium")

# Store one session per session_id
sessions: dict = {}

class ChatModel:
    def __init__(self):
        print(f"Loading model from {MODEL_PATH} ...")
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
        self.model     = AutoModelForCausalLM.from_pretrained(MODEL_PATH)
        self.model.eval()
        print("Model ready!")

    def chat(self, user_input: str, session_id: str = "default", reset: bool = False) -> str:
        if reset or session_id not in sessions:
            sessions[session_id] = None

        # Tokenize new input
        new_ids = self.tokenizer.encode(
            user_input + self.tokenizer.eos_token,
            return_tensors="pt"
        )

        # Append to conversation history
        history = sessions[session_id]
        bot_ids = torch.cat([history, new_ids], dim=-1) if history is not None else new_ids

        # Generate response
        output_ids = self.model.generate(
            bot_ids,
            max_length=1000,
            pad_token_id=self.tokenizer.eos_token_id,
            no_repeat_ngram_size=3,
            do_sample=True,
            top_k=100,
            top_p=0.7,
            temperature=0.8
        )

        # Save history for next turn
        sessions[session_id] = output_ids

        # Decode only the new response (not the full history)
        response = self.tokenizer.decode(
            output_ids[:, bot_ids.shape[-1]:][0],
            skip_special_tokens=True
        )
        return response

# Singleton — load once, reuse forever
_model_instance = None

def get_model() -> ChatModel:
    global _model_instance
    if _model_instance is None:
        _model_instance = ChatModel()
    return _model_instance