import React from 'react'
import { AlertTriangle, CheckCircle, TrendingUp, MessageCircle } from 'lucide-react'

const RiskResult = ({ result, onReset }) => {
  if (!result) return null

  const { risk_probability, risk_percentage, risk_classification, recommendation } = result
  const isHighRisk = risk_classification === 'HIGH RISK'

  return (
    <div className={`rounded-lg shadow-lg overflow-hidden ${
      isHighRisk ? 'border-4 border-red-500 bg-red-50' : 'border-4 border-green-500 bg-green-50'
    }`}>
      {/* Header */}
      <div className={`px-6 py-8 ${isHighRisk ? 'bg-red-600' : 'bg-green-600'}`}>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-3xl font-bold text-white">Risk Assessment Result</h2>
          {isHighRisk ? (
            <AlertTriangle className="w-12 h-12 text-white" />
          ) : (
            <CheckCircle className="w-12 h-12 text-white" />
          )}
        </div>
        <p className="text-red-100 text-sm">
          {new Date().toLocaleString()}
        </p>
      </div>

      {/* Main Results */}
      <div className="px-6 py-8">
        {/* Risk Classification */}
        <div className="mb-8">
          <p className="text-sm text-gray-600 mb-2">Risk Classification</p>
          <div className={`text-4xl font-bold ${
            isHighRisk ? 'text-red-600' : 'text-green-600'
          }`}>
            {risk_classification}
          </div>
        </div>

        {/* Risk Probability */}
        <div className="mb-8">
          <p className="text-sm text-gray-600 mb-3">Risk Probability</p>
          
          {/* Circular Progress */}
          <div className="flex items-center gap-6">
            <div className="relative w-32 h-32">
              <svg className="w-full h-full transform -rotate-90" viewBox="0 0 120 120">
                {/* Background circle */}
                <circle
                  cx="60"
                  cy="60"
                  r="54"
                  stroke="#e5e7eb"
                  strokeWidth="8"
                  fill="none"
                />
                {/* Progress circle */}
                <circle
                  cx="60"
                  cy="60"
                  r="54"
                  stroke={isHighRisk ? '#dc2626' : '#16a34a'}
                  strokeWidth="8"
                  fill="none"
                  strokeDasharray={`${(risk_probability / 1) * 2 * Math.PI * 54} ${2 * Math.PI * 54}`}
                  strokeLinecap="round"
                />
              </svg>
              <div className="absolute inset-0 flex items-center justify-center flex-col">
                <span className={`text-3xl font-bold ${
                  isHighRisk ? 'text-red-600' : 'text-green-600'
                }`}>
                  {risk_percentage.toFixed(1)}%
                </span>
                <span className="text-xs text-gray-500">Risk Level</span>
              </div>
            </div>

            {/* Probability Details */}
            <div className="flex-1">
              <div className="bg-white p-4 rounded-lg border border-gray-200">
                <p className="text-sm text-gray-600 mb-2">Probability Score</p>
                <p className="text-2xl font-bold text-gray-800">
                  {risk_probability.toFixed(4)}
                </p>
                <p className="text-xs text-gray-500 mt-2">
                  {risk_probability > 0.5
                    ? 'Score indicates HIGH RISK (> 0.5)'
                    : 'Score indicates LOW RISK (≤ 0.5)'}
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Recommendation */}
        <div className="mb-8">
          <div className="flex items-start gap-3 bg-white p-5 rounded-lg border border-gray-200">
            <MessageCircle className={`w-6 h-6 mt-1 ${
              isHighRisk ? 'text-red-600' : 'text-green-600'
            }`} />
            <div>
              <p className="font-semibold text-gray-800 mb-2">Clinical Recommendation</p>
              <p className="text-gray-700 leading-relaxed">{recommendation}</p>
            </div>
          </div>
        </div>

        {/* Risk Scale */}
        <div className="mb-8">
          <p className="text-sm text-gray-600 mb-3">Risk Scale</p>
          <div className="bg-white p-4 rounded-lg border border-gray-200">
            <div className="flex justify-between items-center mb-2">
              <span className="text-xs font-semibold text-green-600">Low Risk</span>
              <span className="text-xs font-semibold text-red-600">High Risk</span>
            </div>
            <div className="w-full h-8 bg-gradient-to-r from-green-500 to-red-500 rounded-lg relative">
              <div
                className="h-full w-1 bg-black rounded-full absolute"
                style={{
                  left: `${risk_probability * 100}%`,
                  transform: 'translateX(-50%)',
                }}
              />
            </div>
            <div className="flex justify-between mt-2 text-xs text-gray-500">
              <span>0.0</span>
              <span>0.5 (Threshold)</span>
              <span>1.0</span>
            </div>
          </div>
        </div>

        {/* Information Box */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
          <p className="text-sm text-blue-900 leading-relaxed">
            <strong>Note:</strong> This assessment is based on seven key clinical parameters
            and uses a Logistic Regression model trained on research data from 2,400 participants.
            The score above 0.5 indicates HIGH RISK for Chronic Lumbopelvic Pain. Always consult
            with a healthcare professional for final diagnosis and treatment planning.
          </p>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="px-6 py-6 bg-gray-100 border-t border-gray-200 flex gap-4">
        <button
          onClick={onReset}
          className="flex-1 bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg transition"
        >
          Assess Another Patient
        </button>
        <button
          onClick={() => window.print()}
          className="px-6 bg-gray-600 hover:bg-gray-700 text-white font-bold py-2 rounded-lg transition"
        >
          Print Report
        </button>
      </div>
    </div>
  )
}

export default RiskResult
