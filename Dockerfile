## Parent image
FROM python:3.10-slim

## Essential environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

## Work directory inside the docker container
WORKDIR /app

## Installing system dependencies (including OpenCV requirements)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

## Copying all contents from local to /app in container
COPY . .

## Run setup.py (for editable install if using setup.py)
RUN pip install --no-cache-dir -e .

## Expose Flask port
EXPOSE 5000

## Run the app (ensure this is the correct file with app.run)
CMD ["python", "app.py"]