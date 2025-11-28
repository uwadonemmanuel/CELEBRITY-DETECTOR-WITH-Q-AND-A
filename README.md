# 🌟 Celebrity Detector & Q&A Application

A modern web application that uses AI vision models to detect celebrities in images and answer questions about them. Built with Flask, OpenCV, and Groq's Llama 4 vision models.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Details](#api-details)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

- **🎯 Celebrity Detection**: Upload an image to identify celebrities using AI vision models
- **💬 Interactive Q&A**: Ask questions about detected celebrities and get AI-powered answers
- **👤 Face Detection**: Automatic face detection using OpenCV's Haar Cascade classifier
- **🔄 Model Fallback**: Automatically tries alternative models if the primary one fails
- **📱 Modern UI**: Beautiful, responsive web interface built with Tailwind CSS
- **🐳 Docker Support**: Containerized application for easy deployment
- **☸️ Kubernetes Ready**: Includes Kubernetes deployment configurations
- **🔄 CI/CD**: CircleCI integration for automated deployments

## 🛠 Tech Stack

### Backend
- **Flask**: Web framework
- **OpenCV**: Image processing and face detection
- **NumPy**: Numerical operations
- **Requests**: HTTP client for API calls
- **Python-dotenv**: Environment variable management

### AI/ML
- **Groq API**: High-performance inference for vision models
- **Llama 4 Maverick**: Primary vision model for celebrity recognition
- **Llama 4 Scout**: Fallback vision model

### Frontend
- **HTML5/CSS3**: Modern web standards
- **Tailwind CSS**: Utility-first CSS framework
- **JavaScript**: Client-side interactivity

### DevOps
- **Docker**: Containerization
- **Kubernetes**: Container orchestration
- **CircleCI**: Continuous integration/deployment
- **Google Cloud Platform**: Cloud infrastructure

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.10+** (Python 3.10 recommended)
- **pip** (Python package manager)
- **Docker** (optional, for containerized deployment)
- **kubectl** (optional, for Kubernetes deployment)
- **gcloud CLI** (optional, for GCP deployment)
- **Groq API Key** ([Get one here](https://console.groq.com/))

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd CELEBRITY-DETECTOR-AND-Q-A
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install as an editable package:

```bash
pip install -e .
```

### 4. Verify Installation

```bash
python3 -m pip list
```

You should see:
- Flask
- opencv-python
- numpy
- requests
- python-dotenv

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
GROQ_API_KEY=your_groq_api_key_here
SECRET_KEY=your_secret_key_here  # Optional, for Flask sessions
```

### Get Your Groq API Key

1. Visit [Groq Console](https://console.groq.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key to your `.env` file

### Supported Groq Vision Models

The application uses the following models (with automatic fallback):

1. **Primary**: `meta-llama/llama-4-maverick-17b-128e-instruct`
   - Powerful vision model with large context window
   - Best for complex image analysis

2. **Fallback**: `meta-llama/llama-4-scout-17b-16e-instruct`
   - Lighter-weight model for faster processing
   - Used if primary model fails

> **Note**: Llama 3.2 vision models were deprecated as of April 14, 2025. The application now uses only Llama 4 models.

## 🎮 Usage

### Local Development

1. **Activate virtual environment**:
   ```bash
   source venv/bin/activate
   ```

2. **Set environment variables** (or use `.env` file):
   ```bash
   export GROQ_API_KEY=your_api_key_here
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Access the application**:
   Open your browser and navigate to `http://localhost:5000`

### Using the Application

1. **Upload an Image**:
   - Click "Choose File" and select an image containing a celebrity
   - Click "Detect Celebrity"
   - The app will detect faces and identify the celebrity

2. **Ask Questions**:
   - After detection, you'll see celebrity information
   - Enter a question in the text field
   - Click "Ask" to get AI-powered answers

### Example Questions

- "What movies has this person starred in?"
- "What is their net worth?"
- "Tell me about their early life"
- "What awards have they won?"

## 📁 Project Structure

```
CELEBRITY-DETECTOR-AND-Q-A/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── routes.py            # Application routes
│   └── utils/
│       ├── celebrity_detector.py  # Groq API integration for vision
│       ├── image_handler.py       # OpenCV face detection
│       └── qa_engine.py          # Groq API for Q&A
├── templates/
│   └── index.html           # Main UI template
├── static/
│   └── style.css           # Additional styles
├── app.py                   # Application entry point
├── requirements.txt         # Python dependencies
├── setup.py                 # Package configuration
├── Dockerfile              # Docker image definition
├── kubernetes-deployment.yaml  # K8s deployment config
└── README.md               # This file
```

## 🔌 API Details

### Celebrity Detection API

**Endpoint**: `POST /`

**Request**: Multipart form data with image file

**Response**: 
- Celebrity information in structured format
- Detected face with bounding box
- Celebrity name extracted from response

**Models Used**:
- Primary: `meta-llama/llama-4-maverick-17b-128e-instruct`
- Fallback: `meta-llama/llama-4-scout-17b-16e-instruct`

### Q&A API

**Endpoint**: `POST /` (with question form data)

**Request**: 
- `player_name`: Celebrity name
- `question`: User's question

**Response**: AI-generated answer about the celebrity

**Model Used**: `llama-3.1-8b-instant` (text generation)

## 🐳 Docker Deployment

### Build Docker Image

```bash
docker build -t celebrity-detector:latest .
```

### Run Container

```bash
docker run -p 5000:5000 \
  -e GROQ_API_KEY=your_api_key_here \
  celebrity-detector:latest
```

### Docker Compose (Optional)

Create a `docker-compose.yml`:

```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}
    volumes:
      - .:/app
```

Run with:
```bash
docker-compose up
```

## ☸️ Kubernetes Deployment

### Prerequisites

- GKE cluster created
- `kubectl` configured
- Docker image pushed to container registry

### Deploy to Kubernetes

1. **Create Kubernetes secret**:
   ```bash
   kubectl create secret generic llmops-secrets \
     --from-literal=GROQ_API_KEY="your_groq_api_key"
   ```

2. **Apply deployment**:
   ```bash
   kubectl apply -f kubernetes-deployment.yaml
   ```

3. **Check deployment status**:
   ```bash
   kubectl get deployments
   kubectl get services
   ```

4. **Access the application**:
   ```bash
   kubectl get service llmops-service
   ```
   Use the external IP from the LoadBalancer service.

### Update Deployment

```bash
kubectl set image deployment/llmops-app \
  llmops-app=your-registry/llmops-app:new-tag
```

## 🔄 CI/CD with CircleCI

The project includes CircleCI configuration for automated deployments.

### Setup CircleCI

1. **Connect repository** to CircleCI
2. **Set environment variables** in CircleCI project settings:
   - `GCLOUD_SERVICE_KEY`: Base64-encoded GCP service account key
   - `GOOGLE_PROJECT_ID`: Your GCP project ID
   - `GKE_CLUSTER`: Your GKE cluster name
   - `GOOGLE_COMPUTE_REGION`: Compute region (e.g., `us-central1`)

3. **Pipeline automatically runs** on every push to the repository

### Manual Pipeline Trigger

You can manually trigger pipelines from the CircleCI dashboard.

## 🐛 Troubleshooting

### Common Issues

#### 1. "GROQ_API_KEY is not configured"

**Solution**: 
- Ensure `.env` file exists in project root
- Verify `GROQ_API_KEY` is set correctly
- For production, check Kubernetes secrets

#### 2. "Model decommissioned" Error

**Solution**: 
- The application automatically tries fallback models
- Check [Groq's model documentation](https://console.groq.com/docs/models) for latest models
- Update `models_to_try` list in `celebrity_detector.py` if needed

#### 3. "No face detected"

**Solution**:
- Ensure image contains a clear face
- Try a different image with better lighting
- Check image format (JPEG, PNG supported)

#### 4. OpenCV Installation Issues

**Solution**:
```bash
pip install --upgrade opencv-python
# Or on Linux:
sudo apt-get install libgl1-mesa-glx libglib2.0-0
```

#### 5. Port Already in Use

**Solution**:
```bash
# Find process using port 5000
lsof -i :5000
# Kill the process or change port in app.py
```

### Debug Mode

Enable Flask debug mode for development:

```python
# In app.py
app.run(host="0.0.0.0", port=5000, debug=True)
```

### Logging

The application includes comprehensive logging. Check logs for:
- Model selection and fallback
- API request/response details
- Error messages with context

## 🔒 Security Considerations

1. **API Keys**: Never commit API keys to version control
2. **Environment Variables**: Use `.env` file (add to `.gitignore`)
3. **Secrets Management**: Use Kubernetes secrets for production
4. **HTTPS**: Always use HTTPS in production
5. **Input Validation**: Validate uploaded images (size, format)

## 📊 Performance Tips

1. **Image Size**: Resize large images before processing
2. **Caching**: Consider caching celebrity detection results
3. **Model Selection**: Use Scout model for faster responses if accuracy allows
4. **Connection Pooling**: Reuse HTTP connections for API calls

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Add docstrings to functions
- Include error handling
- Update tests if applicable
- Update README for new features

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Groq** for providing high-performance AI inference
- **OpenCV** for computer vision capabilities
- **Flask** community for the excellent web framework
- **Tailwind CSS** for the beautiful UI components

## 📞 Support

For issues, questions, or contributions:

- Open an issue on GitHub
- Check existing documentation
- Review Groq API documentation: https://console.groq.com/docs

## 🔗 Useful Links

- [Groq Console](https://console.groq.com/)
- [Groq API Documentation](https://console.groq.com/docs)
- [Groq Model List](https://console.groq.com/docs/models)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [OpenCV Documentation](https://docs.opencv.org/)

---

**Made with ❤️ for AI-powered celebrity recognition**

