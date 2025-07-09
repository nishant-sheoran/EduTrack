"use client";

import React, { createContext, useContext, useState } from 'react';
import { useLocalStorage } from '../hooks/useLocalStorage';

export interface TeacherConfig {
  // Core class inputs for real-time calculations
  classStrength: number;
  currentSubject: string;

  // Existing config options
  videoQuality: string;
  animationStyle: string;
  autoSaveFrequency: number;
  engagementSensitivity: number;
}

const defaultConfig: TeacherConfig = {
  classStrength: 30,
  currentSubject: "Mathematics",
  videoQuality: "HD",
  animationStyle: "Smooth",
  autoSaveFrequency: 5,
  engagementSensitivity: 75,
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


  const updateConfig = (updates: Partial<TeacherConfig>) => {
    setConfig((prev) => ({ ...prev, ...updates }));
  };

  const resetConfig = () => {
    setConfig(defaultConfig);
  };

  return (
    <ConfigContext.Provider value={{ config, updateConfig, resetConfig, isAnalyticsActive, setIsAnalyticsActive }}>
      {children}
    </ConfigContext.Provider>
  );
}

export function useConfig() {
  const context = useContext(ConfigContext);
  if (context === undefined) {
    throw new Error('useConfig must be used within a ConfigProvider');
  }
  return context;
}