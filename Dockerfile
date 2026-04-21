# Use a lightweight python image instead
FROM python:3.10-slim

WORKDIR /app

# Install CPU-only PyTorch and other dependencies
# (This is much smaller than the full PyTorch image)
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir fastapi uvicorn transformers accelerate pydantic python-multipart

COPY app/ ./app/
RUN mkdir -p /app/models

EXPOSE 8000
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
