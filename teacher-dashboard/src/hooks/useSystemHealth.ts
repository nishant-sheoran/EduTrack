import { useState, useEffect } from 'react';
import { fetchSystemHealth } from '../lib/mockData';

export interface SystemHealth {
  apiStatus: boolean;
  diskUsage: number;
  memoryUsage: number;
  systemMessages: string[];
}

export function useSystemHealth() {
  const [health, setHealth] = useState<SystemHealth | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchHealth = async () => {
    try {
      setLoading(true);
      setError(null);
      const result = await fetchSystemHealth();
      setHealth(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch system health');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHealth();
  }, []);

  // Refresh system health every 10 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      fetchHealth();
    }, 10000);

    return () => clearInterval(interval);
  }, []);

  return {
    health,
    loading,
    error,
    refresh: fetchHealth,
  };
} 