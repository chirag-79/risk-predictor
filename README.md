# CLPP Risk Prediction System
## AI-Driven Risk Prediction for Chronic Lumbopelvic Pain in Women

### 📋 Project Description
This is a clinical-grade web application that predicts the risk of Chronic Lumbopelvic Pain (CLPP) in Indian women using a Logistic Regression Model trained on clinical data.

**Key Features:**
- Non-invasive digital screening tool
- Reduces need for expensive imaging (MRI/CT scans)
- Identifies patients at high risk for early intervention
- Responsive web interface for hospitals and clinics
- Scalable for rural and remote areas

---

### 🎯 Objectives
1. Digitize the validated prediction model from CLPP research
2. Provide zero-cost preliminary screening
3. Enable early intervention through lifestyle modifications
4. Eliminate radiation exposure in initial screening
5. Make healthcare accessible in remote areas

---

### 📊 Model Parameters (7 Clinical Features)
The model uses these independent variables to predict CLPP risk:

1. **Hamstring Tightness** - Range: 0-100
2. **Lumbar Lordosis** - Range: 0-100
3. **Hip Flexibility** - Range: 0-100
4. **Foot Posture** - Range: 0-100
5. **Psychological Stress** - Range: 0-10
6. **Physical Activity** - Range: 0-100
7. **Core Performance** - Range: 0-100

**Output:**
- Probability Score (0.0 to 1.0)
- Classification: High Risk (>0.5) or Low Risk (≤0.5)

---

### 🛠️ Tech Stack

**Backend:**
- Python 3.14.2
- FastAPI (Web framework)
- scikit-learn (ML model)
- pandas & numpy (Data processing)
- uvicorn (ASGI server)

**Frontend:**
- React.js (UI framework)
- Vite (Build tool)
- Tailwind CSS (Styling)
- Axios (API client)
- Recharts (Data visualization)

**DevOps:**
- Git (Version control)
- Node.js v24.14.0 (JavaScript runtime)
- npm 11.9.0 (Package manager)

**Deployment:**
- Render (Backend)
- Vercel (Frontend)

---

### 📁 Project Structure
```
Risk Predictor/
├── backend/                      # FastAPI application
│   ├── venv/                     # Python virtual environment
│   ├── app.py                    # Main FastAPI app
│   ├── model.py                  # Model training & inference
│   ├── requirements.txt          # Python dependencies
│   ├── .env                      # Environment variables
│   └── trained_model.pkl         # Trained ML model
│
├── frontend/                     # React.js application
│   ├── src/
│   │   ├── components/           # React components
│   │   ├── pages/                # Page components
│   │   ├── services/             # API services
│   │   └── App.jsx               # Main app component
│   ├── package.json              # Node dependencies
│   └── vite.config.js            # Vite configuration
│
├── docs/                         # Documentation
├── Patient_data.csv              # Training dataset
├── PROJECT_ROADMAP.md            # Development roadmap
├── README.md                     # This file
└── .gitignore                    # Git ignore rules
```

---

### 🚀 Getting Started

#### Prerequisites
- Git 2.53.0+ ✅
- Node.js v24.14.0+ ✅
- Python 3.14.2+ ✅
- npm 11.9.0+ ✅

#### Installation

**1. Backend Setup:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
python model.py                # Train the model
python -m uvicorn app:app --reload
```

**2. Frontend Setup:**
```bash
cd frontend
npm install
npm run dev
```

**3. Access the Application:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

### 📈 Model Training

The model is trained using:
- **Dataset:** Patient_data.csv (2,400 participants)
- **Target Variable:** LPP Group (1 = Case/High Risk, 2 = Control/Low Risk)
- **Algorithm:** Logistic Regression
- **Features:** 7 clinical parameters
- **Train-Test Split:** 80% training, 20% testing

---

### 🔄 API Endpoints

**POST /predict**
- **Description:** Get CLPP risk prediction
- **Request Body:**
```json
{
  "hamstring_tightness": 45,
  "lumbar_lordosis": 60,
  "hip_flexibility": 55,
  "foot_posture": 50,
  "psychological_stress": 7,
  "physical_activity": 40,
  "core_performance": 65
}
```
- **Response:**
```json
{
  "risk_probability": 0.78,
  "risk_classification": "HIGH RISK",
  "recommendation": "Schedule consultation with clinician"
}
```

**GET /health**
- **Description:** API health check
- **Response:** `{"status": "ok"}`

---

### 🎨 Frontend Features

1. **Patient Entry Form**
   - Input 7 clinical parameters
   - Form validation
   - Real-time feedback

2. **Risk Results Dashboard**
   - Probability percentage
   - Risk classification (High/Low)
   - Visual color indicators
   - Recommendations

3. **Responsive Design**
   - Works on desktop, tablet, mobile
   - Accessible for healthcare professionals

---

### 📊 Future Enhancements

1. **Computer Vision Integration**
   - MediaPipe/OpenCV for automated measurements
   - Camera-based Lumbar Lordosis measurement
   - Foot Posture analysis via smartphone camera

2. **Data Management**
   - Patient database
   - Medical history tracking
   - Appointment scheduling

3. **Advanced Analytics**
   - Doctor dashboard with patient insights
   - Population health analytics
   - Report generation (PDF)

4. **Expansion**
   - Mobile app (React Native)
   - Multi-language support
   - Integration with hospital systems

---

### 📝 Dataset

**File:** Patient_data.csv
- **Records:** 2,400 patients
- **Columns:** 7 clinical parameters + target variable
- **Target:** LPP Group (1 = Case, 2 = Control)

---

### 🔐 Privacy & Compliance

- All patient data processed locally
- No personal information storage (MVP version)
- Can be extended with DICOM compliance
- HIPAA-ready architecture

---

### 📞 Support

For questions or issues:
1. Check Project Roadmap: [PROJECT_ROADMAP.md](PROJECT_ROADMAP.md)
2. Review API documentation: `/docs` endpoint
3. Contact development team

---

### 📄 License
[Add your license here]

---

### 👥 Team
- **Clinical Advisor:** [Name]
- **Lead Developer:** [Name]
- **UI/UX Designer:** [Name]

---

---

## 🚀 Deployment Status

**✅ FULLY PRODUCTION READY!**

### Phase Status
- **PHASE 1**: ✅ Complete (Environment Setup)
- **PHASE 2**: ✅ Complete (Backend API + ML Model)
- **PHASE 3**: ✅ Complete (Frontend UI)
- **PHASE 4**: ✅ Complete (Testing & Verification)
- **PHASE 5**: ✅ Complete (Production Build)
- **PHASE 6**: ✅ Complete (Deployment Configuration)

### 🎯 Ready to Deploy

**Quick Start Deployment (15 minutes):**
→ See [QUICK_DEPLOY.md](QUICK_DEPLOY.md)

**Detailed Deployment Guide:**
→ See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

**Pre-Deployment Checklist:**
→ See [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)

### Current Build Status
- **Backend**: Ready for Render
- **Frontend**: Built & Optimized (dist/ folder)
- **Model**: Trained & Serialized
- **Documentation**: Complete

### Deployment Options

**Recommended Setup** (Free):
- Backend: Render (https://render.com)
- Frontend: Vercel (https://vercel.com)
- Estimated setup time: 15 minutes

**Alternative Options**:
- Railway, Netlify, AWS, Azure, Google Cloud
- See DEPLOYMENT_GUIDE.md for detailed options

### Next Steps to Go Live

1. **Push to GitHub**: `git push origin main`
2. **Deploy Backend**: Create Web Service on Render
3. **Deploy Frontend**: Import project on Vercel
4. **Configure API URL**: Update environment variables
5. **Test Live App**: Verify predictions work
6. **Celebrate**: Your app is live! 🎉

---

**Version:** 1.0.0  
**Last Updated:** March 12, 2026  
**Status:** ✅ Production Ready - Ready for Deployment
