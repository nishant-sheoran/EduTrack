"use client";

import React, { useEffect, useState } from "react";
import { BentoGrid, BentoCard } from "@/components/magicui/bento-grid";
import KPIBox from "../../components/KPIBox";
import ChartBox from "../../components/ChartBox";
import TranscriptList from "../../components/TranscriptList";
import ConfigPanel from "../../components/ConfigPanel";
import VideoBox from "../../components/VideoBox";
import { Users, TrendingUp, Video, FileText, Eye, BookOpen, Zap, Sparkles } from "lucide-react";
import { useDashboardData } from "../../hooks/useDashboardData";
import { useRealTimeKPIs } from "../../hooks/useRealTimeKPIs";
import { useConfig } from "../../contexts/ConfigContext";
import SystemHealthMarquee from "@/components/SystemHealthMarquee";
import { PulsatingButton } from "@/components/magicui/pulsating-button";
import { RippleButton } from "@/components/magicui/ripple-button";
import { ScratchToReveal } from "@/components/magicui/scratch-to-reveal";
import { BorderBeam } from "@/components/magicui/border-beam";
import { v4 as uuidv4 } from 'uuid';
import { useAnalyticsRecording } from "@/hooks/useAnalyticsRecording";

export default function Dashboard() {
  const { data, loading, error } = useDashboardData();
  const { kpis: realTimeKPIs } = useRealTimeKPIs();
  const { config, updateConfig, isAnalyticsActive, setIsAnalyticsActive } = useConfig();
  const [hasLoadedOnce, setHasLoadedOnce] = useState(false);
  const [showConfigMessage, setShowConfigMessage] = useState(false);
  const [popupStudents, setPopupStudents] = useState(config.classStrength);
  const [popupSubject, setPopupSubject] = useState(config.currentSubject);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const { sendAnalyticsState, recordingResult } = useAnalyticsRecording();
  const [sessionStartTime, setSessionStartTime] = useState<number | null>(null);
  const [sessionDuration, setSessionDuration] = useState<string>("00:00");
  const [lastRecordingResult, setLastRecordingResult] = useState<string | null>(null);

  // Replace your current useEffect with this:
  useEffect(() => {
    if (recordingResult?.videoUrl && recordingResult?.transcriptUrl) {
      console.log('Recording result has been updated:', {
        videoUrl: recordingResult.videoUrl,
        transcriptUrl: recordingResult.transcriptUrl
      });
      
      // Create a unique key to prevent duplicate updates
      const resultKey = `${recordingResult.videoUrl}-${recordingResult.transcriptUrl}`;
      
      // Only update if this is a new result
      if (lastRecordingResult !== resultKey) {
        setLastRecordingResult(resultKey);
        
        // Update config with the new URLs
        updateConfig({
          videoURL: recordingResult.videoUrl,
          transcriptURL: recordingResult.transcriptUrl
        });
      }
    }
  }, [recordingResult?.videoUrl, recordingResult?.transcriptUrl, lastRecordingResult, updateConfig]);

  useEffect(() => {
    if (!loading && data) {
      setHasLoadedOnce(true);
    }
  }, [loading, data]);

  const handleToggleAnalytics = () => {
    if (!isAnalyticsActive) {
      const newSessionId = `${uuidv4()}-${Date.now()}`;
      setSessionId(newSessionId);
  
      // Start session time
      setSessionStartTime(Date.now());
  
      // Set initial popup values
      setPopupStudents(config.classStrength);
      setPopupSubject(config.currentSubject);
      setShowConfigMessage(true);
  
      // Notify backend
      sendAnalyticsState('start', newSessionId);
    } else {
      setIsAnalyticsActive(false);
  
      if (sessionId && sessionStartTime) {
        const now = Date.now();
        const diffInMs = now - sessionStartTime;
        const totalSeconds = Math.floor(diffInMs / 1000);
        const minutes = Math.floor(totalSeconds / 60);
        const seconds = totalSeconds % 60;
  
        const formattedDuration = `${minutes.toString().padStart(2, '0')}:${seconds
          .toString()
          .padStart(2, '0')}`;
        setSessionDuration(formattedDuration);
  
        updateConfig({ studentAttendance: realTimeKPIs?.totStudents, session_duration: formattedDuration });
  
        sendAnalyticsState('stop', sessionId);
        
        setSessionId(null);
        setSessionStartTime(null); // reset start time
      }
    }
  };
  

  const handleApplySettings = () => {
    // Apply the settings from popup to main config
    updateConfig({
      classStrength: popupStudents,
      currentSubject: popupSubject
    });
    
    // Start analytics and close popup
    setIsAnalyticsActive(true);
    setShowConfigMessage(false);
  };

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

  // Use real-time KPIs only if analytics are active, otherwise use static values
  const attendanceKPI = {
    title: "Live Attendance",
    value: isAnalyticsActive ? (realTimeKPIs?.attendance.value || data.kpis.attendance.value) : data.kpis.attendance.value,
    delta: isAnalyticsActive ? (realTimeKPIs?.attendance.delta || data.kpis.attendance.delta) : 0,
    icon: <Users />,
    accentColor: "text-emerald-400",
  };

  const engagementKPI = {
    title: "Live Engagement",
    value: isAnalyticsActive ? (realTimeKPIs?.engagement.value || data.kpis.engagement.value) : data.kpis.engagement.value,
    delta: isAnalyticsActive ? (realTimeKPIs?.engagement.delta || data.kpis.engagement.delta) : 0,
    icon: <TrendingUp />,
    accentColor: "text-blue-400",
  };

  // Additional KPI to show students in frame
  const studentsInFrameKPI = {
    title: "Students in Frame",
    value: isAnalyticsActive ?
      (realTimeKPIs ? `${100}/${config.classStrength}` : `${data.videoSession.studentsPresent}/${config.classStrength}`) :
      `${data.videoSession.studentsPresent}/${data.videoSession.classStrength}`,
    delta: isAnalyticsActive ?
      (realTimeKPIs ? ((100 / config.classStrength - 0.8) * 100) : 0) :
      0,
    icon: <Eye />,
    accentColor: "text-cyan-400",
  };

  const features = [
    // KPI cards
    {
      Icon: Users,
      name: "Live Attendance",
      description: `${isAnalyticsActive ? 'Current' : 'Last'} attendance: ${attendanceKPI.value}`,
      href: "#attendance",
      cta: "View details",
      className: "col-span-1",
      background: <KPIBox {...attendanceKPI} />,
    },
    {
      Icon: TrendingUp,
      name: "Live Engagement",
      description: `${isAnalyticsActive ? 'Current' : 'Last'} engagement: ${engagementKPI.value}`,
      href: "#engagement",
      cta: "View details",
      className: "col-span-1",
      background: <KPIBox {...engagementKPI} />,
    },
    {
      Icon: Eye,
      name: "Students in Frame",
      description: `${isAnalyticsActive ? 'In frame' : 'Last count'}: ${studentsInFrameKPI.value}`,
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
      cta: "Watch all",
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
      description: "",
      href: "/engagement-timeline",
      cta: "See all",
      className: "col-span-1",
      background: <ChartBox
        type="line"
        data={data.charts.engagement}
        title="Engagement Timeline"
        dataKey="engagement"
        accentColor="#34d399"
        summaryValue="83%"
        summaryLabel="Avg Engagement"
        href="/engagement-timeline"
      />,
    },
    {
      Icon: Sparkles,
      name: "",
      description: "",
      href: "",
      cta: "",
      className: "col-span-1",
      background: (
        <div className="bg-gray-800 rounded-xl p-2 shadow-lg h-full flex items-center justify-center">
          <ScratchToReveal
            width={400}
            height={220}
            minScratchPercentage={70}
            className="flex items-center justify-center overflow-hidden rounded-lg"
            gradientColors={["#A97CF8", "#F38CB8", "#FDCC92"]}
          >
            <div className="text-center">
              <div className="text-6xl mb-2">🎉</div>
              <p className="text-lg font-bold text-white mb-1">Awesome Teaching!</p>
            </div>
          </ScratchToReveal>
        </div>
      ),
    },
    {
      Icon: FileText,
      name: "Emotion Distribution",
      description: "",
      href: "/emotion-distribution",
      cta: "See all",
      className: "col-span-1",
      background: <ChartBox
        type="bar"
        data={data.charts.emotions}
        title="Emotion Distribution"
        dataKey="count"
        accentColor="#f59e0b"
        summaryValue={realTimeKPIs?.totStudents?.toString() || "30"}
        href="/emotion-distribution"
      />,
    },
  ];

  return (
    <main className="min-h-screen bg-gray-900 text-white p-6">
      {/* Real-time Status Bar */}
      <div className="mb-6 bg-gray-800 rounded-lg p-4 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <div className={`w-3 h-3 rounded-full ${isAnalyticsActive ? 'bg-green-400 animate-pulse' : 'bg-red-500'}`}></div>
            <span className="text-sm text-gray-300">
              Live Analytics {isAnalyticsActive ? 'Active' : 'Inactive'}
            </span>
          </div>
          <div className="text-sm text-gray-400">
            Subject: <span className="text-white font-medium">{config.currentSubject}</span>
          </div>
          <div className="text-sm text-gray-400">
            Class Size: <span className="text-white font-medium">{config.classStrength} students</span>
          </div>
        </div>
        <div className="flex items-center gap-4">
          {realTimeKPIs && isAnalyticsActive && (
            <div className="text-xs text-gray-400">
              Last updated: {new Date(realTimeKPIs.lastUpdated).toLocaleTimeString()}
            </div>
          )}
          {isAnalyticsActive ? (
            <button
              onClick={handleToggleAnalytics}
              className="px-4 py-2 rounded-md text-sm font-medium transition-colors bg-red-500 hover:bg-red-600 text-white"
            >
              Stop
            </button>
          ) : (
            <PulsatingButton
              onClick={handleToggleAnalytics}
              className="bg-green-500 hover:bg-green-600 text-white border-green-500 hover:border-green-600 text-sm font-medium"
              pulseColor="#10b981"
              duration="2s"
            >
              Start
            </PulsatingButton>
          )}
        </div>
      </div>
      <BentoGrid>
        {features.map((feature, idx) => (
          <BentoCard key={idx} {...feature} />
        ))}
      </BentoGrid>
      
      {/* System Health Marquee at bottom */}
      <SystemHealthMarquee />
      
      {/* Live Settings Popup */}
      {showConfigMessage && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="relative bg-gray-800 p-6 rounded-lg max-w-md w-full mx-4 overflow-hidden">
            <div className="flex items-center gap-2 mb-4">
              <Zap className="w-5 h-5 text-emerald-400" />
              <h3 className="text-lg font-semibold text-emerald-400">Live Settings</h3>
            </div>
            
            <div className="space-y-4">
              {/* Students Input */}
              <div className="space-y-2">
                <label className="flex items-center gap-2 text-sm font-medium text-white">
                  <Users className="w-4 h-4" />
                  Students ({popupStudents})
                </label>
                <input
                  type="number"
                  value={popupStudents}
                  onChange={(e) => setPopupStudents(parseInt(e.target.value) || 0)}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white text-sm focus:outline-none focus:border-emerald-400"
                  min="1"
                  max="200"
                  placeholder="Enter number of students"
                />
              </div>

              {/* Subject Dropdown */}
              <div className="space-y-2">
                <label className="flex items-center gap-2 text-sm font-medium text-white">
                  <BookOpen className="w-4 h-4" />
                  Subject
                </label>
                <select
                  value={popupSubject}
                  onChange={(e) => setPopupSubject(e.target.value)}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white text-sm focus:outline-none focus:border-emerald-400"
                >
                  <option value="Mathematics">Mathematics</option>
                  <option value="Physics">Physics</option>
                  <option value="Chemistry">Chemistry</option>
                  <option value="Biology">Biology</option>
                  <option value="English">English</option>
                  <option value="History">History</option>
                  <option value="Geography">Geography</option>
                  <option value="Computer Science">Computer Science</option>
                  <option value="Other">Other</option>
                </select>
              </div>
            </div>

            <div className="flex gap-3 mt-6">
              <button
                onClick={() => setShowConfigMessage(false)}
                className="flex-1 px-4 py-2 bg-gray-600 hover:bg-gray-500 rounded-lg text-white text-sm transition-colors"
              >
                Cancel
              </button>
              <RippleButton
                onClick={handleApplySettings}
                className="flex-1 bg-emerald-600 hover:bg-emerald-500 text-white border-emerald-600 hover:border-emerald-500 text-sm font-medium"
                rippleColor="#ffffff"
                duration="600ms"
              >
                <div className="flex items-center justify-center gap-2">
                  <span>Apply & Start</span>
                </div>
              </RippleButton>
            </div>
            <BorderBeam
              duration={6}
              size={400}
              className="from-transparent via-emerald-500 to-transparent"
            />
            <BorderBeam
              duration={6}
              delay={3}
              size={400}
              borderWidth={2}
              className="from-transparent via-purple-500 to-transparent"
            />
          </div>
        </div>
      )}
    </main>
  );
}