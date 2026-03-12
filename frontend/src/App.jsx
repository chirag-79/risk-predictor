import React, { useState, useEffect } from 'react'
import { AlertCircle, Loader } from 'lucide-react'
import Header from './components/Header'
import PatientForm from './components/PatientForm'
import RiskResult from './components/RiskResult'
import api from './services/api'

function App() {
  const [result, setResult] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)
  const [apiStatus, setApiStatus] = useState('checking')

  // Check API health on component mount
  useEffect(() => {
    checkApiHealth()
  }, [])

  const checkApiHealth = async () => {
    try {
      setApiStatus('checking')
      const response = await api.checkHealth()
      if (response.data.model_loaded) {
        setApiStatus('healthy')
      } else {
        setApiStatus('model-not-loaded')
        setError('Model not loaded. Please train the model first.')
      }
    } catch (err) {
      console.error('API health check failed:', err)
      setApiStatus('error')
      setError(`Cannot connect to API. Make sure the backend is running at ${import.meta.env.VITE_API_URL || 'http://localhost:8000'}`)
    }
  }

  const handlePrediction = async (patientData) => {
    try {
      setIsLoading(true)
      setError(null)

      const response = await api.predictRisk(patientData)
      setResult(response.data)
    } catch (err) {
      console.error('Prediction error:', err)
      if (err.response?.status === 503) {
        setError('Model not loaded. Please train the model first.')
      } else if (err.response?.data?.detail) {
        setError(err.response.data.detail)
      } else {
        setError('Failed to get prediction. Please try again.')
      }
      setResult(null)
    } finally {
      setIsLoading(false)
    }
  }

  const handleReset = () => {
    setResult(null)
    setError(null)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />

      <main className="max-w-6xl mx-auto px-4 py-12">
        {/* API Status Check */}
        {apiStatus !== 'healthy' && (
          <div className={`mb-6 p-4 rounded-lg ${
            apiStatus === 'model-not-loaded'
              ? 'bg-yellow-50 border border-yellow-200'
              : 'bg-red-50 border border-red-200'
          }`}>
            <div className="flex items-start gap-3">
              <AlertCircle className={`w-5 h-5 mt-0.5 ${
                apiStatus === 'model-not-loaded' ? 'text-yellow-600' : 'text-red-600'
              }`} />
              <div>
                <p className={`font-semibold ${
                  apiStatus === 'model-not-loaded' ? 'text-yellow-800' : 'text-red-800'
                }`}>
                  {apiStatus === 'model-not-loaded'
                    ? 'Model Training Required'
                    : 'Cannot Connect to Backend'}
                </p>
                <p className={`text-sm mt-1 ${
                  apiStatus === 'model-not-loaded' ? 'text-yellow-700' : 'text-red-700'
                }`}>
                  {error}
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Error Display */}
        {error && apiStatus === 'healthy' && (
          <div className="mb-6 p-4 rounded-lg bg-red-50 border border-red-200">
            <div className="flex items-start gap-3">
              <AlertCircle className="w-5 h-5 mt-0.5 text-red-600" />
              <div>
                <p className="font-semibold text-red-800">Error</p>
                <p className="text-sm mt-1 text-red-700">{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* Main Content */}
        {result ? (
          <RiskResult result={result} onReset={handleReset} />
        ) : (
          <div className="bg-white rounded-lg shadow-lg p-8">
            <div className="mb-8">
              <h2 className="text-2xl font-bold text-gray-800 mb-2">
                Patient Clinical Assessment
              </h2>
              <p className="text-gray-600 leading-relaxed">
                Enter the patient's seven key clinical parameters below. The system will analyze
                the data and provide a risk assessment for Chronic Lumbopelvic Pain (CLPP).
                All values are required for accurate prediction.
              </p>
            </div>

            {apiStatus === 'healthy' && isLoading && (
              <div className="flex items-center justify-center gap-3 p-8">
                <Loader className="w-5 h-5 animate-spin text-blue-600" />
                <p className="text-gray-600">Analyzing patient data...</p>
              </div>
            )}

            {apiStatus === 'healthy' && !isLoading && (
              <PatientForm onSubmit={handlePrediction} isLoading={isLoading} />
            )}

            {apiStatus !== 'healthy' && (
              <div className="text-center py-8">
                <p className="text-gray-600 mb-4">
                  {apiStatus === 'checking' ? 'Checking API connection...' : 'Unable to load form. Please check the backend connection.'}
                </p>
                {apiStatus === 'error' && (
                  <button
                    onClick={checkApiHealth}
                    className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded-lg transition"
                  >
                    Retry Connection
                  </button>
                )}
              </div>
            )}
          </div>
        )}

        {/* Footer */}
        <footer className="mt-12 text-center text-gray-600 text-sm">
          <p className="mb-2">
            CLPP Risk Prediction System v1.0.0
          </p>
          <p>
            This assessment tool is based on clinical research and uses artificial intelligence
            for preliminary screening only. Always consult with a qualified healthcare professional
            for diagnosis and treatment decisions.
          </p>
        </footer>
      </main>
    </div>
  )
}

export default App
