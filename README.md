# Banking AI Chatbot — HuggingFace + FastAPI + Docker

A production-ready conversational AI chatbot built using **HuggingFace Transformers**, **FastAPI**, and **Docker**. This project demonstrates end-to-end AI application development — from model deployment to API containerization.

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers-yellow.svg)](https://huggingface.co/)

---

## 🚀 What This Project Does

This chatbot uses **Microsoft's DialoGPT-medium** model (a conversational AI trained on Reddit conversations) to provide intelligent responses. The entire system runs in a Docker container and exposes a REST API, making it production-ready and easy to deploy.

**Key Features:**
- 💬 Multi-turn conversations with memory per session
- 🔄 Session management (track different users/conversations)
- 🐳 Fully containerized with Docker
- 📡 REST API built with FastAPI
- 🎯 Interactive API documentation (auto-generated Swagger UI)
- 🧠 Uses HuggingFace Transformers for model inference
- ⚡ Fast response times (~2-3 seconds on CPU)

---

## 📁 Project Structure

```
banking-chatbot/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI server and endpoints
│   └── model_handler.py     # HuggingFace model loading and inference
├── models/                  # Downloaded models stored here (not in git)
│   └── dialogpt-medium/     # Created after running download_model.py
├── download_model.py        # One-time script to download the model
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker image configuration
├── docker-compose.yml       # Easy container orchestration
├── .dockerignore           # Keep Docker image lean
├── .gitignore              # Don't push models or venv to GitHub
└── README.md               # You're reading it!
```

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **AI Model** | HuggingFace Transformers (DialoGPT-medium) | Conversational AI engine |
| **Deep Learning** | PyTorch 2.3.0 | Model inference runtime |
| **Web Framework** | FastAPI 0.111.0 | REST API endpoints |
| **Server** | Uvicorn | ASGI server for FastAPI |
| **Containerization** | Docker + Docker Compose | Isolated, reproducible environment |
| **Data Validation** | Pydantic | Request/response schema validation |

---

## ⚙️ Installation & Setup

### Prerequisites

Before starting, make sure you have:
- **Python 3.10+** installed
- **Docker Desktop** installed and running
- **Git** installed
- At least **2GB of free disk space** (for the model)

### Step 1: Clone the Repository

```bash
git clone https://github.com/AHTISHAM327/banking-ai-chatbot.git
cd banking-ai-chatbot
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Download the AI Model

This downloads ~350MB from HuggingFace and saves it locally:

```bash
python download_model.py
```

You should see:
```
Downloading microsoft/DialoGPT-medium from HuggingFace...
Done! Model saved to: ./models/dialogpt-medium
```

---

## 🐳 Running with Docker (Recommended)

### Build and Run

```bash
# Build the Docker image and start the container
docker-compose up --build

# Or run in detached mode (background)
docker-compose up --build -d
```

The API will be available at **http://localhost:8000**

### Stop the Container

```bash
docker-compose down
```

---

## 🖥️ Running Locally (Without Docker)

If you prefer to run without Docker:

```bash
# Make sure venv is activated and dependencies are installed
uvicorn app.main:app --reload --port 8000
```

The API will be available at **http://localhost:8000**

---

## 📡 API Endpoints

### 1. **Health Check**
```bash
GET /health
```

**Response:**
```json
{
  "status": "healthy"
}
```

---

### 2. **Chat with the Bot**
```bash
POST /chat
Content-Type: application/json

{
  "message": "Hello, I need help with my bank account",
  "session_id": "user123",
  "reset_history": false
}
```

**Response:**
```json
{
  "response": "Hi! I'd be happy to help. What would you like to know about your account?",
  "session_id": "user123"
}
```

**Parameters:**
- `message` (required): The user's message
- `session_id` (optional): Unique ID to track conversation history (default: "default")
- `reset_history` (optional): Set to `true` to start a fresh conversation (default: false)

---

### 3. **Clear Session History**
```bash
DELETE /chat/{session_id}
```

Clears conversation memory for a specific session.

---

## 🧪 Testing the API

### Method 1: Interactive Swagger UI (Easiest)

Open in your browser:
```
http://localhost:8000/docs
```

Click on any endpoint → **Try it out** → Fill in the JSON → **Execute**

### Method 2: cURL (Terminal)

```bash
# Send a message
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is a savings account?", "session_id": "user1"}'

# Check health
curl http://localhost:8000/health
```

### Method 3: Python Script

```python
import requests

BASE_URL = "http://localhost:8000"

response = requests.post(
    f"{BASE_URL}/chat",
    json={"message": "Hello!", "session_id": "test"}
)

print(response.json()["response"])
```

---

## 🎯 Example Conversation

```bash
User: Hi, I need help with banking services.
Bot:  Hello! I'd be happy to help. What banking service are you interested in?

User: What is the difference between savings and checking accounts?
Bot:  Great question! A savings account is designed for storing money and earning interest...

User: Thank you!
Bot:  You're welcome! Let me know if you need anything else.
```

---

## 🔧 Configuration

### Change the Model

To use a different HuggingFace model, edit `download_model.py`:

```python
MODEL_NAME = "facebook/blenderbot-400M-distill"  # Or any other model
SAVE_PATH  = "./models/blenderbot"
```

Then re-run:
```bash
python download_model.py
```

And update `MODEL_PATH` in `docker-compose.yml`:
```yaml
environment:
  - MODEL_PATH=/app/models/blenderbot
```

### Adjust Response Quality

Edit `app/model_handler.py` and modify generation parameters:

```python
output_ids = self.model.generate(
    bot_ids,
    max_length=1000,        # Longer conversations
    temperature=0.8,        # Higher = more creative (0.1–1.0)
    top_k=100,              # Limits word choices
    top_p=0.7,              # Nucleus sampling threshold
    no_repeat_ngram_size=3  # Prevents repetition
)
```

---

## 📦 Docker Image Details

- **Base Image:** `python:3.11-slim`
- **Final Size:** ~2.0 GB (without model in image)
- **Model Storage:** Mounted as volume from host machine
- **Exposed Port:** 8000

The model is **not baked into the Docker image** — it's mounted as a volume. This keeps the image small and makes model swapping easy.

---

## 🚀 Deployment Ideas

This project is production-ready and can be deployed to:

- **AWS ECS / EC2** (with Docker)
- **Google Cloud Run** (serverless containers)
- **Azure Container Instances**
- **DigitalOcean App Platform**
- **Railway / Render** (simple 1-click deploy)

For production, consider adding:
- Authentication (API keys or JWT)
- Rate limiting
- Logging and monitoring
- HTTPS/SSL certificates
- Load balancing for multiple replicas

---

## 📊 Performance

On a **standard CPU** (no GPU):
- Model loading time: ~5 seconds (once at startup)
- Response generation: ~2-3 seconds per message
- Memory usage: ~1.5 GB RAM

With a **GPU**:
- Response generation: ~0.5-1 second per message

---

## 🐛 Troubleshooting

### "uvicorn: executable file not found"
**Fix:** Change the Dockerfile CMD line to:
```dockerfile
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Model not found error
**Fix:** Make sure you ran `python download_model.py` and the `models/dialogpt-medium/` folder exists.

### Docker build is very slow
**Fix:** This is normal for the first build (installing PyTorch takes time). Subsequent builds use cached layers and are much faster.

### Port 8000 already in use
**Fix:** Change the port in `docker-compose.yml`:
```yaml
ports:
  - "8080:8000"  # Use 8080 on your PC, 8000 inside container
```

---

## 🤝 Contributing

Contributions are welcome! Here are some ideas:
- Add support for more HuggingFace models
- Build a React frontend
- Add conversation export (download chat history as JSON)
- Implement user authentication
- Add speech-to-text / text-to-speech
- Create a Telegram or Discord bot integration

---

## 📜 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙏 Acknowledgments

- [HuggingFace](https://huggingface.co/) for the Transformers library
- [FastAPI](https://fastapi.tiangolo.com/) for the amazing web framework
- [Microsoft Research](https://www.microsoft.com/en-us/research/) for DialoGPT
- Built as part of an internship application project for **Askari Bank Digital Lab**

---

## 📧 Contact

**Ahtisham Ul Hassan**  
GitHub: [@AHTISHAM327](https://github.com/AHTISHAM327)  
Email: ahtisham.nbc@gmail.com

---

**⭐ If you found this project helpful, please give it a star!**
