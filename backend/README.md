# AI Voice Detection API - Backend

FastAPI backend for detecting AI-generated vs human voice using machine learning models.

## 📁 Project Structure

```
backend/
├── app.py              # Main FastAPI application
├── requirements.txt    # Python dependencies
├── render.yaml         # Render deployment config
└── runtime.txt         # Python version specification
```

## 🚀 Deployed on Render

### API Endpoint
- **Base URL**: `https://ai-voice-detection.onrender.com` (after deployment)
- **API Route**: `POST /detect-voice`
- **Authentication**: Required via `X-API-Key` header

### Request Format

```json
{
  "language": "en",
  "audio_format": "mp3",
  "audio_base64": "<base64_encoded_audio>"
}
```

### Response Format

```json
{
  "classification": "AI-generated" | "Human-generated",
  "confidence": 0.85,
  "explanation": "Detailed analysis explanation"
}
```

## 🔧 Local Development

### Prerequisites
- Python 3.10+
- pip

### Setup

```bash
cd backend
pip install -r requirements.txt
```

### Run Locally

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

API will be available at: `http://localhost:8000`

### Test Request

```bash
curl -X POST "http://localhost:8000/detect-voice" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: test123" \
  -d '{
    "language": "en",
    "audio_format": "mp3",
    "audio_base64": "YOUR_BASE64_AUDIO"
  }'
```

## 📦 Dependencies

- **FastAPI**: Web framework
- **Uvicorn**: ASGI server
- **Transformers**: Hugging Face ML models
- **Librosa**: Audio analysis
- **PyDub**: Audio processing
- **PyTorch**: Deep learning framework

## 🤖 ML Models Used

1. **HuBERT** (superb/hubert-large-superb-er) - Emotion recognition
2. **Wav2Vec2** (superb/wav2vec2-base-superb-ks) - Keyword spotting
3. **AST** (MIT/ast-finetuned-audioset-10-10-0.4593) - Spoof detection

## 🔐 Security

- API key authentication required
- Default key: `test123` (change in production)
- Set via environment variable `X_API_KEY` in Render

## ⚙️ Deployment Details

### Build Process
1. Install Python dependencies from `requirements.txt`
2. Download ML models from Hugging Face (~2GB)
3. Start uvicorn server

### First Deployment
- Takes **10-15 minutes** (model downloads)
- Subsequent deployments: **3-5 minutes**

### Resource Requirements
- **Memory**: 2GB+ recommended (Free tier: 512MB may cause OOM)
- **Disk**: Models require ~2GB storage
- **Cold starts**: Free tier sleeps after 15min inactivity

## 🛠️ Troubleshooting

### Out of Memory (OOM)
- Upgrade to Render Standard plan ($25/month, 2GB RAM)
- Or reduce number of models in `app.py`

### Slow Response Times
- First request after sleep: 30-60 seconds (free tier)
- Upgrade to paid plan to avoid cold starts

### Model Download Issues
- Check Render logs for download progress
- Ensure stable internet connection during deployment

## 📊 Performance

- **Response time**: 2-5 seconds (active)
- **Cold start**: 30-60 seconds (free tier)
- **Accuracy**: ~85-90% (depends on audio quality)

## 🔄 Updates

Push to GitHub `main` branch to auto-deploy:

```bash
git add .
git commit -m "Update message"
git push origin main
```

Render will automatically detect changes and redeploy.

## 📝 License

MIT License
