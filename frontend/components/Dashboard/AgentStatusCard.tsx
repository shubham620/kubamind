import React from 'react';
import { motion } from 'framer-motion';

interface AgentStatus {
  name: string;
  status: 'healthy' | 'warning' | 'error';
  insights_count: number;
  last_analysis: string;
}

interface AgentStatusCardProps {
  agents: AgentStatus[];
}

export const AgentStatusCard: React.FC<AgentStatusCardProps> = ({ agents }) => {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'healthy':
        return 'bg-green-900/20 border-green-600 text-green-200';
      case 'warning':
        return 'bg-yellow-900/20 border-yellow-600 text-yellow-200';
      case 'error':
        return 'bg-red-900/20 border-red-600 text-red-200';
      default:
        return 'bg-gray-900/20 border-gray-600 text-gray-200';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'healthy':
        return '✅';
      case 'warning':
        return '⚠️';
      case 'error':
        return '❌';
      default:
        return '⏳';
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"
    >
      {agents.map((agent) => (
        <div
          key={agent.name}
          className={`p-4 rounded-lg border ${getStatusColor(agent.status)}`}
        >
          <div className="flex items-start justify-between mb-3">
            <h3 className="font-semibold">{agent.name}</h3>
            <span className="text-xl">{getStatusIcon(agent.status)}</span>
          </div>
          <div className="space-y-2 text-sm">
            <p>Insights: <span className="font-semibold">{agent.insights_count}</span></p>
            <p>Last Analysis: {new Date(agent.last_analysis).toLocaleTimeString()}</p>
          </div>
        </div>
      ))}
    </motion.div>
  );
};

export default AgentStatusCard;
