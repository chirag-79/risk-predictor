# Quick Deployment Guide

Get your CLPP Risk Prediction System live in 15 minutes!

## Prerequisites

- GitHub account (https://github.com)
- Render account (https://render.com) - Free
- Vercel account (https://vercel.com) - Free

## 🚀 Quick Start (15 minutes)

### Step 1: Push to GitHub (2 min)

```bash
cd /path/to/Risk\ Predictor
git remote add origin https://github.com/YOUR_USERNAME/risk-predictor.git
git branch -M main
git push -u origin main
```

**OR** if already connected, just push:
```bash
git push origin main
```

### Step 2: Deploy Backend to Render (6 min)

1. Go to https://render.com
2. Sign up with GitHub account
3. Click "New +" → Select "Web Service"
4. Choose your GitHub repository
5. Configure:
   - **Name**: `clpp-risk-api`
   - **Runtime**: Python 3
   - **Region**: Pick closest to you
   - **Build Command**: 
     ```
     pip install -r backend/requirements.txt && python backend/model.py
     ```
   - **Start Command**: 
     ```
     uvicorn backend.app:app --host 0.0.0.0 --port $PORT
     ```

6. **Add Environment Variables**:
   ```
   ENVIRONMENT = production
   DEBUG = False
   CORS_ORIGINS = https://your-vercel-app.vercel.app
   ```
   (Update with your actual Vercel URL after step 4)

7. Click "Create Web Service"
8. Wait for deployment (2-3 minutes)
9. **📌 Copy your API URL** (e.g., `https://clpp-risk-api.onrender.com`)

### Step 3: Deploy Frontend to Vercel (5 min)

1. Go to https://vercel.com
2. Sign up with GitHub account
3. Click "Add New" → "Project"
4. Select your GitHub repository
5. Configure:
   - **Root Directory**: `frontend`
   - **Framework**: Vite
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

6. **Add Environment Variables**:
   ```
   VITE_API_URL = https://your-render-api.onrender.com
   ```
   (Use the URL copied from Step 2)

7. Click "Deploy"
8. Wait for deployment (1-2 minutes)
9. **Your app is live!** 🎉

### Step 4: Update Backend CORS (2 min)

1. Back in Render dashboard
2. Find your `clpp-risk-api` service
3. Go to "Settings" → "Environment"
4. Update `CORS_ORIGINS`:
   ```
   https://your-vercel-app.vercel.app
   ```
5. Click "Save"
6. Service redeploys automatically

---

## ✅ Verify It Works

### Test Backend
```bash
curl https://your-render-api.onrender.com/health
```

Should return:
```json
{"status":"healthy","model_loaded":true}
```

### Test Frontend
Open your Vercel URL in browser:
```
https://your-app.vercel.app
```

Should see the CLPP Risk Prediction dashboard!

### Test Prediction
In the browser, fill the form with:
- Hamstring Tightness: 45
- Lumbar Lordosis: 60
- Hip Flexibility: 55
- Foot Posture: 50
- Psychological Stress: 7
- Physical Activity: 400
- Core Performance: 2

Click "Predict Risk" → Should show HIGH RISK ✅

---

## 🎯 You're Done!

Your production system is now live:

- **Frontend**: https://your-app.vercel.app
- **API**: https://your-render-api.onrender.com/docs (API docs)

Both services auto-deploy whenever you push to GitHub!

---

## 📝 Future Updates

To update your app:

```bash
# Make changes locally
git add .
git commit -m "Your update message"
git push origin main

# Both Render and Vercel auto-deploy!
```

---

## 🆘 Troubleshooting

### "Build failed" on Render
- Check logs in Render dashboard
- Ensure `runtime.txt` has Python version
- Verify `requirements.txt` exists

### "Can't connect to API" on frontend
- Check `VITE_API_URL` in Vercel environment
- Ensure `CORS_ORIGINS` is set in Render environment
- Wait ~2 min for services to fully start

### "Module not found" error
- Check all imports are correct
- Verify dependencies in `requirements.txt`
- Run `npm install` locally

---

## 💡 Tips

- **Render cold starts**: First request takes 2-3 seconds. Upgrade for faster performance.
- **Custom domain**: Add in Vercel dashboard under "Domains"
- **Monitor uptime**: Render dashboard shows service status
- **View logs**: Click service → "Logs" tab to debug issues

---

**Estimated total time**: 15-20 minutes ⏱️

**Difficulty**: Beginner-Friendly 🟢

**Cost**: Totally Free! 💰
