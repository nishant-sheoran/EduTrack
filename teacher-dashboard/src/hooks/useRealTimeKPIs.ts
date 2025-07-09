import { useState, useEffect, useCallback } from 'react';
import { fetchRealTimeEngagement, calculateRealTimeKPIs, calculateEmotionChartData } from '../lib/mockData';
import { useConfig } from '../contexts/ConfigContext';

export interface RealTimeKPIs {
  totStudents: number;
  attendance: {
    value: string;
    delta: number;
  };
  engagement: {
    value: string;
    delta: number;
  };
  emotions: Array<{ name: string; count: number }>;
  lastUpdated: string;
}

export function useRealTimeKPIs() {
  const { config } = useConfig();
  const [kpis, setKpis] = useState<RealTimeKPIs | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchKPIs = useCallback(async () => {
    try {
      setError(null);
      const engagementData = await fetchRealTimeEngagement();
      
      // Calculate KPIs based on teacher's total students input and detected students
      const calculatedKPIs = calculateRealTimeKPIs(
        config.classStrength,
        engagementData.totalStudents,
        engagementData.detectedFaces,
      );

      const emotionChart = calculateEmotionChartData(engagementData.detectedFaces);

      setKpis({
        totStudents: engagementData.totalStudents,
        ...calculatedKPIs,
        emotions: emotionChart,
        lastUpdated: engagementData.lastUpdated,
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch real-time KPIs');
    } finally {
      setLoading(false);
    }
  }, [config.classStrength]);

  useEffect(() => {
    fetchKPIs();
  }, [config.classStrength, fetchKPIs]); // Refetch when total students changes

  // Update KPIs every 5 seconds for real-time feeling
  useEffect(() => {
    const interval = setInterval(() => {
      fetchKPIs();
    }, 5000);

    return () => clearInterval(interval);
  }, [config.classStrength, fetchKPIs]);

  return {
    kpis,
    loading,
    error,
    refetch: fetchKPIs,
  };
} 