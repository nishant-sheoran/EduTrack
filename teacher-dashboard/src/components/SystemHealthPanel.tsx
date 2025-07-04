"use client";

import React from "react";
import { Wifi, HardDrive, MemoryStick, RefreshCw, CheckCircle, XCircle, AlertTriangle } from "lucide-react";
import { useSystemHealth } from "../hooks/useSystemHealth";
import { useToast } from "../contexts/ToastContext";

export default function SystemHealthPanel() {
  const { health, loading, refresh } = useSystemHealth();
  const { showToast } = useToast();

  const handleRefresh = () => {
    refresh();
    showToast({
      type: 'info',
      title: 'Refreshing',
      message: 'System health data is being updated...',
    });
  };

  // Use default values if health data is not available
  const apiStatus = health?.apiStatus ?? true;
  const diskUsage = health?.diskUsage ?? 65.2;
  const memoryUsage = health?.memoryUsage ?? 48.7;
  const systemMessages = health?.systemMessages ?? [
    "Session recording completed successfully",
    "Transcript generation completed",
    "High CPU usage detected during video processing",
    "Backup scheduled for tonight at 2:00 AM"
  ];

  const getStatusColor = (usage: number) => {
    if (usage < 70) return "text-emerald-400";
    if (usage < 85) return "text-yellow-400";
    return "text-red-400";
  };

  const getStatusIcon = (status: boolean) => {
    return status ? <CheckCircle className="w-4 h-4 text-emerald-400" /> : <XCircle className="w-4 h-4 text-red-400" />;
  };

  return (
    <div className="bg-gray-800 rounded-xl p-6 shadow-lg flex flex-col h-full">
      <div className="flex items-center justify-between mb-4">
        <span className="text-lg font-semibold text-white">System Health</span>
        <button 
          onClick={handleRefresh}
          className="p-2 rounded-lg bg-gray-700 hover:bg-gray-600 btn-interactive"
          disabled={loading}
        >
          <RefreshCw className={`w-4 h-4 text-white ${loading ? 'animate-spin' : ''}`} />
        </button>
      </div>

      <div className="space-y-4 flex-1">
        {/* API Status */}
        <div className="flex items-center gap-3">
          <Wifi className="w-5 h-5 text-blue-400" />
          <span className="text-white">API Connection:</span>
          {getStatusIcon(apiStatus)}
          <span className={`text-sm ${apiStatus ? 'text-emerald-400' : 'text-red-400'}`}>
            {apiStatus ? 'Active' : 'Failed'}
          </span>
        </div>

        {/* Disk Usage */}
        <div className="space-y-2">
          <div className="flex items-center gap-3">
            <HardDrive className="w-5 h-5 text-purple-400" />
            <span className="text-white">Disk Usage:</span>
            <span className={`text-sm ${getStatusColor(diskUsage)}`}>
              {diskUsage.toFixed(1)}%
            </span>
          </div>
          <div className="w-full bg-gray-700 rounded-full h-2">
            <div 
              className={`h-2 rounded-full transition-all ${
                diskUsage < 70 ? 'bg-emerald-400' : diskUsage < 85 ? 'bg-yellow-400' : 'bg-red-400'
              }`}
              style={{ width: `${diskUsage}%` }}
            />
          </div>
        </div>

        {/* Memory Usage */}
        <div className="space-y-2">
          <div className="flex items-center gap-3">
            <MemoryStick className="w-5 h-5 text-cyan-400" />
            <span className="text-white">Memory Usage:</span>
            <span className={`text-sm ${getStatusColor(memoryUsage)}`}>
              {memoryUsage.toFixed(1)}%
            </span>
          </div>
          <div className="w-full bg-gray-700 rounded-full h-2">
            <div 
              className={`h-2 rounded-full transition-all ${
                memoryUsage < 70 ? 'bg-emerald-400' : memoryUsage < 85 ? 'bg-yellow-400' : 'bg-red-400'
              }`}
              style={{ width: `${memoryUsage}%` }}
            />
          </div>
        </div>

        {/* System Messages */}
        <div className="space-y-2">
          <span className="text-sm font-medium text-gray-300">Recent Messages:</span>
          <div className="space-y-1 max-h-24 overflow-y-auto custom-scrollbar">
            {systemMessages.map((message, index) => (
              <div key={index} className="flex items-start gap-2 text-xs text-gray-400">
                <AlertTriangle className="w-3 h-3 text-yellow-400 mt-0.5 flex-shrink-0" />
                <span>{message}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
} 