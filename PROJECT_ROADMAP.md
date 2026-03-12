# CLPP Risk Prediction System - Full Stack Development Roadmap

## Project Overview
AI-Driven Risk Prediction System for Chronic Lumbopelvic Pain (CLPP) in Women using Logistic Regression Model with React Frontend and FastAPI Backend.

---

## PHASE 1: Environment & Project Setup ✅ (COMPLETED)
### Tools Verification
- [x] Git: 2.53.0 ✓
- [x] Node.js: v24.14.0 ✓
- [x] npm: 11.9.0 ✓
- [x] Python: 3.14.2 ✓

### Tasks:
- [x] Verify all development tools
- [ ] Initialize Git repository
- [ ] Create project folder structure
- [ ] Set up .gitignore

---

## PHASE 2: Backend Setup (Python/FastAPI)
### Objective: Create the AI inference engine

**Tasks:**
1. Create Python virtual environment
2. Install dependencies:
   - FastAPI
   - scikit-learn (for model training)
   - pandas & numpy (data processing)
   - python-multipart
   - uvicorn (ASGI server)
   - joblib (model serialization)
3. Create project structure:
   ```
   backend/
   ├── venv/
   ├── app.py (main FastAPI app)
   ├── model.py (ML model training)
   ├── requirements.txt
   ├── .env (environment variables)
   └── trained_model.pkl
   ```
4. Load and explore Patient_data.csv
5. Train Logistic Regression Model
6. Create prediction endpoint

---

## PHASE 3: Frontend Setup (React.js)
### Objective: Create responsive UI dashboard

**Tasks:**
1. Initialize React project with Vite/Create React App
2. Install dependencies:
   - React Router (navigation)
   - Axios (API calls)
   - Tailwind CSS / Material-UI (styling)
   - Chart.js / Recharts (data visualization)
3. Create folder structure:
   ```
   frontend/
   ├── src/
   │   ├── components/
   │   │   ├── PatientForm.jsx
   │   │   ├── RiskResult.jsx
   │   │   ├── Dashboard.jsx
   │   │   └── Header.jsx
   │   ├── pages/
   │   │   ├── Home.jsx
   │   │   ├── PatientEntry.jsx
   │   │   └── Results.jsx
   │   ├── services/
   │   │   └── api.js
   │   ├── App.jsx
   │   └── index.css
   ├── public/
   ├── package.json
   └── vite.config.js
   ```
4. Build responsive form for 7 parameters:
   - Hamstring Tightness
   - Lumbar Lordosis
   - Hip Flexibility
   - Foot Posture
   - Psychological Stress
   - Physical Activity
   - Core Performance

---

## PHASE 4: Model Training & API Integration
### Objective: Train ML model and create endpoints

**Backend Tasks:**
1. Data Preprocessing:
   - Load Patient_data.csv
   - Handle missing values
   - Normalize/scale features
   - Split train-test data (80-20)
   
2. Train Logistic Regression Model:
   - Fit model on 7 parameters
   - Calculate accuracy metrics
   - Save model as .pkl file

3. Create FastAPI Endpoints:
   ```
   POST /predict
   - Input: Patient data (7 parameters)
   - Output: Risk probability (0.0-1.0) + Classification (High/Low Risk)
   
   GET /health
   - Check API status
   ```

4. Add CORS support for frontend-backend communication

---

## PHASE 5: Frontend-Backend Integration
### Objective: Connect UI with prediction API

**Tasks:**
1. Create API service module (api.js)
2. Build PatientForm component with validation
3. Connect form submission to `/predict` endpoint
4. Display results with:
   - Risk probability percentage
   - High Risk / Low Risk classification
   - Visual indicators (color coding)
5. Add loading states & error handling

---

## PHASE 6: Testing & Validation
### Objective: Ensure accuracy and reliability

**Backend Tests:**
- Test model predictions with sample data
- Verify API responses
- Test edge cases and error handling

**Frontend Tests:**
- Form validation tests
- API integration tests
- UI responsiveness across devices

---

## PHASE 7: Deployment Preparation
### Objective: Prepare for cloud deployment

**Tasks:**
1. Create production builds
2. Set environment variables
3. Create deployment configuration files
4. Prepare database (if needed)

---

## PHASE 8: Deployment (Production)
### Option A: Vercel (Frontend) + Render (Backend)

**Backend (Render):**
1. Create Render account
2. Connect GitHub repository
3. Deploy FastAPI app
4. Set production environment variables
5. Get backend API URL

**Frontend (Vercel):**
1. Create Vercel account
2. Connect GitHub repository
3. Set API endpoint to production URL
4. Deploy React app
5. Get live website URL

### Option B: Single Deployment (Render)
- Deploy full-stack app on Render as one service

---

## TECHNICAL SPECIFICATIONS

### Model Parameters (7 Features)
1. **Hamstring Tightness** - Numeric value (0-100)
2. **Lumbar Lordosis** - Numeric value (0-100)
3. **Hip Flexibility** - Numeric value (0-100)
4. **Foot Posture** - Numeric value (0-100)
5. **Psychological Stress** - Numeric value (0-10)
6. **Physical Activity** - Numeric value (0-100)
7. **Core Performance** - Numeric value (0-100)

### Prediction Logic
- Input: 7 parameters
- Model: Logistic Regression
- Output: Probability score (0.0-1.0)
- Classification: 
  - Score > 0.5 = **HIGH RISK** (Red)
  - Score ≤ 0.5 = **LOW RISK** (Green)

---

## FUTURE ENHANCEMENTS (Post-MVP)
1. Computer Vision (MediaPipe/OpenCV) for automated measurements
2. Patient history/records database
3. Doctor dashboard with patient analytics
4. PDF report generation
5. Multi-language support
6. Mobile app (React Native)

---

## File Structure Overview
```
Risk Predictor/
├── frontend/                    # React.js app
│   ├── src/
│   ├── public/
│   └── package.json
├── backend/                     # FastAPI app
│   ├── app.py
│   ├── model.py
│   ├── requirements.txt
│   └── trained_model.pkl
├── Patient_data.csv            # Training dataset
├── PROJECT_ROADMAP.md          # This file
├── .gitignore
└── README.md
```

---

## Timeline Estimate
- Phase 1: ✅ Completed
- Phase 2: 1-2 days
- Phase 3: 2-3 days
- Phase 4: 1-2 days
- Phase 5: 1 day
- Phase 6: 1 day
- Phase 7: 1 day
- Phase 8: 1-2 days
**Total: 1-2 weeks**

---

## Next Steps
1. Initialize Git repository
2. Begin PHASE 2: Backend Setup
3. Set up Python virtual environment
4. Install required packages
