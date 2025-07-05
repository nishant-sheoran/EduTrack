"use client";

import React from "react";
import { Settings, Users, BookOpen, Video, Zap, Save } from "lucide-react";
import { useConfig } from "../contexts/ConfigContext";
import { useToast } from "../contexts/ToastContext";
import { RippleButton } from "./magicui/ripple-button";

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
    <div className="bg-gray-800 rounded-xl p-3 shadow-lg flex flex-col hover:shadow-xl transition-all duration-300">
      <div className="flex items-center gap-2 mb-3">
        <Settings className="w-4 h-4 text-purple-400" />
        <span className="text-sm font-semibold text-white">Configuration</span>
      </div>

      <div className="space-y-2">
        {/* Real-time Class Inputs Section */}
        <div className="bg-gray-700 rounded-lg p-3 space-y-2">
          <h3 className="text-xs font-semibold text-emerald-400 flex items-center gap-2">
            <Zap className="w-3 h-3" />
            Live Settings
          </h3>
          
          {/* Total Students */}
          <div className="space-y-1">
            <label className="flex items-center gap-1 text-xs font-medium text-white">
              <Users className="w-3 h-3" />
              Students ({config.totalStudents})
          </label>
          <input
            type="number"
              value={config.totalStudents}
              onChange={(e) => handleInputChange('totalStudents', parseInt(e.target.value) || 0)}
              className="w-full px-2 py-1 bg-gray-600 border border-gray-500 rounded text-white text-xs focus:outline-none focus:border-emerald-400"
            min="1"
              max="200"
          />
        </div>

          {/* Current Subject */}
          <div className="space-y-1">
            <label className="flex items-center gap-1 text-xs font-medium text-white">
              <BookOpen className="w-3 h-3" />
              Subject
          </label>
            <select
              value={config.currentSubject}
              onChange={(e) => handleInputChange('currentSubject', e.target.value)}
              className="w-full px-2 py-1 bg-gray-600 border border-gray-500 rounded text-white text-xs focus:outline-none focus:border-emerald-400"
            >
              <option value="Mathematics">Mathematics</option>
              <option value="Physics">Physics</option>
              <option value="Chemistry">Chemistry</option>
              <option value="Biology">Biology</option>
              <option value="English">English</option>
              <option value="History">History</option>
              <option value="Geography">Geography</option>
              <option value="Computer Science">Computer Science</option>
              <option value="Other">Other</option>
            </select>
          </div>
        </div>

        {/* Quick Settings */}
        <div className="bg-gray-700 rounded-lg p-3 space-y-2">
          <h3 className="text-xs font-semibold text-blue-400 flex items-center gap-1">
            <Video className="w-3 h-3" />
            Settings
          </h3>
          
          <div className="grid grid-cols-2 gap-2">
            <div>
              <label className="text-xs text-gray-300">Quality</label>
          <select
            value={config.videoQuality}
            onChange={(e) => handleInputChange('videoQuality', e.target.value)}
                className="w-full px-2 py-1 bg-gray-600 border border-gray-500 rounded text-white text-xs focus:outline-none focus:border-blue-400"
          >
                <option value="SD">SD</option>
                <option value="HD">HD</option>
                <option value="FHD">FHD</option>
                <option value="4K">4K</option>
          </select>
        </div>

            <div>
              <label className="text-xs text-gray-300">Animation</label>
          <select
            value={config.animationStyle}
            onChange={(e) => handleInputChange('animationStyle', e.target.value)}
                className="w-full px-2 py-1 bg-gray-600 border border-gray-500 rounded text-white text-xs focus:outline-none focus:border-blue-400"
          >
            <option value="None">None</option>
            <option value="Smooth">Smooth</option>
            <option value="Bounce">Bounce</option>
          </select>
        </div>
        </div>
        </div>
      </div>

      {/* Save Button */}
      <div className="mt-3">
        <RippleButton
          onClick={handleSave}
          className="w-full bg-blue-600 hover:bg-blue-500 text-white border-blue-600 hover:border-blue-500 text-xs font-medium"
          rippleColor="#ffffff"
          duration="600ms"
        >
          <div className="flex items-center justify-center gap-2">
            <Save className="w-3 h-3" />
            <span>Save</span>
          </div>
        </RippleButton>
      </div>
    </div>
  );
} 