"use client";

import React from "react";
import { ArrowLeft, Smile, Users, AlertTriangle, TrendingUp } from "lucide-react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, PieChart, Pie, Cell } from "recharts";
import { useRealTimeKPIs } from "../../hooks/useRealTimeKPIs";
import Link from "next/link";

export default function EmotionDistributionPage() {
  const { kpis, loading } = useRealTimeKPIs();

  const emotionMeta: Record<string, { label: string; color: string; status: string }> = {
    happy: { label: "Happy", color: "#10B981", status: "Positive" },
    neutral: { label: "Neutral", color: "#6B7280", status: "Neutral" },
    sad: { label: "Sad", color: "#F59E0B", status: "Needs Attention" },
    anger: { label: "Anger", color: "#EF4444", status: "Needs Attention" },
    surprise: { label: "Surprise", color: "#3B82F6", status: "Needs Attention" },
  };

  const fallbackEmotions = [
    { name: "happy", count: 10 },
    { name: "neutral", count: 8 },
    { name: "sad", count: 5 },
    { name: "anger", count: 3 },
    { name: "surprise", count: 4 },
  ];

  const emotionRaw = kpis?.emotions || fallbackEmotions;
  const totalStudents = kpis?.totStudents || emotionRaw.reduce((acc, e) => acc + e.count, 0);

  const emotionData = emotionRaw.map((e) => {
    const meta = emotionMeta[e.name.toLowerCase()] || {
      label: e.name,
      color: "#9CA3AF",
      status: "Neutral",
    };
    return {
      ...e,
      label: meta.label,
      color: meta.color,
      percentage: totalStudents > 0 ? Math.round((e.count / totalStudents) * 100) : 0,
      status: meta.status,
    };
  });

  const chartData = emotionData.map(({ label, count, color }) => ({
    name: label,
    count,
    fill: color,
  }));

  const pieData = emotionData.map(({ label, percentage, color }) => ({
    name: label,
    value: percentage,
    color,
  }));

  const positive = emotionData.filter((e) => e.status === "Positive").reduce((acc, e) => acc + e.count, 0);
  const neutral = emotionData.filter((e) => e.status === "Neutral").reduce((acc, e) => acc + e.count, 0);
  const needsAttention = emotionData.filter((e) => e.status === "Needs Attention").reduce((acc, e) => acc + e.count, 0);

  const getActionRequired = (emotion: string) => {
    switch (emotion.toLowerCase()) {
      case "happy":
        return "Maintain positive environment";
      case "neutral":
        return "Monitor engagement";
      case "sad":
        return "Check student wellbeing";
      case "anger":
        return "Diffuse stress or conflict";
      case "surprise":
        return "Clarify confusing content";
      default:
        return "Monitor";
    }
  };

  const getStatusBadge = (status: string) => {
    const color = status === "Positive" ? "green" : status === "Neutral" ? "blue" : "red";
    return (
      <span className={`px-2 py-1 rounded-full text-xs font-medium bg-${color}-500/20 text-${color}-400`}>
        {status}
      </span>
    );
  };

  return (
    <main className="min-h-screen bg-gray-900 text-white p-6">
      {/* Header */}
      <div className="mb-6">
        <Link href="/dashboard" className="flex items-center gap-2 text-blue-400 hover:text-blue-300 transition-colors mb-4">
          <ArrowLeft className="w-4 h-4" />
          Back to Dashboard
        </Link>

        <div className="flex items-center gap-3 mb-2">
          <TrendingUp className="w-8 h-8 text-yellow-400" />
          <h1 className="text-3xl font-bold">Emotion Distribution</h1>
        </div>

        <p className="text-gray-400 max-w-3xl">
          Real-time emotion tracking of students to identify attention levels and engagement patterns.
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
          <div className="flex items-center gap-2 mb-2">
            <Smile className="w-5 h-5 text-green-400" />
            <span className="text-sm font-semibold text-green-400">Positive Emotions</span>
          </div>
          <div className="text-4xl font-bold text-white mb-1">{positive}</div>
          <p className="text-sm text-gray-400">Happy</p>
        </div>

        <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
          <div className="flex items-center gap-2 mb-2">
            <Users className="w-5 h-5 text-blue-400" />
            <span className="text-sm font-semibold text-blue-400">Neutral</span>
          </div>
          <div className="text-4xl font-bold text-white mb-1">{neutral}</div>
          <p className="text-sm text-gray-400">No strong reaction</p>
        </div>

        <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
          <div className="flex items-center gap-2 mb-2">
            <AlertTriangle className="w-5 h-5 text-yellow-400" />
            <span className="text-sm font-semibold text-yellow-400">Needs Attention</span>
          </div>
          <div className="text-4xl font-bold text-white mb-1">{needsAttention}</div>
          <p className="text-sm text-gray-400">Sad, Anger, Surprise</p>
        </div>

        <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
          <div className="flex items-center gap-2 mb-2">
            <TrendingUp className="w-5 h-5 text-cyan-400" />
            <span className="text-sm font-semibold text-cyan-400">Total Students</span>
          </div>
          <div className="text-4xl font-bold text-white mb-1">{totalStudents}</div>
          <p className="text-sm text-gray-400">Detected in frame</p>
        </div>
      </div>

      {/* Bar + Pie Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
          <h2 className="text-xl font-semibold mb-6">Emotion Distribution (Bar Chart)</h2>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis dataKey="name" stroke="#9CA3AF" />
                <YAxis stroke="#9CA3AF" />
                <Tooltip contentStyle={{ backgroundColor: '#1F2937', border: '1px solid #374151', borderRadius: '8px', color: '#ffffff' }} formatter={(value) => [value, 'Students']} />
                <Bar dataKey="count" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
          <h2 className="text-xl font-semibold mb-6">Emotion Distribution (Pie Chart)</h2>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={pieData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={100} label={({ name, value }) => `${name} ${value}%`}>
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ backgroundColor: '#1F2937', border: '1px solid #374151', borderRadius: '8px', color: '#ffffff' }} formatter={(value) => [`${value}%`, 'Percentage']} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Table */}
      <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
        <h2 className="text-xl font-semibold mb-6">Emotion Breakdown</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-gray-700">
                <th className="py-3 px-4 text-left font-medium text-gray-400">Emotion</th>
                <th className="py-3 px-4 text-left font-medium text-gray-400">Students</th>
                <th className="py-3 px-4 text-left font-medium text-gray-400">Percentage</th>
                <th className="py-3 px-4 text-left font-medium text-gray-400">Status</th>
                <th className="py-3 px-4 text-left font-medium text-gray-400">Action Required</th>
              </tr>
            </thead>
            <tbody>
              {emotionData.map((e, index) => (
                <tr key={index} className="border-b border-gray-700/50 hover:bg-gray-700/30">
                  <td className="py-3 px-4">{e.label}</td>
                  <td className="py-3 px-4 text-gray-300">{e.count} students</td>
                  <td className="py-3 px-4 text-white">{e.percentage}%</td>
                  <td className="py-3 px-4">{getStatusBadge(e.status)}</td>
                  <td className="py-3 px-4 text-gray-300">{getActionRequired(e.name)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </main>
  );
}
