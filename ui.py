
def chat_with_bot(user_message, history):
    url = "http://localhost:8000/chat"
    payload = {"message": user_message}

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        bot_reply = response.json().get("response", "Error: No response from bot.")
        return bot_reply
    except Exception as e:
        return f"Connection error: {e}"

# Create a chat interface
demo = gr.ChatInterface(
    fn=chat_with_bot, 
    title="Banking Chatbot",
    description="Ask me about your account, balance, or transactions!"
)

if __name__ == "__main__":
    demo.launch()
