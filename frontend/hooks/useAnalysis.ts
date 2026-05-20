import { useEffect, useCallback } from 'react';
import { analysisAPI } from '@/lib/api';
import { useAnalysisStore } from '@/store/analysisStore';

export function useAnalysis(autoRefresh: boolean = true, interval: number = 30000) {
  const { setLatestAnalysis, addToHistory, setLoading, setError } = useAnalysisStore();

  const fetchLatestAnalysis = useCallback(async () => {
    try {
      setLoading(true);
      const response = await analysisAPI.getLatest();
      setLatestAnalysis(response.data);
      addToHistory(response.data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch analysis');
    } finally {
      setLoading(false);
    }
  }, [setLatestAnalysis, addToHistory, setLoading, setError]);

  const runAnalysis = useCallback(async () => {
    try {
      setLoading(true);
      const response = await analysisAPI.runAnalysis();
      setLatestAnalysis(response.data);
      addToHistory(response.data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to run analysis');
    } finally {
      setLoading(false);
    }
  }, [setLatestAnalysis, addToHistory, setLoading, setError]);

  useEffect(() => {
    if (autoRefresh) {
      fetchLatestAnalysis();
      const intervalId = setInterval(fetchLatestAnalysis, interval);
      return () => clearInterval(intervalId);
    }
  }, [autoRefresh, interval, fetchLatestAnalysis]);

  return { fetchLatestAnalysis, runAnalysis };
}
