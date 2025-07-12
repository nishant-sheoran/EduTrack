"use client";

import React from "react";
import { Wifi, HardDrive, MemoryStick, RefreshCw, CheckCircle, XCircle, AlertTriangle } from "lucide-react";
import { useSystemHealth } from "../hooks/useSystemHealth";
import { useToast } from "../contexts/ToastContext";
import { RippleButton } from "./magicui/ripple-button";

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
    <div className="bg-gray-800 rounded-xl p-4 shadow-lg flex flex-col h-full hover:shadow-xl transition-all duration-300">
      <div className="flex items-center justify-between mb-3">
        <span className="text-sm font-semibold text-white">System Health</span>
        <RippleButton 
          onClick={handleRefresh}
          className="bg-gray-700 hover:bg-gray-600 text-white border-gray-700 hover:border-gray-600"
          rippleColor="#ffffff"
          duration="600ms"
          disabled={loading}
        >
          <RefreshCw className={`w-3 h-3 text-white ${loading ? 'animate-spin' : ''}`} />
        </RippleButton>
      </div>

      <div className="space-y-3 flex-1 text-xs">
        {/* API Status */}
        <div className="flex items-center gap-2">
          <Wifi className="w-3 h-3 text-blue-400" />
          <span className="text-white">API:</span>
          {getStatusIcon(apiStatus)}
          <span className={`${apiStatus ? 'text-emerald-400' : 'text-red-400'}`}>
            {apiStatus ? 'Active' : 'Failed'}
          </span>
        </div>

        {/* Disk Usage */}
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <HardDrive className="w-3 h-3 text-purple-400" />
            <span className="text-white">Disk:</span>
            <span className={getStatusColor(diskUsage)}>
              {diskUsage.toFixed(1)}%
            </span>
          </div>
          <div className="w-full bg-gray-700 rounded-full h-1.5">
            <div 
              className={`h-1.5 rounded-full transition-all ${
                diskUsage < 70 ? 'bg-emerald-400' : diskUsage < 85 ? 'bg-yellow-400' : 'bg-red-400'
              }`}
              style={{ width: `${diskUsage}%` }}
            />
          </div>
        </div>

        {/* Memory Usage */}
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <MemoryStick className="w-3 h-3 text-cyan-400" />
            <span className="text-white">Memory:</span>
            <span className={getStatusColor(memoryUsage)}>
              {memoryUsage.toFixed(1)}%
            </span>
          </div>
          <div className="w-full bg-gray-700 rounded-full h-1.5">
            <div 
              className={`h-1.5 rounded-full transition-all ${
                memoryUsage < 70 ? 'bg-emerald-400' : memoryUsage < 85 ? 'bg-yellow-400' : 'bg-red-400'
              }`}
              style={{ width: `${memoryUsage}%` }}
            />
          </div>
        </div>

        {/* System Messages */}
        <div className="space-y-1">
          <span className="text-xs font-medium text-gray-300">Messages:</span>
          <div className="space-y-1 max-h-16 overflow-y-auto custom-scrollbar">
            {systemMessages.slice(0, 3).map((message, index) => (
              <div key={index} className="flex items-start gap-1 text-xs text-gray-400">
                <AlertTriangle className="w-3 h-3 text-yellow-400 mt-0.5 flex-shrink-0" />
                <span className="leading-tight">{message.substring(0, 50)}...</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
} 