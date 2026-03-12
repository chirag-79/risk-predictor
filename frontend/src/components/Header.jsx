import React from 'react'
import { Heart, Activity } from 'lucide-react'

const Header = () => {
  return (
    <header className="bg-gradient-to-r from-blue-600 to-blue-800 shadow-lg">
      <div className="max-w-6xl mx-auto px-4 py-6">
        <div className="flex items-center gap-3 mb-2">
          <div className="bg-white p-2 rounded-lg">
            <Heart className="w-6 h-6 text-red-600" />
          </div>
          <h1 className="text-3xl font-bold text-white">CLPP Risk Prediction</h1>
        </div>
        <p className="text-blue-100 ml-11 text-sm">
          AI-Driven Risk Assessment for Chronic Lumbopelvic Pain in Women
        </p>
      </div>
    </header>
  )
}

export default Header
