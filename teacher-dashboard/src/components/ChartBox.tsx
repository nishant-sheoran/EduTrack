"use client";

import React from "react";
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts";
import { TrendingUp, BarChart3 } from "lucide-react";
import Link from "next/link";

interface ChartData {
  name: string;
  [key: string]: string | number;
}

interface ChartBoxProps {
  type: "line" | "bar";
  data: ChartData[];
  title: string;
  dataKey: string;
  accentColor?: string;
  summaryValue?: string;
  summaryLabel?: string;
  href?: string;
}

export default function ChartBox({ 
  type, 
  data, 
  title, 
  dataKey, 
  accentColor = "#34d399",
  summaryValue,
  summaryLabel,
  href
}: ChartBoxProps) {
  if (!data || data.length === 0) {
    return (
      <div className="bg-gray-800 rounded-xl p-4 shadow-lg flex flex-col h-full hover:shadow-xl transition-all duration-300">
        <span className="text-sm font-semibold text-white mb-3">{title}</span>
        <div className="flex-1 flex items-center justify-center">
          <span className="text-gray-400 text-sm">No data available</span>
        </div>
      </div>
    );
  }

  // Calculate summary value if not provided
  const calculatedSummaryValue = summaryValue || (() => {
    if (type === "line") {
      // For engagement timeline, calculate average
      const total = data.reduce((sum, item) => sum + Number(item[dataKey]), 0);
      return `${Math.round(total / data.length)}%`;
    } else {
      // For emotion distribution, get highest count
      const maxItem = data.reduce((max, item) => Number(item[dataKey]) > Number(max[dataKey]) ? item : max, data[0]);
      return String(maxItem[dataKey]);
    }
  })();

  const calculatedSummaryLabel = summaryLabel || (type === "line" ? "Avg Engagement" : "Positive Emotions");

  const content = (
    <div className="group relative bg-gray-800 rounded-xl p-4 shadow-lg flex flex-col h-full hover:shadow-xl transition-all duration-300 cursor-pointer">
      {/* Header */}
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          {type === "line" ? (
            <TrendingUp className="w-4 h-4 text-green-400" />
          ) : (
            <BarChart3 className="w-4 h-4 text-yellow-400" />
          )}
          <span className="text-sm font-semibold text-white">{title}</span>
        </div>
      </div>

      {/* Summary Stats */}
      <div className="mb-3">
        <div className="text-2xl font-bold text-white">{calculatedSummaryValue}</div>
        <div className="text-sm text-gray-400">{calculatedSummaryLabel}</div>
      </div>

      {/* Chart */}
      <div className="flex-1 min-h-0">
        <ResponsiveContainer width="100%" height="100%">
          {type === "line" ? (
            <LineChart data={data} margin={{ top: 5, right: 10, left: 0, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#333" />
              <XAxis dataKey="name" stroke="#999" fontSize={10} />
              <YAxis hide />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: '#1f2937', 
                  border: '1px solid #374151',
                  borderRadius: '8px',
                  fontSize: '12px'
                }}
              />
              <Line 
                type="monotone" 
                dataKey={dataKey} 
                stroke={accentColor} 
                strokeWidth={2} 
                dot={false}
                activeDot={{ r: 4, fill: accentColor }}
              />
            </LineChart>
          ) : (
            <BarChart data={data} margin={{ top: 5, right: 10, left: 0, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#333" />
              <XAxis dataKey="name" stroke="#999" fontSize={10} />
              <YAxis hide />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: '#1f2937', 
                  border: '1px solid #374151',
                  borderRadius: '8px',
                  fontSize: '12px'
                }}
              />
              <Bar dataKey={dataKey} fill={accentColor} radius={[2, 2, 0, 0]} />
            </BarChart>
          )}
        </ResponsiveContainer>
      </div>

      {/* Bottom description */}
      <div className="mt-2 text-xs text-gray-400">
        {type === "line" ? "Track engagement patterns over time" : "Analyze student emotional states"}
      </div>
    </div>
  );

  // Wrap with Link if href is provided
  if (href) {
    return (
      <Link href={href} className="block h-full">
        {content}
      </Link>
    );
  }

  return content;
} 