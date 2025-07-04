"use client";

import React, { createContext, useContext } from 'react';
import { useLocalStorage } from '../hooks/useLocalStorage';

export interface TeacherConfig {
  totalStrength: number;
  subject: string;
  videoQuality: string;
  animationStyle: string;
  autoSaveFrequency: number;
  engagementSensitivity: number;
}

const defaultConfig: TeacherConfig = {
  totalStrength: 30,
  subject: "Mathematics",
  videoQuality: "HD",
  animationStyle: "Smooth",
  autoSaveFrequency: 5,
  engagementSensitivity: 75,
};

interface ConfigContextType {
  config: TeacherConfig;
  updateConfig: (updates: Partial<TeacherConfig>) => void;
  resetConfig: () => void;
}

const ConfigContext = createContext<ConfigContextType | undefined>(undefined);

export function ConfigProvider({ children }: { children: React.ReactNode }) {
  const [config, setConfig] = useLocalStorage<TeacherConfig>('teacherConfig', defaultConfig);

  const updateConfig = (updates: Partial<TeacherConfig>) => {
    setConfig((prev) => ({ ...prev, ...updates }));
  };

  const resetConfig = () => {
    setConfig(defaultConfig);
  };

  return (
    <ConfigContext.Provider value={{ config, updateConfig, resetConfig }}>
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