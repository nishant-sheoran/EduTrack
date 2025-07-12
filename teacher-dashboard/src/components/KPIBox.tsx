import React from "react";
import { ArrowUpRight, ArrowDownRight } from "lucide-react";
import { AnimatedCircularProgressBar } from "./magicui/animated-circular-progress-bar";

interface KPIBoxProps {
  title: string;
  value: string | number;
  delta?: number;
  icon?: React.ReactNode;
  accentColor?: string;
}

export default function KPIBox({ title, value, delta, icon, accentColor = "text-emerald-400" }: KPIBoxProps) {
  // Compact style for Live KPI cards
  if (title === "Live Attendance" || title === "Live Engagement" || title === "Students in Frame") {
    const percent = typeof value === "number" ? value : parseFloat(value.toString().replace(/[^\d.]/g, ''));
    
    // Set specific colors for each card
    let progressColor = "#10b981"; // default green
    let textColor = "text-emerald-400";
    
    if (title === "Live Engagement") {
      progressColor = "#3b82f6"; // blue
      textColor = "text-blue-400";
    } else if (title === "Students in Frame") {
      progressColor = "#06b6d4"; // cyan
      textColor = "text-cyan-400";
    }
    
    return (
      <div className="bg-gray-800 rounded-xl p-4 flex flex-col shadow transition hover:shadow-lg border border-gray-800 h-auto w-full">
        <div className="flex items-center gap-2 mb-3">
          {icon && <span className={`w-5 h-5 ${textColor} flex-shrink-0`}>{icon}</span>}
          <span className="text-sm font-semibold text-gray-100 truncate">{title}</span>
        </div>
        <div className="relative flex flex-col items-center justify-center flex-1">
          <div className="scale-75">
            <AnimatedCircularProgressBar value={percent} max={100} gaugePrimaryColor={progressColor} gaugeSecondaryColor="#374151" />
          </div>
        </div>
        {typeof delta === "number" && (
          <div className="flex justify-start mt-2">
            <span className={`text-sm flex items-center ${delta >= 0 ? textColor : "text-red-400"}`}>
              {delta >= 0 ? <ArrowUpRight className="w-4 h-4 mr-1" /> : <ArrowDownRight className="w-4 h-4 mr-1" />}
              {Math.abs(delta).toFixed(1)}%
            </span>
          </div>
        )}
      </div>
    );
  }

  return (
    <div className="bg-gray-800 rounded-xl p-4 shadow-lg flex flex-col justify-between h-full hover:shadow-xl transition-all duration-300">
      <div className="flex items-center gap-2 mb-2">
        {icon && <span className={`w-5 h-5 ${accentColor} flex-shrink-0`}>{icon}</span>}
        <span className="text-sm font-medium text-gray-300 truncate">{title}</span>
      </div>
      <div className="flex items-end gap-2 mt-auto">
        <span className={`text-2xl font-bold ${accentColor} leading-none`}>{value}</span>
        {typeof delta === "number" && (
          <span className={`text-xs flex items-center ${delta >= 0 ? "text-emerald-400" : "text-red-400"} leading-none`}>
            {delta >= 0 ? <ArrowUpRight className="w-3 h-3" /> : <ArrowDownRight className="w-3 h-3" />}
            {Math.abs(delta).toFixed(1)}%
          </span>
        )}
      </div>
    </div>
  );
} 