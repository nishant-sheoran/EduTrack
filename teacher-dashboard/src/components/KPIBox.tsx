import React from "react";
import { ArrowUpRight, ArrowDownRight } from "lucide-react";

interface KPIBoxProps {
  title: string;
  value: string | number;
  delta?: number;
  icon?: React.ReactNode;
  accentColor?: string;
}

export default function KPIBox({ title, value, delta, icon, accentColor = "text-emerald-400" }: KPIBoxProps) {
  return (
    <div className="bg-gray-800 rounded-xl p-6 shadow-lg flex flex-col gap-2 min-h-[100px]">
      <div className="flex items-center gap-2">
        {icon && <span className={`w-6 h-6 ${accentColor}`}>{icon}</span>}
        <span className="text-lg font-semibold text-white">{title}</span>
      </div>
      <div className="flex items-end gap-2">
        <span className={`text-3xl font-bold ${accentColor}`}>{value}</span>
        {typeof delta === "number" && (
          <span className={`text-sm flex items-center ${delta >= 0 ? "text-emerald-400" : "text-red-400"}`}>
            {delta >= 0 ? <ArrowUpRight className="w-4 h-4" /> : <ArrowDownRight className="w-4 h-4" />}
            {Math.abs(delta)}%
          </span>
        )}
      </div>
    </div>
  );
} 