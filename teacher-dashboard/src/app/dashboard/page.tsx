"use client";

import React, { useEffect, useState } from "react";
import { BentoGrid, BentoCard } from "@/components/magicui/bento-grid";
import KPIBox from "../../components/KPIBox";
import ChartBox from "../../components/ChartBox";
import TranscriptList from "../../components/TranscriptList";
import ConfigPanel from "../../components/ConfigPanel";
import VideoBox from "../../components/VideoBox";
import { Users, TrendingUp, Video, FileText, Eye } from "lucide-react";
import { useDashboardData } from "../../hooks/useDashboardData";
import { useRealTimeKPIs } from "../../hooks/useRealTimeKPIs";
import { useConfig } from "../../contexts/ConfigContext";
import SystemHealthMarquee from "@/components/SystemHealthMarquee";

export default function Dashboard() {
  const { data, loading, error } = useDashboardData();
  const { kpis: realTimeKPIs, loading: kpisLoading } = useRealTimeKPIs();
  const { config } = useConfig();
  const [hasLoadedOnce, setHasLoadedOnce] = useState(false);

  useEffect(() => {
    if (!loading && data) {
      setHasLoadedOnce(true);
    }
  }, [loading, data]);

  if (!hasLoadedOnce && loading) {
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

  // Use real-time KPIs if available, otherwise fall back to mock data
const attendanceKPI = {
    title: "Live Attendance",
    value: realTimeKPIs?.attendance.value || data.kpis.attendance.value,
    delta: realTimeKPIs?.attendance.delta || data.kpis.attendance.delta,
  icon: <Users />,
  accentColor: "text-emerald-400",
};

const engagementKPI = {
    title: "Live Engagement",
    value: realTimeKPIs?.engagement.value || data.kpis.engagement.value,
    delta: realTimeKPIs?.engagement.delta || data.kpis.engagement.delta,
  icon: <TrendingUp />,
  accentColor: "text-blue-400",
};

  // Additional KPI to show students in frame
  const studentsInFrameKPI = {
    title: "Students in Frame",
    value: realTimeKPIs ? `${realTimeKPIs.studentsInFrame}/${config.totalStudents}` : `${data.videoSession.studentsPresent}/${data.videoSession.totalStudents}`,
    delta: realTimeKPIs ? ((realTimeKPIs.studentsInFrame / config.totalStudents - 0.8) * 100) : 0,
    icon: <Eye />,
    accentColor: "text-cyan-400",
  };

  const features = [
    // KPI cards
    {
      Icon: Users,
      name: "Live Attendance",
      description: `Current attendance: ${attendanceKPI.value}`,
      href: "#attendance",
      cta: "View details",
      className: "col-span-1",
      background: <KPIBox {...attendanceKPI} />,
    },
    {
      Icon: TrendingUp,
      name: "Live Engagement",
      description: `Current engagement: ${engagementKPI.value}`,
      href: "#engagement",
      cta: "View details",
      className: "col-span-1",
      background: <KPIBox {...engagementKPI} />,
    },
    {
      Icon: Eye,
      name: "Students in Frame",
      description: `In frame: ${studentsInFrameKPI.value}`,
      href: "#students-in-frame",
      cta: "View details",
      className: "col-span-1",
      background: <KPIBox {...studentsInFrameKPI} />,
    },
    // Config Panel
    {
      Icon: ConfigPanel,
      name: "Config Panel",
      description: "Adjust class settings and preferences.",
      href: "#config",
      cta: "Configure",
      className: "col-span-1",
      background: <ConfigPanel />,
    },
    // Session Video (should take col2-col3)
    {
      Icon: Video,
      name: "Session Video",
      description: "Current session video and details.",
      href: "/session-videos",
      cta: "Watch",
      className: "col-span-2 row-span-2",
      background: <VideoBox {...data.videoSession} subject={config.currentSubject} />,
    },
    // Transcripts under Config Panel
    {
      Icon: FileText,
      name: "Transcripts",
      description: `Transcripts available: ${data.kpis.transcripts.value}`,
      href: "/transcripts",
      cta: "See all",
      className: "col-span-1",
      background: (<TranscriptList transcripts={data.transcripts.slice(0, 5)} />),
    },
    {
      Icon: TrendingUp,
      name: "Engagement Timeline",
      description: "Engagement over time.",
      href: "#chart1",
      cta: "See chart",
      className: "col-span-3 lg:col-span-2",
      background: <ChartBox type="line" data={data.charts.engagement} title="Engagement Timeline" dataKey="engagement" accentColor="#34d399" />,
    },
    {
      Icon: FileText,
      name: "Emotion Distribution",
      description: "Distribution of emotions detected.",
      href: "#chart2",
      cta: "See chart",
      className: "col-span-3 lg:col-span-2",
      background: <ChartBox type="bar" data={data.charts.emotions} title="Emotion Distribution" dataKey="count" accentColor="#f59e0b" />,
    },
  ];

  return (
    <main className="min-h-screen bg-gray-900 text-white p-6">
      {/* Real-time Status Bar */}
      <div className="mb-6 bg-gray-800 rounded-lg p-4 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <div className={`w-3 h-3 rounded-full ${realTimeKPIs && !kpisLoading ? 'bg-green-400 animate-pulse' : 'bg-gray-500'}`}></div>
            <span className="text-sm text-gray-300">
              {realTimeKPIs && !kpisLoading ? 'Live Analytics Active' : 'Loading Analytics...'}
            </span>
        </div>
          <div className="text-sm text-gray-400">
            Subject: <span className="text-white font-medium">{config.currentSubject}</span>
        </div>
          <div className="text-sm text-gray-400">
            Class Size: <span className="text-white font-medium">{config.totalStudents} students</span>
        </div>
        </div>
        {realTimeKPIs && (
          <div className="text-xs text-gray-400">
            Last updated: {new Date(realTimeKPIs.lastUpdated).toLocaleTimeString()}
        </div>
        )}
        </div>
      <BentoGrid>
        {features.map((feature, idx) => (
          <BentoCard key={idx} {...feature} />
        ))}
      </BentoGrid>
      
      {/* System Health Marquee at bottom */}
      <SystemHealthMarquee />
    </main>
  );
} 