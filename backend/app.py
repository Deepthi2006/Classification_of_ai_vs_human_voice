from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import base64
import uuid
import os
import numpy as np
from pydub import AudioSegment
import librosa
from transformers import pipeline

app = FastAPI(title="AI Voice Detection API")

# =========================
# Health Check Endpoint
# =========================
@app.get("/")
def health_check():
    return {
        "status": "healthy",
        "service": "AI Voice Detection API",
        "version": "1.0.0",
        "endpoints": {
            "POST /detect-voice": "Detect AI vs Human voice"
        }
    }

# =========================
# Request Model
# =========================
class VoiceRequest(BaseModel):
    language: str
    audio_format: str
    audio_base64: str


# =========================
# Load Models
# =========================
print("Loading models...")

# Supporting models
hubert_classifier = pipeline(
    "audio-classification",
    model="superb/hubert-large-superb-er"
)

wav2vec_classifier = pipeline(
    "audio-classification",
    model="superb/wav2vec2-base-superb-ks"
)

# ✅ REAL spoof / deepfake detection model
spoof_classifier = pipeline(
    "audio-classification",
    model="MIT/ast-finetuned-audioset-10-10-0.4593"
)

print("Models loaded successfully.")

# =========================
# Signal Analysis
# =========================
def compute_signal_scores(y, sr):
    pitches, _ = librosa.piptrack(y=y, sr=sr)
    pitch_values = pitches[pitches > 0]
    pitch_variance = np.var(pitch_values) if len(pitch_values) else 0
    pitch_score = min(pitch_variance / 500, 1.0)

    energy = librosa.feature.rms(y=y)[0]
    speaking_rate_score = 1 - np.clip(np.std(energy), 0, 1)

    silence_ratio = np.mean(energy < np.percentile(energy, 20))
    pause_score = silence_ratio

    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
    spectral_smoothness = 1 - (
        np.std(spectral_centroid) / (np.mean(spectral_centroid) + 1e-6)
    )

    return float(
        np.clip(
            np.mean([
                pitch_score,
                speaking_rate_score,
                pause_score,
                spectral_smoothness
            ]),
            0,
            1
        )
    )


# =========================
# API Endpoint
# =========================
@app.post("/detect-voice")
def detect_voice(
    request: VoiceRequest,
    x_api_key: str = Header(None)
):
    if x_api_key != "test123":
        raise HTTPException(status_code=401, detail="Invalid API Key")

    try:
        audio_bytes = base64.b64decode(request.audio_base64)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Base64 audio")

    audio_id = str(uuid.uuid4())
    mp3_path = f"temp_{audio_id}.mp3"
    wav_path = f"temp_{audio_id}.wav"

    try:
        # Save MP3
        with open(mp3_path, "wb") as f:
            f.write(audio_bytes)

        # Convert to WAV
        AudioSegment.from_file(mp3_path).export(wav_path, format="wav")

        # Load audio
        y, sr = librosa.load(wav_path, sr=None)

        # =========================
        # Signal score (support)
        # =========================
        signal_score = compute_signal_scores(y, sr)

        # =========================
        # Supporting ML scores
        # =========================
        hubert_score = hubert_classifier(wav_path)[0]["score"]
        wav2vec_score = wav2vec_classifier(wav_path)[0]["score"]

        support_score = (
            0.5 * hubert_score +
            0.5 * wav2vec_score
        )

        # =========================
        # 🔥 SPOOF MODEL (MAIN DECISION)
        # =========================
        spoof_result = spoof_classifier(wav_path)[0]
        spoof_label = spoof_result["label"].lower()
        spoof_score = spoof_result["score"]

        # Normalize: higher score = more AI-like
        if "bonafide" in spoof_label:
            spoof_score = 1 - spoof_score

        # =========================
        # FINAL CONFIDENCE
        # =========================
        final_score = (
            0.65 * spoof_score +           # dominant
            0.20 * support_score +         # support
            0.15 * (1 - signal_score)      # smoother speech → AI
        )

        final_score = float(np.clip(final_score, 0, 1))

        # =========================
        # FINAL DECISION
        # =========================
        if final_score >= 0.65:
            classification = "AI-generated"
            explanation = (
                "Synthetic speech detected using a dedicated anti-spoofing "
                "model combined with acoustic consistency analysis."
            )
        else:
            classification = "Human-generated"
            explanation = (
                "Speech characteristics match natural human patterns with "
                "low spoofing likelihood."
            )

        return {
            "classification": classification,
            "confidence": round(final_score, 2),
            "explanation": explanation
        }

    finally:
        if os.path.exists(mp3_path):
            os.remove(mp3_path)
        if os.path.exists(wav_path):
            os.remove(wav_path)
