import React, { useState } from 'react'
import { AlertCircle, CheckCircle, Loader } from 'lucide-react'

const PatientForm = ({ onSubmit, isLoading = false }) => {
  const [formData, setFormData] = useState({
    hamstring_tightness: '',
    lumbar_lordosis: '',
    hip_flexibility: '',
    foot_posture: '',
    psychological_stress: '',
    physical_activity: '',
    core_performance: '',
  })

  const [errors, setErrors] = useState({})

  const fieldConfig = [
    {
      name: 'hamstring_tightness',
      label: 'Hamstring Tightness',
      description: 'Hamstring muscle tightness test score',
      min: 0,
      max: 100,
      placeholder: 'Enter value (0-100)',
    },
    {
      name: 'lumbar_lordosis',
      label: 'Lumbar Lordosis',
      description: 'Spine lordosis angle measurement (degrees)',
      min: 0,
      max: 100,
      placeholder: 'Enter value (0-100°)',
    },
    {
      name: 'hip_flexibility',
      label: 'Hip Flexibility',
      description: 'Hip range of motion (cm)',
      min: 0,
      max: 100,
      placeholder: 'Enter value (0-100 cm)',
    },
    {
      name: 'foot_posture',
      label: 'Foot Posture Index',
      description: 'Foot posture assessment score',
      min: 0,
      max: 100,
      placeholder: 'Enter value (0-100)',
    },
    {
      name: 'psychological_stress',
      label: 'Psychological Stress',
      description: 'Perceived Stress Scale (PSS)',
      min: 0,
      max: 10,
      placeholder: 'Enter value (0-10)',
    },
    {
      name: 'physical_activity',
      label: 'Physical Activity',
      description: 'IPAQ physical activity level (MET min/week)',
      min: 0,
      max: 10000,
      placeholder: 'Enter value (0-10000)',
    },
    {
      name: 'core_performance',
      label: 'Core Performance',
      description: 'Core strength and stability test',
      min: 0,
      max: 10,
      placeholder: 'Enter value (0-10)',
    },
  ]

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }))
    // Clear error for this field when user starts typing
    if (errors[name]) {
      setErrors((prev) => ({
        ...prev,
        [name]: '',
      }))
    }
  }

  const validateForm = () => {
    const newErrors = {}

    Object.entries(formData).forEach(([key, value]) => {
      if (!value || value === '') {
        newErrors[key] = 'This field is required'
      } else {
        const numValue = parseFloat(value)
        const config = fieldConfig.find((f) => f.name === key)

        if (isNaN(numValue)) {
          newErrors[key] = 'Must be a valid number'
        } else if (numValue < config.min) {
          newErrors[key] = `Minimum value is ${config.min}`
        } else if (numValue > config.max) {
          newErrors[key] = `Maximum value is ${config.max}`
        }
      }
    })

    return newErrors
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    const newErrors = validateForm()

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors)
      return
    }

    // Convert all values to numbers
    const patientData = {}
    Object.entries(formData).forEach(([key, value]) => {
      patientData[key] = parseFloat(value)
    })

    onSubmit(patientData)
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {fieldConfig.map((field) => (
          <div key={field.name} className="flex flex-col">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              {field.label}
              <span className="text-red-500 ml-1">*</span>
            </label>
            <p className="text-xs text-gray-500 mb-2">{field.description}</p>
            <input
              type="number"
              name={field.name}
              value={formData[field.name]}
              onChange={handleChange}
              placeholder={field.placeholder}
              min={field.min}
              max={field.max}
              step="0.1"
              className={`w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition ${
                errors[field.name]
                  ? 'border-red-500 bg-red-50'
                  : 'border-gray-300 bg-white'
              }`}
              disabled={isLoading}
            />
            {errors[field.name] && (
              <div className="flex items-center mt-1 text-xs text-red-600">
                <AlertCircle className="w-3 h-3 mr-1" />
                {errors[field.name]}
              </div>
            )}
          </div>
        ))}
      </div>

      <button
        type="submit"
        disabled={isLoading}
        className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-bold py-3 px-4 rounded-lg transition flex items-center justify-center gap-2"
      >
        {isLoading ? (
          <>
            <Loader className="w-5 h-5 animate-spin" />
            Analyzing Patient Data...
          </>
        ) : (
          <>
            <CheckCircle className="w-5 h-5" />
            Predict Risk
          </>
        )}
      </button>
    </form>
  )
}

export default PatientForm
