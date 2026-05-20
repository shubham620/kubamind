import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Analysis endpoints
export const analysisAPI = {
  runAnalysis: () => apiClient.get('/api/analysis/run'),
  getLatest: () => apiClient.get('/api/analysis/latest'),
  getStatus: () => apiClient.get('/api/analysis/status'),
  getHistory: (limit: number = 10) => apiClient.get(`/api/analysis/history?limit=${limit}`),
};

// Agents endpoints
export const agentsAPI = {
  getStatus: () => apiClient.get('/api/agents/status'),
  getCPUAnalysis: () => apiClient.get('/api/agents/cpu/status'),
  getMemoryAnalysis: () => apiClient.get('/api/agents/memory/status'),
  getStorageAnalysis: () => apiClient.get('/api/agents/storage/status'),
  getNetworkAnalysis: () => apiClient.get('/api/agents/network/status'),
  getLogAnalysis: () => apiClient.get('/api/agents/log/status'),
  getDependencyAnalysis: () => apiClient.get('/api/agents/dependency/status'),
};

// Chat endpoints
export const chatAPI = {
  sendMessage: (message: string) => 
    apiClient.post('/api/chat/query', { query: message }),
};

// Health check
export const healthAPI = {
  check: () => apiClient.get('/api/health'),
};

export default apiClient;
