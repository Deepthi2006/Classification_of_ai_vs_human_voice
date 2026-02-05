# AI Voice Detection - Render Deployment Guide

## 📋 Current Structure

```
Classification_of_ai_vs_human_voice/
├── backend/                 # Backend API (for Render deployment)
│   ├── app.py              # FastAPI application
│   ├── requirements.txt    # Python dependencies
│   ├── render.yaml         # Render configuration
│   ├── runtime.txt         # Python version
│   └── README.md           # Backend documentation
├── frontend/               # Frontend (empty - for future use)
├── .gitignore             # Git ignore rules
└── DEPLOYMENT.md          # This file
```

## 🚀 Deploy to Render - Step by Step

### Step 1: Prerequisites
✅ GitHub repository: `https://github.com/Deepthi2006/Classification_of_ai_vs_human_voice`  
✅ Render account: Sign up at https://render.com (free)

### Step 2: Deploy Using Blueprint (Recommended)

1. **Go to Render Dashboard**
   - Visit: https://dashboard.render.com
   - Sign in with GitHub

2. **Create New Blueprint**
   - Click **"New"** → **"Blueprint"**
   
3. **Connect Repository**
   - Select: `Deepthi2006/Classification_of_ai_vs_human_voice`
   - Grant Render access if prompted

4. **Configure Blueprint**
   - Render will auto-detect `backend/render.yaml`
   - **Root Directory**: `backend`
   - Click **"Apply"**

5. **Wait for Deployment**
   - Initial deployment: ~10-15 minutes (downloads ML models)
   - Watch the logs in real-time

6. **Get Your URL**
   - After deployment: `https://ai-voice-detection-XXXX.onrender.com`
   - Test health check: Visit the URL in browser

### Step 3: Alternative - Manual Web Service Setup

If Blueprint doesn't work, use manual setup:

1. **Click "New" → "Web Service"**

2. **Connect GitHub Repository**
   - Select your repo

3. **Configure Service:**
   - **Name**: `ai-voice-detection`
   - **Region**: Oregon (US West)
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: Free

4. **Environment Variables:**
   - Key: `X_API_KEY`
   - Value: `test123` (or your custom key)

5. **Click "Create Web Service"**

## ✅ Verify Deployment

### 1. Health Check
Visit your deployment URL in a browser:
```
https://your-app-name.onrender.com/
```

You should see:
```json
{
  "status": "healthy",
  "service": "AI Voice Detection API",
  "version": "1.0.0"
}
```

### 2. Test API Endpoint

```bash
curl -X POST "https://your-app-name.onrender.com/detect-voice" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: test123" \
  -d '{
    "language": "en",
    "audio_format": "mp3",
    "audio_base64": "YOUR_BASE64_AUDIO_HERE"
  }'
```

## 📊 Deployment Timeline

| Stage | Time | Description |
|-------|------|-------------|
| Clone repo | 10s | Render clones from GitHub |
| Install Python | 30s | Sets up Python 3.10 |
| Install packages | 2-3min | `pip install -r requirements.txt` |
| Download ML models | 5-10min | Hugging Face model downloads (~2GB) |
| Start server | 30s | Uvicorn starts |
| **Total** | **10-15min** | First deployment |

Subsequent deployments: **3-5 minutes** (models cached)

## ⚠️ Important Notes

### Free Tier Limitations
- **Memory**: 512MB RAM (Models need ~1.5-2GB)
- **Risk**: Out of Memory (OOM) errors possible
- **Sleep**: Service sleeps after 15 min of inactivity
- **Wake time**: 30-60 seconds for first request

### Recommended: Upgrade for Production
- **Starter**: $7/month - 512MB, no sleep
- **Standard**: $25/month - 2GB RAM ✅ **Recommended for ML models**

### Build Logs
Monitor deployment in Render dashboard:
- Click on your service
- Go to **"Logs"** tab
- Watch for:
  - ✅ "Loading models..."
  - ✅ "Models loaded successfully."
  - ✅ "Uvicorn running on..."

## 🔧 Troubleshooting

### Build Failed
**Error**: `pip install` fails
- **Fix**: Check `requirements.txt` syntax
- **Fix**: Ensure Python 3.10 in `runtime.txt`

### Out of Memory (OOM)
**Error**: Service crashes after starting
- **Fix**: Upgrade to Standard plan (2GB RAM)
- **Alternative**: Reduce models in `app.py` (use only 1 instead of 3)

### 502 Bad Gateway
**Cause**: Service is sleeping (free tier)
- **Fix**: Wait 30-60 seconds and retry
- **Prevention**: Upgrade to paid plan

### Models Not Loading
**Error**: Timeout during deployment
- **Fix**: Increase build timeout in Render settings
- **Fix**: Check Hugging Face model names are correct

## 🔄 Auto-Deploy on Push

Every push to `main` branch triggers auto-deployment:

```bash
# Make changes to backend/app.py
git add backend/app.py
git commit -m "Update API logic"
git push origin main

# Render automatically detects and redeploys
```

## 📱 API Usage

### Base URL
```
https://ai-voice-detection-XXXX.onrender.com
```

### Endpoints

#### 1. Health Check
```
GET /
```
Response:
```json
{
  "status": "healthy",
  "service": "AI Voice Detection API"
}
```

#### 2. Detect Voice
```
POST /detect-voice
Headers: X-API-Key: test123
Body: {
  "language": "en",
  "audio_format": "mp3",
  "audio_base64": "<base64_string>"
}
```

Response:
```json
{
  "classification": "AI-generated",
  "confidence": 0.85,
  "explanation": "Synthetic speech detected..."
}
```

## 📈 Monitoring

### View Logs
- Render Dashboard → Your Service → Logs
- Real-time log streaming
- Search and filter logs

### Metrics
- Request count
- Response times
- Memory usage
- Error rates

### Alerts
- Set up email notifications for:
  - Deployment failures
  - Service down
  - High error rates

## 🔐 Security

### Change API Key
In Render Dashboard:
1. Go to Environment tab
2. Edit `X_API_KEY`
3. Save changes
4. Service auto-restarts

### HTTPS
- ✅ Automatic SSL/TLS
- ✅ Free certificates from Let's Encrypt
- ✅ HTTPS enforced by default

## 📞 Support

- **Render Docs**: https://render.com/docs
- **Render Community**: https://community.render.com
- **Render Status**: https://status.render.com

## 🎉 Success Checklist

- [ ] Repository pushed to GitHub
- [ ] Render account created
- [ ] Service deployed (Blueprint or Manual)
- [ ] Health check returns 200 OK
- [ ] Test API call successful
- [ ] API key configured
- [ ] Auto-deploy working

---

**Your API is now live! 🚀**

Share your API URL with your frontend or clients!
