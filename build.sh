#!/usr/bin/env bash
# exit on error
set -o errexit

# Install system dependencies (ffmpeg for pydub)
apt-get update
apt-get install -y ffmpeg

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt
