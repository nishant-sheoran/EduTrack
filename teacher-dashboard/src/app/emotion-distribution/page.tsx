"use client";

import React from "react";
import { ArrowLeft, Smile, Users, AlertTriangle, TrendingUp } from "lucide-react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, PieChart, Pie, Cell } from "recharts";
import Link from "next/link";

// Sample data for emotion distribution
const emotionData = [
  { emotion: "Happy", count: 15, percentage: 38, color: "#10B981", status: "Positive" },
  { emotion: "Excited", count: 12, percentage: 30, color: "#3B82F6", status: "Positive" },
  { emotion: "Neutral", count: 8, percentage: 20, color: "#6B7280", status: "Neutral" },
  { emotion: "Confused", count: 3, percentage: 8, color: "#F59E0B", status: "Needs Attention" },
  { emotion: "Bored", count: 2, percentage: 5, color: "#EF4444", status: "Needs Attention" },
];

const chartData = [
  { name: "Happy", count: 15, fill: "#10B981" },
  { name: "Neutral", count: 8, fill: "#6B7280" },
  { name: "Confused", count: 3, fill: "#F59E0B" },
  { name: "Bored", count: 2, fill: "#EF4444" },
  { name: "Excited", count: 12, fill: "#3B82F6" },
];

const pieData = [
  { name: "Happy", value: 38, color: "#10B981" },
  { name: "Excited", value: 30, color: "#3B82F6" },
  { name: "Neutral", value: 20, color: "#6B7280" },
  { name: "Confused", value: 8, color: "#F59E0B" },
  { name: "Bored", value: 5, color: "#EF4444" },
];

export default function EmotionDistributionPage() {
  const totalStudents = 40;
  const positiveEmotions = emotionData.filter(e => e.status === "Positive").reduce((sum, item) => sum + item.count, 0);
  const neutralEmotions = emotionData.filter(e => e.status === "Neutral").reduce((sum, item) => sum + item.count, 0);
  const needsAttention = emotionData.filter(e => e.status === "Needs Attention").reduce((sum, item) => sum + item.count, 0);

  const getEmotionIcon = (emotion: string) => {
    switch (emotion) {
      case "Happy": return <div className="w-3 h-3 bg-green-500 rounded-full" />;
      case "Excited": return <div className="w-3 h-3 bg-blue-500 rounded-full" />;
      case "Neutral": return <div className="w-3 h-3 bg-gray-500 rounded-full" />;
      case "Confused": return <div className="w-3 h-3 bg-yellow-500 rounded-full" />;
      case "Bored": return <div className="w-3 h-3 bg-red-500 rounded-full" />;
      default: return <div className="w-3 h-3 bg-gray-500 rounded-full" />;
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "Positive":
        return <span className="px-2 py-1 rounded-full text-xs font-medium bg-green-500/20 text-green-400">Positive</span>;
      case "Neutral":
        return <span className="px-2 py-1 rounded-full text-xs font-medium bg-blue-500/20 text-blue-400">Neutral</span>;
      case "Needs Attention":
        return <span className="px-2 py-1 rounded-full text-xs font-medium bg-red-500/20 text-red-400">Needs Attention</span>;
      default:
        return null;
    }
  };

  const getActionRequired = (emotion: string) => {
    switch (emotion) {
      case "Happy":
        return "Maintain positive environment";
      case "Excited":
        return "Channel enthusiasm into learning";
      case "Neutral":
        return "Monitor for engagement opportunities";
      case "Confused":
        return "Provide clarification and support";
      case "Bored":
        return "Increase interactivity and engagement";
      default:
        return "Monitor closely";
    }
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
          Analyze student emotional states during class. Understand engagement levels, identify
          students who need attention, and track emotional patterns to improve teaching effectiveness.
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
          <div className="flex items-center gap-2 mb-2">
            <Smile className="w-5 h-5 text-green-400" />
            <span className="text-sm font-semibold text-green-400">Positive Emotions</span>
          </div>
          <div className="text-4xl font-bold text-white mb-1">{positiveEmotions}</div>
          <p className="text-sm text-gray-400">Happy + Excited</p>
        </div>
        
        <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
          <div className="flex items-center gap-2 mb-2">
            <Users className="w-5 h-5 text-blue-400" />
            <span className="text-sm font-semibold text-blue-400">Neutral</span>
          </div>
          <div className="text-4xl font-bold text-white mb-1">{neutralEmotions}</div>
          <p className="text-sm text-gray-400">Standard attention</p>
        </div>
        
        <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
          <div className="flex items-center gap-2 mb-2">
            <AlertTriangle className="w-5 h-5 text-yellow-400" />
            <span className="text-sm font-semibold text-yellow-400">Needs Attention</span>
          </div>
          <div className="text-4xl font-bold text-white mb-1">{needsAttention}</div>
          <p className="text-sm text-gray-400">Confused + Bored</p>
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

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {/* Bar Chart */}
        <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
          <h2 className="text-xl font-semibold mb-6">Emotion Distribution (Bar Chart)</h2>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis dataKey="name" stroke="#9CA3AF" />
                <YAxis stroke="#9CA3AF" />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: '#1F2937', 
                    border: '1px solid #374151',
                    borderRadius: '8px',
                    color: '#ffffff'
                  }}
                  formatter={(value) => [value, 'Students']}
                />
                <Bar dataKey="count" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Pie Chart */}
        <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
          <h2 className="text-xl font-semibold mb-6">Emotion Distribution (Pie Chart)</h2>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={pieData}
                  dataKey="value"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  outerRadius={100}
                  label={({ name, value }) => `${name} ${value}%`}
                >
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: '#1F2937', 
                    border: '1px solid #374151',
                    borderRadius: '8px',
                    color: '#ffffff'
                  }}
                  formatter={(value) => [`${value}%`, 'Percentage']}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Emotion Breakdown Table */}
      <div className="bg-gray-800 rounded-xl p-6 border border-gray-700 mb-8">
        <h2 className="text-xl font-semibold mb-6">Emotion Breakdown</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-gray-700">
                <th className="text-left py-3 px-4 font-medium text-gray-400">Emotion</th>
                <th className="text-left py-3 px-4 font-medium text-gray-400">Students</th>
                <th className="text-left py-3 px-4 font-medium text-gray-400">Percentage</th>
                <th className="text-left py-3 px-4 font-medium text-gray-400">Status</th>
                <th className="text-left py-3 px-4 font-medium text-gray-400">Action Required</th>
              </tr>
            </thead>
            <tbody>
              {emotionData.map((item, index) => (
                <tr key={index} className="border-b border-gray-700/50 hover:bg-gray-700/30">
                  <td className="py-3 px-4">
                    <div className="flex items-center gap-2">
                      {getEmotionIcon(item.emotion)}
                      <span className="font-medium text-white">{item.emotion}</span>
                    </div>
                  </td>
                  <td className="py-3 px-4 text-gray-300">{item.count} students</td>
                  <td className="py-3 px-4">
                    <div className="flex items-center gap-2">
                      <div className="w-20 h-2 bg-gray-700 rounded-full overflow-hidden">
                        <div 
                          className="h-full rounded-full" 
                          style={{ 
                            width: `${item.percentage}%`,
                            backgroundColor: item.color
                          }}
                        />
                      </div>
                      <span className="text-white font-medium">{item.percentage}%</span>
                    </div>
                  </td>
                  <td className="py-3 px-4">
                    {getStatusBadge(item.status)}
                  </td>
                  <td className="py-3 px-4 text-gray-300">
                    {getActionRequired(item.emotion)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Teaching Recommendations */}
      <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
        <h2 className="text-xl font-semibold mb-6">Teaching Recommendations</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 className="text-lg font-semibold text-green-400 mb-4">Positive Indicators</h3>
            <ul className="space-y-2 text-sm text-gray-300">
              <li>• 67.5% of students show positive emotions (Happy + Excited)</li>
              <li>• Strong engagement with current teaching methods</li>
              <li>• Good classroom atmosphere and student participation</li>
            </ul>
          </div>
          
          <div>
            <h3 className="text-lg font-semibold text-amber-400 mb-4">Areas for Improvement</h3>
            <ul className="space-y-2 text-sm text-gray-300">
              <li>• 12.5% of students are confused - need clarification</li>
              <li>• 5% of students appear bored - increase interactivity</li>
              <li>• Consider breaking down complex concepts further</li>
            </ul>
          </div>
        </div>
      </div>
    </main>
  );
} 