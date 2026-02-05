# Deploy to Render - Step by Step Guide

## Prerequisites
- GitHub account
- Render account (sign up at https://render.com)

## Deployment Steps

### 1. Push Code to GitHub

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - AI Voice Detection API"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

### 2. Deploy on Render Dashboard

**Option A: Using render.yaml (Recommended)**

1. Go to https://dashboard.render.com
2. Click "New" → "Blueprint"
3. Connect your GitHub repository
4. Render will automatically detect `render.yaml`
5. Click "Apply" to deploy

**Option B: Manual Setup**

1. Go to https://dashboard.render.com
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: ai-voice-detection
   - **Region**: Oregon (US West)
   - **Branch**: main
   - **Root Directory**: (leave blank)
   - **Runtime**: Python 3
   - **Build Command**: `./build.sh`
   - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free

5. Add Environment Variable:
   - Key: `PYTHON_VERSION`
   - Value: `3.10.0`

6. Click "Create Web Service"

### 3. Deployment Process

- Initial deployment takes **10-15 minutes** (downloading ML models)
- Render will:
  1. Clone your repository
  2. Install system dependencies (ffmpeg)
  3. Install Python packages
  4. Download AI models (~2GB)
  5. Start the server

### 4. Your API Endpoint

After deployment, your API will be available at:
```
https://ai-voice-detection-XXXX.onrender.com/detect-voice
```

### 5. Test Your Deployment

```bash
curl -X POST "https://YOUR-APP-NAME.onrender.com/detect-voice" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: test123" \
  -d '{
    "language": "en",
    "audio_format": "mp3",
    "audio_base64": "YOUR_BASE64_AUDIO"
  }'
```

## Important Notes

### Free Tier Limitations
- **Cold starts**: Service sleeps after 15 min of inactivity
- **First request after sleep**: Takes 30-60 seconds to wake up
- **Memory**: 512 MB RAM (models use ~1.5GB, may cause issues)
- **Disk**: Limited to 1GB

### Upgrade Recommendations
For production use, upgrade to:
- **Starter Plan** ($7/month): 512 MB RAM, no cold starts
- **Standard Plan** ($25/month): 2 GB RAM (recommended for ML models)

### Model Loading Time
- First deployment: 10-15 minutes
- Each restart: 3-5 minutes to load models into memory
- Consider using a smaller model for free tier

## Troubleshooting

### Out of Memory Error
If you get OOM errors on free tier:
1. Use smaller models
2. Reduce number of models (use only 1-2 instead of 3)
3. Upgrade to Standard plan

### Build Fails
- Check build logs in Render dashboard
- Ensure `build.sh` has execute permissions
- Verify all dependencies in requirements.txt exist

### API Returns 503
- Service is sleeping (free tier)
- Wait 30-60 seconds and retry
- Or upgrade to paid plan to avoid cold starts

## Monitoring

View logs in Render dashboard:
- Click on your service
- Go to "Logs" tab
- Monitor model loading and API requests

## Environment Variables

You can add more environment variables in Render:
- `X_API_KEY`: Change from default "test123"
- `MAX_AUDIO_SIZE`: Limit audio file size
- Any other configuration needed

## Support

- Render Documentation: https://render.com/docs
- Render Community: https://community.render.com
