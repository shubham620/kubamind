import React from 'react';
import Layout from '@/components/Common/Layout';
import ServiceTopology from '@/components/Topology/ServiceTopology';

export default function Topology() {
  const mockServices = [
    {
      name: 'API Gateway',
      status: 'healthy' as const,
      dependencies: [],
    },
    {
      name: 'Auth Service',
      status: 'healthy' as const,
      dependencies: ['PostgreSQL'],
    },
    {
      name: 'Payment Service',
      status: 'warning' as const,
      dependencies: ['Auth Service', 'Database', 'Cache'],
    },
    {
      name: 'PostgreSQL',
      status: 'healthy' as const,
      dependencies: [],
    },
    {
      name: 'Redis Cache',
      status: 'healthy' as const,
      dependencies: [],
    },
    {
      name: 'Worker Service',
      status: 'healthy' as const,
      dependencies: ['Redis Cache', 'MessageQueue'],
    },
  ];

  return (
    <Layout>
      <div className="space-y-8">
        <div>
          <h1 className="text-4xl font-bold text-white mb-2">🕸️ Service Topology</h1>
          <p className="text-gray-400">
            Microservice dependency graph and health status
          </p>
        </div>

        <ServiceTopology services={mockServices} />
      </div>
    </Layout>
  );
}
