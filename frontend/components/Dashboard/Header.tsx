import React from 'react';
import { motion } from 'framer-motion';
import { useAnalysisStore } from '@/store/analysisStore';

export const DashboardHeader: React.FC = () => {
  const { latestAnalysis, isLoading } = useAnalysisStore();

  const containerVariants = {
    hidden: { opacity: 0, y: -20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.5 },
    },
  };

  return (
    <motion.div
      initial="hidden"
      animate="visible"
      variants={containerVariants}
      className="mb-8"
    >
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold text-white mb-2">🤖 KubeMind AI</h1>
          <p className="text-gray-400">
            AI-Powered Kubernetes Infrastructure Intelligence Platform
          </p>
        </div>
        <div className="text-right">
          {isLoading && (
            <div className="flex items-center gap-2 text-yellow-400">
              <div className="animate-spin">⚙️</div>
              <span>Analyzing...</span>
            </div>
          )}
          {latestAnalysis && (
            <div className="text-sm text-gray-400">
              <p>Last Updated: {new Date(latestAnalysis.timestamp).toLocaleTimeString()}</p>
            </div>
          )}
        </div>
      </div>
    </motion.div>
  );
};

export default DashboardHeader;
