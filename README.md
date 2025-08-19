# YouTube Transcript API Service

A simple Python Flask service that fetches YouTube video transcripts using the `youtube-transcript-api` library.

## Endpoints

- `GET /` - Service info
- `GET /health` - Health check
- `GET /transcript/<video_id>` - Get transcript for a YouTube video

## Deployment on Render.com

This service is designed to be deployed on Render.com's free tier.

### Setup Steps:

1. Push this repository to GitHub
2. Sign up for Render.com (free)
3. Create a new Web Service
4. Connect your GitHub repository
5. Render will automatically deploy using the `render.yaml` configuration

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py
```

The service will be available at `http://localhost:5000`

## Example Usage

```bash
# Get transcript for a video
curl https://your-service.onrender.com/transcript/VIDEO_ID
```

## Response Format

```json
{
  "success": true,
  "video_id": "VIDEO_ID",
  "text": "Full transcript text...",
  "language": "en",
  "is_generated": false,
  "length": 1234,
  "segment_count": 100
}
```