import React from 'react';
import Layout from '@/components/Common/Layout';

export default function Logs() {
  const mockLogs = [
    {
      timestamp: new Date(Date.now() - 5000).toISOString(),
      level: 'ERROR',
      service: 'payment-service',
      message: 'Database connection timeout',
    },
    {
      timestamp: new Date(Date.now() - 10000).toISOString(),
      level: 'WARNING',
      service: 'auth-service',
      message: 'High memory usage detected',
    },
    {
      timestamp: new Date(Date.now() - 15000).toISOString(),
      level: 'INFO',
      service: 'api-gateway',
      message: 'Request rate: 5000 req/s',
    },
    {
      timestamp: new Date(Date.now() - 20000).toISOString(),
      level: 'ERROR',
      service: 'worker-service',
      message: 'Failed to process job: job_12345',
    },
  ];

  const getLevelColor = (level: string) => {
    switch (level) {
      case 'ERROR':
        return 'text-red-400 bg-red-900/20';
      case 'WARNING':
        return 'text-yellow-400 bg-yellow-900/20';
      case 'INFO':
        return 'text-blue-400 bg-blue-900/20';
      default:
        return 'text-gray-400 bg-gray-900/20';
    }
  };

  return (
    <Layout>
      <div className="space-y-8">
        <div>
          <h1 className="text-4xl font-bold text-white mb-2">📝 Logs & Events</h1>
          <p className="text-gray-400">
            Real-time infrastructure logs and NLP-based summaries
          </p>
        </div>

        <div className="bg-gray-800 rounded-lg border border-gray-700 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-700 bg-gray-900">
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-300">Timestamp</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-300">Level</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-300">Service</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-300">Message</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-700">
                {mockLogs.map((log, idx) => (
                  <tr key={idx} className="hover:bg-gray-700/50 transition-colors">
                    <td className="px-6 py-3 text-sm text-gray-400">
                      {new Date(log.timestamp).toLocaleTimeString()}
                    </td>
                    <td className={`px-6 py-3 text-sm font-semibold ${getLevelColor(log.level)}`}>
                      {log.level}
                    </td>
                    <td className="px-6 py-3 text-sm text-gray-300">{log.service}</td>
                    <td className="px-6 py-3 text-sm text-gray-300">{log.message}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </Layout>
  );
}
