"use client";

import React from "react";
import BentoGrid from "../../components/BentoGrid";
import KPIBox from "../../components/KPIBox";
import ChartBox from "../../components/ChartBox";
import SystemHealthPanel from "../../components/SystemHealthPanel";
import TranscriptList from "../../components/TranscriptList";
import ConfigPanel from "../../components/ConfigPanel";
import VideoBox from "../../components/VideoBox";
import { Users, TrendingUp, Video, FileText } from "lucide-react";
import { useDashboardData } from "../../hooks/useDashboardData";

export default function Dashboard() {
  const { data, loading, error } = useDashboardData();

  if (loading) {
    return (
      <main className="min-h-screen bg-gray-900 text-white p-6 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-400 mx-auto mb-4"></div>
          <p className="text-gray-400">Loading dashboard...</p>
        </div>
      </main>
    );
  }

  if (error) {
    return (
      <main className="min-h-screen bg-gray-900 text-white p-6 flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-400 mb-4">Error loading dashboard: {error}</p>
          <button 
            onClick={() => window.location.reload()} 
            className="px-4 py-2 bg-blue-600 hover:bg-blue-500 rounded-lg"
          >
            Retry
          </button>
        </div>
      </main>
    );
  }

  if (!data) {
    return (
      <main className="min-h-screen bg-gray-900 text-white p-6 flex items-center justify-center">
        <p className="text-gray-400">No data available</p>
      </main>
    );
  }

  const attendanceKPI = {
    title: "Attendance",
    value: data.kpis.attendance.value,
    delta: data.kpis.attendance.delta,
    icon: <Users />,
    accentColor: "text-emerald-400",
  };

  const engagementKPI = {
    title: "Engagement",
    value: data.kpis.engagement.value,
    delta: data.kpis.engagement.delta,
    icon: <TrendingUp />,
    accentColor: "text-blue-400",
  };

  const sessionsKPI = {
    title: "Sessions",
    value: data.kpis.sessions.value,
    delta: data.kpis.sessions.delta,
    icon: <Video />,
    accentColor: "text-purple-400",
  };

  const transcriptsKPI = {
    title: "Transcripts",
    value: data.kpis.transcripts.value,
    delta: data.kpis.transcripts.delta,
    icon: <FileText />,
    accentColor: "text-pink-400",
  };

  return (
    <main className="min-h-screen bg-gray-900 text-white p-6">
      <BentoGrid>
        {/* KPI 1 - Attendance */}
        <div className="md:[grid-area:kpi1] col-span-2 row-span-1">
          <KPIBox {...attendanceKPI} />
        </div>
        {/* KPI 2 - Engagement */}
        <div className="md:[grid-area:kpi2] col-span-2 row-span-1">
          <KPIBox {...engagementKPI} />
        </div>
        {/* Video */}
        <div className="md:[grid-area:video] col-span-2 row-span-1">
          <VideoBox {...data.videoSession} />
        </div>
        {/* Chart 1 - Engagement Timeline */}
        <div className="md:[grid-area:chart1] col-span-3 row-span-2">
          <ChartBox 
            type="line" 
            data={data.charts.engagement} 
            title="Engagement Timeline" 
            dataKey="engagement" 
            accentColor="#34d399" 
          />
        </div>
        {/* Chart 2 - Emotion Distribution */}
        <div className="md:[grid-area:chart2] col-span-3 row-span-2">
          <ChartBox 
            type="bar" 
            data={data.charts.emotions} 
            title="Emotion Distribution" 
            dataKey="count" 
            accentColor="#f59e0b" 
          />
        </div>
        {/* Transcripts */}
        <div className="md:[grid-area:transcripts] col-span-2 row-span-2">
          <TranscriptList transcripts={data.transcripts} />
        </div>
        {/* Config */}
        <div className="md:[grid-area:config] col-span-2 row-span-2">
          <ConfigPanel />
        </div>
        {/* System Health */}
        <div className="md:[grid-area:system] col-span-2 row-span-2">
          <SystemHealthPanel />
        </div>
      </BentoGrid>
    </main>
  );
} 