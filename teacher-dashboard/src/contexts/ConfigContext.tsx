// src/contexts/ConfigContext.tsx

"use client";

// 1. Import useCallback from React
import React, { createContext, useContext, useState, useCallback, useMemo } from 'react';
import { useLocalStorage } from '../hooks/useLocalStorage';

export interface TeacherConfig {
  // ... (interface remains the same)
  classStrength: number;
  currentSubject: string;
  studentAttendance: number;
  videoQuality: string;
  animationStyle: string;
  autoSaveFrequency: number;
  engagementSensitivity: number;
  session_duration: string;
  transcriptURL: string;
  videoURL: string;
}

const defaultConfig: TeacherConfig = {
  // ... (defaultConfig remains the same)
  classStrength: 30,
  studentAttendance: 28,
  currentSubject: "Mathematics",
  videoQuality: "HD",
  animationStyle: "Smooth",
  autoSaveFrequency: 5,
  engagementSensitivity: 75,
  session_duration: "45:30",
  transcriptURL: 'path/to/transcript',
  videoURL: 'path/to/video',
};

interface ConfigContextType {
  config: TeacherConfig;
  updateConfig: (updates: Partial<TeacherConfig>) => void;
  resetConfig: () => void;
  isAnalyticsActive: boolean;
  setIsAnalyticsActive: (isActive: boolean) => void;
}

const ConfigContext = createContext<ConfigContextType | undefined>(undefined);

export function ConfigProvider({ children }: { children: React.ReactNode }) {
  const [config, setConfig] = useLocalStorage<TeacherConfig>('teacherConfig', defaultConfig);
  const [isAnalyticsActive, setIsAnalyticsActive] = useLocalStorage<boolean>('isAnalyticsActive', false);

  // **FIX**: Add dependency array and prevent unnecessary updates
  const updateConfig = useCallback((updates: Partial<TeacherConfig>) => {
    setConfig((prev) => {
      // **FIX**: Only update if values actually changed
      const newConfig = { ...prev, ...updates };
      const hasChanges = Object.keys(updates).some(key => 
        prev[key as keyof TeacherConfig] !== updates[key as keyof TeacherConfig]
      );
      
      if (!hasChanges) {
        return prev; // Return same reference if no changes
      }
      
      return newConfig;
    });
  }, [setConfig]);

  const resetConfig = useCallback(() => {
    setConfig(defaultConfig);
  }, [setConfig]);

  // **FIX**: Memoize the context value to prevent unnecessary re-renders
  const contextValue = useMemo(() => ({
    config,
    updateConfig,
    resetConfig,
    isAnalyticsActive,
    setIsAnalyticsActive
  }), [config, updateConfig, resetConfig, isAnalyticsActive, setIsAnalyticsActive]);

  return (
    <ConfigContext.Provider value={contextValue}>
      {children}
    </ConfigContext.Provider>
  );
}

// **ADD THIS BACK**: The useConfig hook that was missing
export function useConfig() {
  const context = useContext(ConfigContext);
  if (context === undefined) {
    throw new Error('useConfig must be used within a ConfigProvider');
  }
  return context;
}
