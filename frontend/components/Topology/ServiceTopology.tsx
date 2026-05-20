import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';

interface ServiceNode {
  name: string;
  status: 'healthy' | 'warning' | 'error';
  dependencies: string[];
}

interface TopologyProps {
  services: ServiceNode[];
}

export const ServiceTopology: React.FC<TopologyProps> = ({ services }) => {
  const [selectedService, setSelectedService] = useState<string | null>(null);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'healthy':
        return '#10b981';
      case 'warning':
        return '#f59e0b';
      case 'error':
        return '#ef4444';
      default:
        return '#6b7280';
    }
  };

  if (!services || services.length === 0) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="p-6 bg-gray-800 rounded-lg border border-gray-700 text-center text-gray-400"
      >
        No service topology data available
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="p-6 bg-gray-800 rounded-lg border border-gray-700"
    >
      <h3 className="text-lg font-semibold text-white mb-6">🕸️ Service Topology</h3>
      
      <div className="flex flex-col gap-4">
        {services.map((service) => (
          <motion.div
            key={service.name}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            whileHover={{ scale: 1.02 }}
            onClick={() => setSelectedService(service.name)}
            className={`p-4 rounded-lg border-l-4 cursor-pointer transition-colors ${
              selectedService === service.name
                ? 'bg-gray-700 border-blue-500'
                : 'bg-gray-900 border-gray-700 hover:bg-gray-700'
            }`}
            style={{
              borderLeftColor: getStatusColor(service.status),
            }}
          >
            <div className="flex items-center justify-between mb-2">
              <h4 className="font-semibold text-white">{service.name}</h4>
              <span className={`px-2 py-1 rounded text-xs ${
                service.status === 'healthy' ? 'bg-green-900/30 text-green-200' :
                service.status === 'warning' ? 'bg-yellow-900/30 text-yellow-200' :
                'bg-red-900/30 text-red-200'
              }`}>
                {service.status}
              </span>
            </div>
            
            {service.dependencies && service.dependencies.length > 0 && (
              <div className="mt-3 pt-3 border-t border-gray-700">
                <p className="text-xs text-gray-400 mb-2">Dependencies:</p>
                <div className="flex gap-2 flex-wrap">
                  {service.dependencies.map((dep) => (
                    <span key={dep} className="text-xs px-2 py-1 bg-gray-800 rounded text-gray-300">
                      → {dep}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
};

export default ServiceTopology;
