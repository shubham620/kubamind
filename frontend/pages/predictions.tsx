import React, { useEffect } from 'react';
import Layout from '@/components/Common/Layout';
import PredictionCard from '@/components/Predictions/PredictionCard';
import { useAnalysisStore } from '@/store/analysisStore';
import { useAnalysis } from '@/hooks/useAnalysis';

export default function Predictions() {
  const { latestAnalysis } = useAnalysisStore();
  const { fetchLatestAnalysis } = useAnalysis();

  useEffect(() => {
    fetchLatestAnalysis();
  }, [fetchLatestAnalysis]);

  const mockPredictions = [
    {
      type: 'Pod Crash Risk',
      probability: 0.72,
      forecast_window: '2-4 hours',
      recommended_action: 'Increase pod replicas or optimize workload',
      severity: 'high' as const,
    },
    {
      type: 'OOM Event',
      probability: 0.45,
      forecast_window: '6-8 hours',
      recommended_action: 'Increase memory limits or implement memory optimization',
      severity: 'medium' as const,
    },
    {
      type: 'Disk Exhaustion',
      probability: 0.31,
      forecast_window: '24-48 hours',
      recommended_action: 'Clean up old logs or increase PVC size',
      severity: 'low' as const,
    },
    {
      type: 'Network Congestion',
      probability: 0.58,
      forecast_window: '1-2 hours',
      recommended_action: 'Implement rate limiting or load balancing',
      severity: 'high' as const,
    },
  ];

  return (
    <Layout>
      <div className="space-y-8">
        <div>
          <h1 className="text-4xl font-bold text-white mb-2">🔮 Predictions</h1>
          <p className="text-gray-400">
            AI-powered forecasts of potential infrastructure issues
          </p>
        </div>

        {latestAnalysis ? (
          <PredictionCard predictions={mockPredictions} />
        ) : (
          <div className="text-center text-gray-400 py-12">
            <p>Run an analysis to see predictions</p>
          </div>
        )}
      </div>
    </Layout>
  );
}
