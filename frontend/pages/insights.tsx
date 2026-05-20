import React, { useEffect } from 'react';
import Layout from '@/components/Common/Layout';
import CorrelationCard from '@/components/Insights/CorrelationCard';
import { useAnalysisStore } from '@/store/analysisStore';
import { useAnalysis } from '@/hooks/useAnalysis';

export default function Insights() {
  const { latestAnalysis } = useAnalysisStore();
  const { fetchLatestAnalysis } = useAnalysis();

  useEffect(() => {
    fetchLatestAnalysis();
  }, [fetchLatestAnalysis]);

  const mockCorrelations = [
    {
      type: 'Database Load Cascade',
      agents_involved: ['CPU Agent', 'Storage Agent', 'Network Agent'],
      description: 'High database write activity is causing elevated CPU and network throughput',
      severity: 'high' as const,
      confidence: 0.92,
    },
    {
      type: 'Memory Leak Detected',
      agents_involved: ['Memory Agent', 'Log Agent'],
      description: 'Gradual memory increase pattern correlates with specific error logs',
      severity: 'medium' as const,
      confidence: 0.78,
    },
    {
      type: 'Network Bottleneck',
      agents_involved: ['Network Agent', 'Dependency Agent'],
      description: 'Service-to-service communication latency increasing due to pod density',
      severity: 'low' as const,
      confidence: 0.65,
    },
  ];

  return (
    <Layout>
      <div className="space-y-8">
        <div>
          <h1 className="text-4xl font-bold text-white mb-2">💡 AI Insights</h1>
          <p className="text-gray-400">
            Correlated analysis from all AI agents revealing infrastructure patterns
          </p>
        </div>

        {latestAnalysis ? (
          <div className="space-y-6">
            <CorrelationCard correlations={mockCorrelations} />
            
            {/* Recommendations */}
            <div className="p-6 bg-gray-800 rounded-lg border border-gray-700">
              <h3 className="text-lg font-semibold text-white mb-4">💡 Recommendations</h3>
              <ul className="space-y-3">
                <li className="flex gap-3">
                  <span className="text-yellow-400">→</span>
                  <span className="text-gray-200">Optimize database query patterns to reduce I/O</span>
                </li>
                <li className="flex gap-3">
                  <span className="text-yellow-400">→</span>
                  <span className="text-gray-200">Implement connection pooling for database services</span>
                </li>
                <li className="flex gap-3">
                  <span className="text-yellow-400">→</span>
                  <span className="text-gray-200">Increase network bandwidth for inter-pod communication</span>
                </li>
                <li className="flex gap-3">
                  <span className="text-yellow-400">→</span>
                  <span className="text-gray-200">Monitor memory allocations in background workers</span>
                </li>
              </ul>
            </div>
          </div>
        ) : (
          <div className="text-center text-gray-400 py-12">
            <p>Run an analysis to see insights</p>
          </div>
        )}
      </div>
    </Layout>
  );
}
