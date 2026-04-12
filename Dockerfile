FROM python:3.10-slim

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency file first (cache layer)
COPY pyproject.toml README.md ./

# Install Python deps
RUN pip install --no-cache-dir .

# Copy project
COPY . .

# Train model if not already present
RUN python scripts/train_model.py

# HF Spaces expects port 7860
EXPOSE 7860

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
