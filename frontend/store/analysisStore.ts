import { create } from 'zustand';

interface Analysis {
  timestamp: string;
  agents: Record<string, any>;
  correlations: any[];
  predictions: any[];
  recommendations: any[];
  explanations: any[];
}

interface AnalysisStore {
  latestAnalysis: Analysis | null;
  analysisHistory: Analysis[];
  isLoading: boolean;
  error: string | null;
  setLatestAnalysis: (analysis: Analysis) => void;
  addToHistory: (analysis: Analysis) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  clearHistory: () => void;
}

export const useAnalysisStore = create<AnalysisStore>((set) => ({
  latestAnalysis: null,
  analysisHistory: [],
  isLoading: false,
  error: null,
  setLatestAnalysis: (analysis) => set({ latestAnalysis: analysis }),
  addToHistory: (analysis) =>
    set((state) => ({
      analysisHistory: [analysis, ...state.analysisHistory].slice(0, 100),
    })),
  setLoading: (loading) => set({ isLoading: loading }),
  setError: (error) => set({ error }),
  clearHistory: () => set({ analysisHistory: [] }),
}));
