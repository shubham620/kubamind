import React, { useState } from 'react';
import { motion } from 'framer-motion';

interface AlertNotificationsProps {
  alerts: Array<{
    id: string;
    title: string;
    description: string;
    type: 'error' | 'warning' | 'info' | 'success';
    timestamp: string;
  }>;
  onClose?: (id: string) => void;
}

export const AlertNotifications: React.FC<AlertNotificationsProps> = ({ alerts, onClose }) => {
  const getAlertColor = (type: string) => {
    switch (type) {
      case 'error':
        return 'border-red-500 bg-red-900/20 text-red-200';
      case 'warning':
        return 'border-yellow-500 bg-yellow-900/20 text-yellow-200';
      case 'success':
        return 'border-green-500 bg-green-900/20 text-green-200';
      case 'info':
        return 'border-blue-500 bg-blue-900/20 text-blue-200';
      default:
        return 'border-gray-500 bg-gray-900/20 text-gray-200';
    }
  };

  const getAlertIcon = (type: string) => {
    switch (type) {
      case 'error':
        return '❌';
      case 'warning':
        return '⚠️';
      case 'success':
        return '✅';
      case 'info':
        return 'ℹ️';
      default:
        return '📢';
    }
  };

  if (!alerts || alerts.length === 0) {
    return null;
  }

  return (
    <div className="space-y-3">
      {alerts.map((alert) => (
        <motion.div
          key={alert.id}
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -20 }}
          className={`p-4 rounded-lg border-l-4 ${getAlertColor(alert.type)}`}
        >
          <div className="flex items-start justify-between">
            <div className="flex items-start gap-3">
              <span className="text-xl mt-1">{getAlertIcon(alert.type)}</span>
              <div>
                <h4 className="font-semibold">{alert.title}</h4>
                <p className="text-sm opacity-90">{alert.description}</p>
                <p className="text-xs opacity-60 mt-1">{new Date(alert.timestamp).toLocaleString()}</p>
              </div>
            </div>
            {onClose && (
              <button
                onClick={() => onClose(alert.id)}
                className="text-sm opacity-60 hover:opacity-100 transition-opacity"
              >
                ✕
              </button>
            )}
          </div>
        </motion.div>
      ))}
    </div>
  );
};

export default AlertNotifications;
