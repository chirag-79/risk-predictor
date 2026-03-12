# DEPLOYMENT GUIDE - CLPP Risk Prediction System

Complete guide for deploying the CLPP Risk Prediction System to production using Render (Backend) and Vercel (Frontend).

## 📋 Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    PRODUCTION SETUP                         │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  User Browser          Vercel CDN         Render Server      │
│  (Frontend)      ←→    (React App)   ←→   (FastAPI + ML)     │
│  http://         https://              https://api.          │
│  yourdomain.com  yourapp.vercel.app   your-app.onrender.com │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   React UI   │  │  Vite Build  │  │   FastAPI    │       │
│  │   (JS/CSS)   │→ │  (Static)    │→ │   (Python)   │       │
│  │              │  │              │  │   API        │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│                                          │                   │
│                                          ↓                   │
│                                    ┌──────────────┐          │
│                                    │  ML Model    │          │
│                                    │  (Logistic   │          │
│                                    │   Regression)│          │
│                                    └──────────────┘          │
└─────────────────────────────────────────────────────────────┘
```

## 🎯 PHASE 5: Deployment Preparation

### Step 1: Build Frontend for Production

```bash
cd frontend
npm run build
```

This creates an optimized `dist/` folder with:
- Minified JavaScript
- Optimized CSS
- HTML files
- Static assets

### Step 2: Prepare Backend for Production

The backend is already production-ready. Verify:

```bash
# Requirements are in backend/requirements.txt
# venv is set up
# Model is trained (trained_model.pkl exists)
# App is configured in app.py
```

### Step 3: Create Production Environment Variables

**Frontend (.env.production):**
```ini
VITE_API_URL=https://your-backend-api.onrender.com
VITE_APP_NAME=CLPP Risk Prediction System
VITE_APP_VERSION=1.0.0
```

**Backend (.env - in repo root or Render):**
```ini
ENVIRONMENT=production
DEBUG=False
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=https://your-app.vercel.app
LOG_LEVEL=INFO
```

### Step 4: Create Additional Deployment Files

#### A. Create `Procfile` for Render (Backend)
```
web: uvicorn backend.app:app --host 0.0.0.0 --port $PORT
```

#### B. Create `build.sh` for Render (Backend)
```bash
#!/bin/bash
pip install -r backend/requirements.txt
python backend/model.py
```

#### C. Create `runtime.txt` for Python Version
```
python-3.14.2
```

---

## 🚀 PHASE 6: Deploy to Production

### **STEP A: Deploy Backend to Render**

#### 1. Create Render Account
- Go to: https://render.com
- Sign up with GitHub
- Authorize access to your repository

#### 2. Create New Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Fill in details:
   - **Name**: `clpp-risk-prediction-api`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r backend/requirements.txt && python backend/model.py`
   - **Start Command**: `uvicorn backend.app:app --host 0.0.0.0 --port $PORT`
   - **Region**: Choose closest to your users

#### 3. Set Environment Variables
In Render dashboard, add:
```
ENVIRONMENT=production
DEBUG=False
API_PORT=8000
CORS_ORIGINS=https://your-app.vercel.app
LOG_LEVEL=INFO
```

#### 4. Configure Auto-Deploy
- Enable "Auto-Deploy from Git"
- Deploys on every push to main branch

#### 5. Get API URL
After deployment, Render provides:
```
https://clpp-risk-prediction-api.onrender.com
```

**Save this URL for frontend configuration!**

---

### **STEP B: Deploy Frontend to Vercel**

#### 1. Create Vercel Account
- Go to: https://vercel.com
- Sign up with GitHub
- Authorize access to your repository

#### 2. Import Project
1. Click "Add New..." → "Project"
2. Select your GitHub repository
3. Vercel auto-detects it's a Vite project

#### 3. Configure Project
- **Framework**: Vite
- **Root Directory**: `frontend`
- **Build Command**: `npm run build`
- **Output Directory**: `dist`

#### 4. Set Environment Variables
In Vercel dashboard, add under "Environment Variables":
```
VITE_API_URL=https://clpp-risk-prediction-api.onrender.com
VITE_APP_NAME=CLPP Risk Prediction System
VITE_APP_VERSION=1.0.0
```

#### 5. Deploy
- Click "Deploy"
- Vercel builds and deploys automatically
- Your app is live at: `https://your-project.vercel.app`

#### 6. Configure Custom Domain (Optional)
In Vercel dashboard:
1. Go to "Settings" → "Domains"
2. Add your custom domain
3. Update DNS records at your domain registrar

---

## ⚙️ Post-Deployment Setup

### 1. Test Production System

**Health Check:**
```bash
curl https://your-backend-api.onrender.com/health
```

**Test Prediction:**
```bash
curl -X POST https://your-backend-api.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{
    "hamstring_tightness": 45,
    "lumbar_lordosis": 60,
    "hip_flexibility": 55,
    "foot_posture": 50,
    "psychological_stress": 7,
    "physical_activity": 400,
    "core_performance": 2
  }'
```

**Access Frontend:**
```
https://your-app.vercel.app
```

### 2. Monitor Deployments

**Render Dashboard:**
- View logs
- Monitor uptime
- Check resource usage

**Vercel Dashboard:**
- View deployments
- Check analytics
- Monitor performance

### 3. Enable Auto-Redeploy

Both Render and Vercel auto-deploy on Git push to main branch.

```bash
# To trigger deployment, just push to GitHub
git add .
git commit -m "Production update"
git push origin main
```

---

## 📊 Deployment Checklist

### Pre-Deployment
- [ ] Frontend builds without errors: `npm run build`
- [ ] Backend is trained: `trained_model.pkl` exists
- [ ] Requirements file is updated: `backend/requirements.txt`
- [ ] Environment variables are configured
- [ ] .gitignore includes `node_modules`, `venv`, `dist/__pycache__`
- [ ] All code is committed to Git

### Backend (Render)
- [ ] Render account created
- [ ] GitHub repository connected
- [ ] Web Service created
- [ ] Build command configured
- [ ] Start command configured
- [ ] Environment variables set
- [ ] Auto-deploy enabled
- [ ] API responds to health check

### Frontend (Vercel)
- [ ] Vercel account created
- [ ] GitHub repository connected
- [ ] Project imported
- [ ] Root directory set to `frontend`
- [ ] Environment variables set
- [ ] Build succeeds
- [ ] App is accessible via URL

### Post-Deployment
- [ ] Both servers are running
- [ ] Frontend connects to backend
- [ ] Form submission works
- [ ] Predictions are accurate
- [ ] Errors display correctly
- [ ] Performance is acceptable
- [ ] CORS is working

---

## 🔍 Troubleshooting Deployment

### Backend Won't Build
```
Error: python: command not found
```
**Solution**: Verify `runtime.txt` contains `python-3.14.2`

### Frontend Can't Connect to Backend
```
CORS error or connection refused
```
**Solution**: 
1. Update `VITE_API_URL` in Vercel environment variables
2. Update backend `CORS_ORIGINS` in Render environment variables

### Model Training Fails on Render
```
Error: Patient_data.csv not found
```
**Solution**: Ensure `Patient_data.csv` is in repository root, not gitignored

### Frontend Build Fails
```
Error: modules not found
```
**Solution**: Run `npm install` locally first, verify `package-lock.json` is in Git

### Slow Initial Load
**Solution**: Render free tier has cold starts. Upgrade to paid plan for production.

---

## 💰 Cost Estimate

| Service | Tier | Cost/Month | Notes |
|---------|------|-----------|-------|
| Render | Starter | Free | Cold starts, limited resources |
| Render | Standard | $7-12 | Production recommended |
| Vercel | Free | Free | Excellent for frontend |
| Vercel | Pro | $20/month | Advanced features |
| Custom Domain | - | $10-15 | Domain registrar (optional) |

**Minimal Cost Setup**: $7-12/month (Render + Vercel Free)

---

## 📈 Scaling for Production

### If You Get High Traffic

**Backend (Render):**
1. Upgrade to Standard or higher plan
2. Enable Autoscaling
3. Add more CPU/RAM resources

**Frontend (Vercel):**
1. Already scales automatically
2. Consider Pro plan for priority support
3. Add paid features if needed

### Performance Optimization

**Frontend:**
```bash
# Analyze bundle size
npm run build
# Check dist/ folder size
```

**Backend:**
```bash
# Monitor API response times
# Check logs in Render dashboard
```

---

## 🔐 Security Checklist

- [ ] DEBUG=False in production
- [ ] CORS limited to frontend domain only
- [ ] API validates all inputs
- [ ] No hardcoded secrets in code
- [ ] Use environment variables for configuration
- [ ] HTTPS enabled (automatic on Render/Vercel)
- [ ] Regular security updates for dependencies

---

## 📞 Support Resources

**Render Documentation:**
- https://render.com/docs
- Python deployment guide
- Environment variables

**Vercel Documentation:**
- https://vercel.com/docs
- Framework guides
- Environment variables

**FastAPI Production Guide:**
- https://fastapi.tiangolo.com/deployment/

---

## ✅ Deployment Complete!

Once both services are deployed:

1. **Your frontend is live at:**
   ```
   https://your-app.vercel.app
   ```

2. **Your API is live at:**
   ```
   https://your-backend-api.onrender.com
   ```

3. **Continue updates with:**
   ```bash
   git push origin main  # Triggers auto-deploy
   ```

---

**Version**: 1.0.0  
**Last Updated**: March 12, 2026  
**Status**: Ready for Deployment
