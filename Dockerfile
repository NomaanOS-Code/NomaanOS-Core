FROM python:3.10-slim

WORKDIR /app

# Copy repository contents
COPY . /app

ENV PYTHONUNBUFFERED=1

# Default command: Run Aegis Red-Team Stress Test
CMD ["python3", "stress_test.py"]
