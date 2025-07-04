import { useState, useEffect, useCallback } from 'react';
import { fetchRealTimeEngagement, calculateRealTimeKPIs } from '../lib/mockData';
import { useConfig } from '../contexts/ConfigContext';

export interface RealTimeKPIs {
  attendance: {
    value: string;
    delta: number;
  };
  engagement: {
    value: string;
    delta: number;
  };
  studentsInFrame: number;
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
        config.totalStudents,
        engagementData.studentsInFrame,
        engagementData.detectedFaces
      );

      setKpis({
        ...calculatedKPIs,
        studentsInFrame: engagementData.studentsInFrame,
        lastUpdated: engagementData.lastUpdated,
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch real-time KPIs');
    } finally {
      setLoading(false);
    }
  }, [config.totalStudents]);

  useEffect(() => {
    fetchKPIs();
  }, [config.totalStudents, fetchKPIs]); // Refetch when total students changes

  // Update KPIs every 5 seconds for real-time feeling
  useEffect(() => {
    const interval = setInterval(() => {
      fetchKPIs();
    }, 5000);

    return () => clearInterval(interval);
  }, [config.totalStudents, fetchKPIs]);

  return {
    kpis,
    loading,
    error,
    refetch: fetchKPIs,
  };
} 