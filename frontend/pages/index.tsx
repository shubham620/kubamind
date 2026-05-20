import React, { useEffect } from 'react';
import Layout from '@/components/Common/Layout';
import DashboardHeader from '@/components/Dashboard/Header';
import AgentStatusCard from '@/components/Dashboard/AgentStatusCard';
import AlertNotifications from '@/components/Common/AlertNotifications';
import MetricsVisualization from '@/components/Common/MetricsVisualization';
import { useAnalysis } from '@/hooks/useAnalysis';
import { useAnalysisStore } from '@/store/analysisStore';
import { useUIStore } from '@/store/uiStore';

export default function Dashboard() {
  const { latestAnalysis, isLoading } = useAnalysisStore();
  const { runAnalysis } = useAnalysis();
  const { addNotification } = useUIStore();

  useEffect(() => {
    const loadDashboard = async () => {
      try {
        await runAnalysis();
      } catch (error) {
        addNotification('Failed to load analysis', 'error');
      }
    };

    loadDashboard();
    const interval = setInterval(loadDashboard, 30000);
    return () => clearInterval(interval);
  }, [runAnalysis, addNotification]);

  const mockAgents = [
    { name: 'CPU Agent', status: 'healthy' as const, insights_count: 5, last_analysis: new Date().toISOString() },
    { name: 'Memory Agent', status: 'healthy' as const, insights_count: 3, last_analysis: new Date().toISOString() },
    { name: 'Storage Agent', status: 'warning' as const, insights_count: 2, last_analysis: new Date().toISOString() },
    { name: 'Network Agent', status: 'healthy' as const, insights_count: 4, last_analysis: new Date().toISOString() },
    { name: 'Log Agent', status: 'healthy' as const, insights_count: 6, last_analysis: new Date().toISOString() },
    { name: 'Dependency Agent', status: 'healthy' as const, insights_count: 3, last_analysis: new Date().toISOString() },
  ];

  const mockAlerts = [
    {
      id: '1',
      title: 'High Disk Usage',
      description: 'Storage usage in pod-xyz has reached 75%',
      type: 'warning' as const,
      timestamp: new Date().toISOString(),
    },
    {
      id: '2',
      title: 'Successful Analysis',
      description: 'Latest analysis cycle completed successfully',
      type: 'success' as const,
      timestamp: new Date().toISOString(),
    },
  ];

  const mockChartData = [
    { name: 'Pod 1', value: 45 },
    { name: 'Pod 2', value: 62 },
    { name: 'Pod 3', value: 38 },
    { name: 'Pod 4', value: 71 },
  ];

  return (
    <Layout>
      <DashboardHeader />

      <div className="space-y-8">
        {/* Action Buttons */}
        <div className="flex gap-4">
          <button
            onClick={runAnalysis}
            disabled={isLoading}
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-semibold transition-colors disabled:opacity-50"
          >
            {isLoading ? 'Analyzing...' : 'Run Analysis Now'}
          </button>
        </div>

        {/* Alerts */}
        {mockAlerts.length > 0 && (
          <div>
            <h2 className="text-2xl font-bold text-white mb-4">📢 Alerts & Notifications</h2>
            <AlertNotifications alerts={mockAlerts} />
          </div>
        )}

        {/* Agent Status */}
        <div>
          <h2 className="text-2xl font-bold text-white mb-4">🔍 AI Agent Status</h2>
          <AgentStatusCard agents={mockAgents} />
        </div>

        {/* Metrics Visualizations */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <MetricsVisualization
            title="CPU Usage by Pod"
            data={mockChartData}
            type="bar"
          />
          <MetricsVisualization
            title="Memory Distribution"
            data={mockChartData}
            type="pie"
          />
        </div>
      </div>
    </Layout>
  );
}
