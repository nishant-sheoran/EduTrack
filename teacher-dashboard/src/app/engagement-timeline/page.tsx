"use client";

import React from "react";
import { ArrowLeft, TrendingUp, Calendar, Users, BarChart3 } from "lucide-react";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts";
import Link from "next/link";

// Sample data for the engagement timeline
const engagementData = [
  { day: "Mon", date: "29/06/2025", engagement: 80, students: 21, duration: "43 min", status: "Good" },
  { day: "Tue", date: "30/06/2025", engagement: 85, students: 26, duration: "36 min", status: "Excellent" },
  { day: "Wed", date: "01/07/2025", engagement: 78, students: 22, duration: "48 min", status: "Good" },
  { day: "Thu", date: "02/07/2025", engagement: 90, students: 25, duration: "58 min", status: "Excellent" },
  { day: "Fri", date: "03/07/2025", engagement: 88, students: 23, duration: "31 min", status: "Excellent" },
  { day: "Sat", date: "04/07/2025", engagement: 82, students: 22, duration: "32 min", status: "Good" },
  { day: "Sun", date: "05/07/2025", engagement: 75, students: 26, duration: "39 min", status: "Good" },
];

const chartData = [
  { name: "Mon", engagement: 80 },
  { name: "Tue", engagement: 85 },
  { name: "Wed", engagement: 78 },
  { name: "Thu", engagement: 90 },
  { name: "Fri", engagement: 88 },
  { name: "Sat", engagement: 82 },
  { name: "Sun", engagement: 75 },
];

export default function EngagementTimelinePage() {
  // Calculate average engagement
  const avgEngagement = Math.round(engagementData.reduce((sum, item) => sum + item.engagement, 0) / engagementData.length);
  
  // Find peak day
  const peakDay = engagementData.reduce((max, item) => item.engagement > max.engagement ? item : max, engagementData[0]);
  
  // Calculate average students per session
  const avgStudents = Math.round(engagementData.reduce((sum, item) => sum + item.students, 0) / engagementData.length);

  return (
    <main className="min-h-screen bg-gray-900 text-white p-6">
      {/* Header */}
      <div className="mb-6">
        <Link href="/dashboard" className="flex items-center gap-2 text-blue-400 hover:text-blue-300 transition-colors mb-4">
          <ArrowLeft className="w-4 h-4" />
          Back to Dashboard
        </Link>
        
        <div className="flex items-center gap-3 mb-2">
          <TrendingUp className="w-8 h-8 text-green-400" />
          <h1 className="text-3xl font-bold">Engagement Timeline</h1>
        </div>
        
        <p className="text-gray-400 max-w-2xl">
          Track student engagement patterns over time. Monitor trends, identify peak engagement
          periods, and understand what teaching methods work best for your class.
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
          <div className="flex items-center gap-2 mb-2">
            <TrendingUp className="w-5 h-5 text-green-400" />
            <span className="text-sm font-semibold text-green-400">Average Engagement</span>
          </div>
          <div className="text-4xl font-bold text-white mb-1">{avgEngagement}%</div>
          <p className="text-sm text-gray-400">Last 7 days</p>
        </div>
        
        <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
          <div className="flex items-center gap-2 mb-2">
            <Calendar className="w-5 h-5 text-blue-400" />
            <span className="text-sm font-semibold text-blue-400">Peak Day</span>
          </div>
          <div className="text-4xl font-bold text-white mb-1">{peakDay.day}</div>
          <p className="text-sm text-gray-400">Highest engagement</p>
        </div>
        
        <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
          <div className="flex items-center gap-2 mb-2">
            <Users className="w-5 h-5 text-cyan-400" />
            <span className="text-sm font-semibold text-cyan-400">Active Students</span>
          </div>
          <div className="text-4xl font-bold text-white mb-1">{avgStudents}</div>
          <p className="text-sm text-gray-400">Average per session</p>
        </div>
      </div>

      {/* Chart */}
      <div className="bg-gray-800 rounded-xl p-6 border border-gray-700 mb-8">
        <h2 className="text-xl font-semibold mb-6">Engagement Over Time</h2>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartData}>
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
                formatter={(value) => [`${value}%`, 'Engagement']}
                labelFormatter={(label) => `${label} - 02/07/2025`}
              />
              <Line 
                type="monotone" 
                dataKey="engagement" 
                stroke="#10B981" 
                strokeWidth={3}
                dot={{ fill: '#10B981', strokeWidth: 2, r: 6 }}
                activeDot={{ r: 8, fill: '#10B981' }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Daily Breakdown Table */}
      <div className="bg-gray-800 rounded-xl p-6 border border-gray-700 mb-8">
        <h2 className="text-xl font-semibold mb-6">Daily Breakdown</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-gray-700">
                <th className="text-left py-3 px-4 font-medium text-gray-400">Day</th>
                <th className="text-left py-3 px-4 font-medium text-gray-400">Date</th>
                <th className="text-left py-3 px-4 font-medium text-gray-400">Engagement</th>
                <th className="text-left py-3 px-4 font-medium text-gray-400">Students</th>
                <th className="text-left py-3 px-4 font-medium text-gray-400">Duration</th>
                <th className="text-left py-3 px-4 font-medium text-gray-400">Status</th>
              </tr>
            </thead>
            <tbody>
              {engagementData.map((item, index) => (
                <tr key={index} className="border-b border-gray-700/50 hover:bg-gray-700/30">
                  <td className="py-3 px-4 font-medium text-white">{item.day}</td>
                  <td className="py-3 px-4 text-gray-300">{item.date}</td>
                  <td className="py-3 px-4">
                    <div className="flex items-center gap-2">
                      <div className="w-16 h-2 bg-gray-700 rounded-full overflow-hidden">
                        <div 
                          className="h-full bg-green-500 rounded-full" 
                          style={{ width: `${item.engagement}%` }}
                        />
                      </div>
                      <span className="text-white font-medium">{item.engagement}%</span>
                    </div>
                  </td>
                  <td className="py-3 px-4 text-gray-300">{item.students} students</td>
                  <td className="py-3 px-4 text-gray-300">{item.duration}</td>
                  <td className="py-3 px-4">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      item.status === 'Excellent' ? 'bg-green-500/20 text-green-400' : 'bg-blue-500/20 text-blue-400'
                    }`}>
                      {item.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Insights & Recommendations */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
          <h3 className="text-lg font-semibold text-green-400 mb-4">Positive Trends</h3>
          <ul className="space-y-2 text-sm text-gray-300">
            <li>• Engagement peaks on Thursdays (90%)</li>
            <li>• Consistent attendance above 80%</li>
            <li>• Strong student participation in interactive sessions</li>
          </ul>
        </div>
        
        <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
          <h3 className="text-lg font-semibold text-amber-400 mb-4">Areas for Improvement</h3>
          <ul className="space-y-2 text-sm text-gray-300">
            <li>• Wednesday sessions show lower engagement (78%)</li>
            <li>• Consider more interactive activities mid-week</li>
            <li>• Review content difficulty for better engagement</li>
          </ul>
        </div>
      </div>
    </main>
  );
} 