"use client";

import React from "react";
import { Settings, Users, BookOpen, Video, Zap, Save, CheckCircle } from "lucide-react";
import { useConfig } from "../contexts/ConfigContext";
import { useToast } from "../contexts/ToastContext";

export default function ConfigPanel() {
  const { config, updateConfig } = useConfig();
  const { showToast } = useToast();

  const handleSave = () => {
    // Config is automatically saved via context
    showToast({
      type: 'success',
      title: 'Configuration Saved',
      message: 'Your settings have been saved successfully.',
    });
  };

  const handleInputChange = (key: keyof typeof config, value: string | number) => {
    updateConfig({ [key]: value });
  };

  return (
    <div className="bg-gray-800 rounded-xl p-6 shadow-lg flex flex-col h-full">
      <div className="flex items-center gap-2 mb-4">
        <Settings className="w-5 h-5 text-purple-400" />
        <span className="text-lg font-semibold text-white">Configuration</span>
      </div>

      <div className="flex-1 space-y-4 overflow-y-auto custom-scrollbar">
        {/* Class Strength */}
        <div className="space-y-2">
          <label className="flex items-center gap-2 text-sm font-medium text-white">
            <Users className="w-4 h-4" />
            Total Class Strength
          </label>
          <input
            type="number"
            value={config.totalStrength}
            onChange={(e) => handleInputChange('totalStrength', parseInt(e.target.value))}
            className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-blue-400"
            min="1"
            max="1000"
          />
        </div>

        {/* Subject */}
        <div className="space-y-2">
          <label className="flex items-center gap-2 text-sm font-medium text-white">
            <BookOpen className="w-4 h-4" />
            Subject Being Taught
          </label>
          <input
            type="text"
            value={config.subject}
            onChange={(e) => handleInputChange('subject', e.target.value)}
            className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-blue-400"
          />
        </div>

        {/* Video Quality */}
        <div className="space-y-2">
          <label className="flex items-center gap-2 text-sm font-medium text-white">
            <Video className="w-4 h-4" />
            Video Quality
          </label>
          <select
            value={config.videoQuality}
            onChange={(e) => handleInputChange('videoQuality', e.target.value)}
            className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-blue-400"
          >
            <option value="SD">Standard Definition</option>
            <option value="HD">High Definition</option>
            <option value="FHD">Full HD</option>
            <option value="4K">4K Ultra HD</option>
          </select>
        </div>

        {/* Animation Style */}
        <div className="space-y-2">
          <label className="flex items-center gap-2 text-sm font-medium text-white">
            <Zap className="w-4 h-4" />
            Animation Style
          </label>
          <select
            value={config.animationStyle}
            onChange={(e) => handleInputChange('animationStyle', e.target.value)}
            className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-blue-400"
          >
            <option value="None">None</option>
            <option value="Smooth">Smooth</option>
            <option value="Bounce">Bounce</option>
            <option value="Elastic">Elastic</option>
          </select>
        </div>

        {/* Auto-save Frequency */}
        <div className="space-y-2">
          <label className="flex items-center gap-2 text-sm font-medium text-white">
            <Save className="w-4 h-4" />
            Auto-save Frequency (minutes)
          </label>
          <input
            type="number"
            value={config.autoSaveFrequency}
            onChange={(e) => handleInputChange('autoSaveFrequency', parseInt(e.target.value))}
            className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-blue-400"
            min="1"
            max="60"
          />
        </div>

        {/* Engagement Sensitivity */}
        <div className="space-y-2">
          <label className="flex items-center gap-2 text-sm font-medium text-white">
            <Zap className="w-4 h-4" />
            Engagement Sensitivity: {config.engagementSensitivity}%
          </label>
          <input
            type="range"
            value={config.engagementSensitivity}
            onChange={(e) => handleInputChange('engagementSensitivity', parseInt(e.target.value))}
            className="w-full h-2 slider"
            min="0"
            max="100"
          />
        </div>
      </div>

      {/* Save Button */}
      <div className="mt-4">
        <button
          onClick={handleSave}
          className="w-full flex items-center justify-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-500 rounded-lg text-white font-medium btn-interactive"
        >
          <Save className="w-4 h-4" />
          Save Configuration
        </button>
      </div>
    </div>
  );
} 