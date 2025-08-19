# Quick Deploy Instructions

## 1. Push to GitHub
```bash
# In the youtube-transcript-api directory
git remote add origin https://github.com/YOUR_USERNAME/youtube-transcript-api.git
git branch -M main
git push -u origin main
```

## 2. Deploy on Render.com

1. Go to [render.com](https://render.com)
2. Sign up with GitHub (free)
3. Click **"New +"** → **"Web Service"**
4. Connect your GitHub account
5. Select **youtube-transcript-api** repository
6. Use these settings:
   - **Name**: youtube-transcript-api
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
7. Click **"Create Web Service"**

## 3. Get Your URL
After deployment (takes 2-3 minutes), you'll get:
```
https://youtube-transcript-api.onrender.com
```

## 4. Add to Railway Environment

1. Go to Railway dashboard
2. Click on your project
3. Go to Variables tab
4. Add:
```
TRANSCRIPT_API_URL=https://youtube-transcript-api.onrender.com
```
5. Railway will auto-redeploy

## 5. Test
Try processing a transcript again - it should work!

## Test Your Service
Once deployed, test it:
```bash
curl https://youtube-transcript-api.onrender.com/health
curl https://youtube-transcript-api.onrender.com/transcript/9qlM1n6bqZU
```