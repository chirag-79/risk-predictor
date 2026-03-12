# CLPP Risk Prediction Frontend

React.js-based frontend application for the CLPP Risk Prediction System. Provides a user-friendly interface for healthcare professionals to input patient data and receive risk assessments.

## 🎯 Features

- **Responsive Dashboard**: Works seamlessly on desktop, tablet, and mobile
- **Patient Data Form**: 7-parameter clinical assessment form with validation
- **Real-time Validation**: Instant feedback on input errors
- **Risk Visualization**: Circular progress indicator and risk scale
- **Clinical Recommendations**: Personalized recommendations based on risk level
- **Print Reports**: Generate and print patient assessment reports
- **API Integration**: Communicates with FastAPI backend
- **Error Handling**: Graceful error messages and API status monitoring
- **Tailwind CSS**: Modern, responsive styling

## 📋 Requirements

- Node.js v24.14.0+
- npm v11.9.0+

## 🚀 Installation & Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

This installs all required packages:
- **React 18.2.0** - UI framework
- **Axios** - HTTP client for API communication
- **Lucide React** - Icons
- **Tailwind CSS** - Styling
- **Vite** - Fast build tool

### 2. Configure Environment

Edit `.env` file to set the backend API URL:

```ini
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=CLPP Risk Prediction System
VITE_APP_VERSION=1.0.0
```

For production, edit `.env.production`:
```ini
VITE_API_URL=https://your-backend-api-url.com
```

### 3. Start Development Server

```bash
npm run dev
```

The application will start at **http://localhost:5173**

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Header.jsx           # Header with branding
│   │   ├── PatientForm.jsx      # Clinical data input form
│   │   └── RiskResult.jsx       # Risk assessment results display
│   ├── services/
│   │   └── api.js               # API client and endpoints
│   ├── App.jsx                  # Main app component
│   ├── main.jsx                 # Entry point
│   └── index.css                # Global styles with Tailwind
├── index.html                   # HTML template
├── package.json                 # Dependencies
├── vite.config.js              # Vite configuration
├── tailwind.config.js          # Tailwind CSS config
├── postcss.config.js           # PostCSS config
├── .env                        # Development environment
├── .env.production             # Production environment
├── README.md                   # This file
├── public/                     # Static assets
└── dist/                       # Built files (generated)
```

## 🛠️ Development

### Run Development Server
```bash
npm run dev
```
Starts with hot-reload enabled.

### Build for Production
```bash
npm run build
```
Creates optimized production build in `dist/` folder.

### Preview Production Build
```bash
npm run preview
```
Serves the production build locally.

## 📡 API Integration

### Configuration

The frontend connects to the backend API defined in `.env`:

```javascript
// src/services/api.js
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
```

### Available Endpoints

All API calls go through `src/services/api.js`:

```javascript
import api from './services/api'

// Health check
api.checkHealth()

// Predict risk
api.predictRisk(patientData)

// Get sample prediction
api.getSamplePrediction()

// Get model info
api.getModelInfo()
```

### Request Format

**POST /predict**

```javascript
{
  "hamstring_tightness": 45,
  "lumbar_lordosis": 60,
  "hip_flexibility": 55,
  "foot_posture": 50,
  "psychological_stress": 7,
  "physical_activity": 400,
  "core_performance": 2
}
```

### Response Format

```javascript
{
  "risk_probability": 0.7823,
  "risk_percentage": 78.23,
  "risk_classification": "HIGH RISK",
  "recommendation": "Patient is at HIGH RISK for CLPP..."
}
```

## 🎨 UI Components

### Header Component
- Branding and navigation
- Logo with app title
- Tagline

### PatientForm Component
- 7 input fields for clinical parameters
- Real-time validation
- Min/max value checking
- Error messages
- Loading state
- Submit button

### RiskResult Component
- Risk classification display
- Circular progress indicator
- Risk probability visualization
- Risk scale (0-1.0)
- Clinical recommendation
- Print report button
- Reset button

## 🔧 Tailwind CSS Configuration

The app uses Tailwind CSS for styling. Key customizations in `tailwind.config.js`:

```javascript
colors: {
  primary: '#3B82F6',  // Blue
  danger: '#EF4444',   // Red
  success: '#10B981',  // Green
}
```

## 📊 Form Fields & Validation

| Field | Range | Type | Validation |
|-------|-------|------|-----------|
| Hamstring Tightness | 0-100 | Numeric | Required, must be in range |
| Lumbar Lordosis | 0-100 | Numeric | Required, must be in range |
| Hip Flexibility | 0-100 | Numeric | Required, must be in range |
| Foot Posture | 0-100 | Numeric | Required, must be in range |
| Psychological Stress | 0-10 | Numeric | Required, must be in range |
| Physical Activity | 0-10000 | Numeric | Required, must be in range |
| Core Performance | 0-10 | Numeric | Required, must be in range |

## 🔐 Security & CORS

**Development**: `.env` allows connection to `http://localhost:8000`

**Production**: Update `.env.production` with your actual backend URL.

The backend FastAPI app handles CORS configuration - frontend can modify it there if needed.

## 📱 Responsive Design

The application is fully responsive using Tailwind's breakpoints:

- **Mobile**: < 640px - Single column layout
- **Tablet**: 640px - 1024px - Optimized spacing
- **Desktop**: > 1024px - Full featured layout

## 🧪 Testing the Application

### 1. With Backend Running

```bash
# Terminal 1: Start backend
cd backend
python app.py

# Terminal 2: Start frontend
cd frontend
npm run dev
```

Then open: **http://localhost:5173**

### 2. Manual Testing Steps

1. Fill in all 7 clinical parameters
2. Click "Predict Risk" button
3. View the risk assessment result
4. Try printing the report
5. Reset and try another patient

### 3. Test Error Handling

- Leave fields empty and try to submit
- Enter values outside valid ranges
- Disconnect backend and see error message
- Retry connection after backend starts

## 🚀 Building for Production

### Build Process

```bash
npm run build
```

This creates:
- Minified JavaScript
- Optimized CSS
- Sourcemaps (optional)
- `dist/` folder ready for deployment

### Deploy to Vercel

1. Push code to GitHub
2. Connect repo to Vercel
3. Set environment variables:
   - `VITE_API_URL` = your backend URL
4. Deploy
5. Access at your Vercel URL

### Deploy to Other Platforms

**Netlify:**
```bash
# Build first
npm run build
# Deploy dist folder
```

**AWS S3 + CloudFront:**
```bash
npm run build
# Upload dist/ to S3 bucket
```

**GitHub Pages:**
```bash
npm run build
# Push dist/ to gh-pages branch
```

## 🐛 Troubleshooting

### Port 5173 Already in Use
```bash
npm run dev -- --port 5174
```

### Backend Connection Error
- Ensure backend is running: `python app.py`
- Check `VITE_API_URL` in `.env`
- Check CORS settings in backend

### Form Not Submitting
- Check browser console for errors
- Verify all fields are filled
- Ensure values are in valid ranges
- Check API response in Network tab

### Build Fails
```bash
rm -rf node_modules
npm install
npm run build
```

## 📚 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| react | 18.2.0 | UI framework |
| react-dom | 18.2.0 | React rendering |
| axios | 1.6.2 | HTTP client |
| lucide-react | 0.263.1 | Icons |
| vite | 5.0.8 | Build tool |
| tailwindcss | 3.3.6 | CSS framework |
| postcss | 8.4.32 | CSS processor |
| autoprefixer | 10.4.16 | CSS vendor prefixes |

## 🎯 Performance Optimization

- Lazy loading of components (ready for future)
- Optimized re-renders with React hooks
- CSS minification with Tailwind
- Asset optimization with Vite
- Tree-shaking of unused code

## 📄 License
[Add your license]

## 🤝 Contributing

For contributions:
1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## 📞 Support

For issues:
1. Check browser console for errors
2. Verify backend is running
3. Check `.env` configuration
4. Review backend logs

## 🔄 Next Steps (Future Enhancements)

1. **Authentication**: Add user login system
2. **Patient History**: Save and retrieve patient records
3. **Analytics Dashboard**: View population-level statistics
4. **Multi-language**: Support multiple languages
5. **Mobile App**: React Native version
6. **PDF Export**: Generate detailed PDF reports
7. **Camera Integration**: Automated measurement capture

---

**Status**: Ready for Testing ✅  
**Frontend**: Fully Functional  
**Next**: Connect with Backend & Deploy

**Version**: 1.0.0  
**Last Updated**: March 12, 2026
