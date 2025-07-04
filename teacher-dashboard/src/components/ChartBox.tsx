"use client";

import React from "react";
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts";

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
}

export default function ChartBox({ type, data, title, dataKey, accentColor = "#34d399" }: ChartBoxProps) {
  if (!data || data.length === 0) {
    return (
      <div className="bg-gray-800 rounded-xl p-6 shadow-lg flex flex-col h-full">
        <span className="text-lg font-semibold text-white mb-2">{title}</span>
        <div className="flex-1 min-h-[180px] flex items-center justify-center">
          <span className="text-gray-400">No data available</span>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-gray-800 rounded-xl p-6 shadow-lg flex flex-col h-full">
      <span className="text-lg font-semibold text-white mb-2">{title}</span>
      <div className="flex-1 min-h-[180px]">
        <ResponsiveContainer width="100%" height={200}>
          {type === "line" ? (
            <LineChart data={data} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#222" />
              <XAxis dataKey="name" stroke="#aaa" />
              <YAxis stroke="#aaa" />
              <Tooltip />
              <Line type="monotone" dataKey={dataKey} stroke={accentColor} strokeWidth={3} dot={false} />
            </LineChart>
          ) : (
            <BarChart data={data} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#222" />
              <XAxis dataKey="name" stroke="#aaa" />
              <YAxis stroke="#aaa" />
              <Tooltip />
              <Bar dataKey={dataKey} fill={accentColor} radius={[8, 8, 0, 0]} />
            </BarChart>
          )}
        </ResponsiveContainer>
      </div>
    </div>
  );
} 