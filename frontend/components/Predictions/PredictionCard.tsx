import React from 'react';
import { motion } from 'framer-motion';

interface Prediction {
  type: string;
  probability: number;
  forecast_window: string;
  recommended_action: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
}

interface PredictionCardProps {
  predictions: Prediction[];
}

export const PredictionCard: React.FC<PredictionCardProps> = ({ predictions }) => {
  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical':
        return 'border-red-600 bg-red-900/20';
      case 'high':
        return 'border-orange-600 bg-orange-900/20';
      case 'medium':
        return 'border-yellow-600 bg-yellow-900/20';
      case 'low':
        return 'border-blue-600 bg-blue-900/20';
      default:
        return 'border-gray-600 bg-gray-900/20';
    }
  };

  if (!predictions || predictions.length === 0) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="p-6 bg-gray-800 rounded-lg border border-gray-700 text-center text-gray-400"
      >
        No predictions at this time. All metrics within normal parameters! 🎯
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-4"
    >
      <h2 className="text-2xl font-bold text-white mb-6">🔮 Infrastructure Predictions</h2>
      {predictions.map((prediction, idx) => (
        <div
          key={idx}
          className={`p-4 rounded-lg border border-l-4 ${getSeverityColor(prediction.severity)}`}
        >
          <div className="flex items-start justify-between mb-3">
            <div>
              <h3 className="font-semibold text-white">{prediction.type}</h3>
              <p className="text-sm text-gray-300">Window: {prediction.forecast_window}</p>
            </div>
            <div className="text-right">
              <div className="text-2xl font-bold text-white">
                {(prediction.probability * 100).toFixed(0)}%
              </div>
              <p className="text-xs text-gray-400">Probability</p>
            </div>
          </div>
          <div className="bg-black/20 p-3 rounded">
            <p className="text-sm text-white">
              <strong>Recommended Action:</strong> {prediction.recommended_action}
            </p>
          </div>
        </div>
      ))}
    </motion.div>
  );
};

export default PredictionCard;
