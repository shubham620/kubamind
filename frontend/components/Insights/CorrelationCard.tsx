import React from 'react';
import { motion } from 'framer-motion';

interface Correlation {
  type: string;
  agents_involved: string[];
  description: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  confidence: number;
}

interface CorrelationCardProps {
  correlations: Correlation[];
}

export const CorrelationCard: React.FC<CorrelationCardProps> = ({ correlations }) => {
  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical':
        return 'bg-red-900/20 border-red-600 text-red-200';
      case 'high':
        return 'bg-orange-900/20 border-orange-600 text-orange-200';
      case 'medium':
        return 'bg-yellow-900/20 border-yellow-600 text-yellow-200';
      case 'low':
        return 'bg-blue-900/20 border-blue-600 text-blue-200';
      default:
        return 'bg-gray-900/20 border-gray-600 text-gray-200';
    }
  };

  if (!correlations || correlations.length === 0) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="p-6 bg-gray-800 rounded-lg border border-gray-700 text-center text-gray-400"
      >
        No correlations found. Infrastructure running smoothly! ✨
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-4"
    >
      <h2 className="text-2xl font-bold text-white mb-6">🔗 Insight Correlations</h2>
      {correlations.map((correlation, idx) => (
        <div
          key={idx}
          className={`p-4 rounded-lg border ${getSeverityColor(correlation.severity)}`}
        >
          <div className="flex items-start justify-between mb-2">
            <h3 className="font-semibold">{correlation.type}</h3>
            <div className="text-sm">
              Confidence: <span className="font-semibold">{(correlation.confidence * 100).toFixed(0)}%</span>
            </div>
          </div>
          <p className="text-sm mb-3">{correlation.description}</p>
          <div className="flex gap-2 flex-wrap">
            {correlation.agents_involved.map((agent) => (
              <span key={agent} className="text-xs px-2 py-1 bg-white/10 rounded">
                {agent}
              </span>
            ))}
          </div>
        </div>
      ))}
    </motion.div>
  );
};

export default CorrelationCard;
