import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const api = {
  // Health check
  checkHealth: () => apiClient.get('/health'),

  // Predict CLPP risk
  predictRisk: (patientData) => apiClient.post('/predict', patientData),

  // Get sample prediction
  getSamplePrediction: () => apiClient.get('/sample-prediction'),

  // Get model info
  getModelInfo: () => apiClient.get('/info'),

  // Get API root info
  getApiInfo: () => apiClient.get('/'),
}

export default api
