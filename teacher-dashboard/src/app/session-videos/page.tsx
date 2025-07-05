"use client";

import React from "react";
import VideoBox from "@/components/VideoBox";
import { ArrowLeft, Video } from "lucide-react";
import Link from "next/link";

interface VideoData {
  id: string;
  sessionDate: string;
  duration: string;
  studentsPresent: number;
  totalStudents: number;
  topics: string[];
  videoUrl: string;
  subject: string;
  disengagement: number; // higher means more disengaged
}

const videos: VideoData[] = [
  {
    id: "v1",
    sessionDate: "2024-01-15",
    duration: "45:30",
    studentsPresent: 28,
    totalStudents: 30,
    topics: ["Algebra", "Quadratic Equations"],
    videoUrl: "#",
    subject: "Mathematics",
    disengagement: 35,
  },
  {
    id: "v2",
    sessionDate: "2024-01-14",
    duration: "40:10",
    studentsPresent: 25,
    totalStudents: 30,
    topics: ["Thermodynamics"],
    videoUrl: "#",
    subject: "Physics",
    disengagement: 50,
  },
  {
    id: "v3",
    sessionDate: "2024-01-13",
    duration: "42:05",
    studentsPresent: 29,
    totalStudents: 30,
    topics: ["Organic Chemistry", "Reactions"],
    videoUrl: "#",
    subject: "Chemistry",
    disengagement: 20,
  },
  {
    id: "v4",
    sessionDate: "2024-01-12",
    duration: "38:45",
    studentsPresent: 22,
    totalStudents: 30,
    topics: ["World War II"],
    videoUrl: "#",
    subject: "History",
    disengagement: 60,
  },
];

export default function SessionVideosPage() {
  // Sort videos by newest first (sessionDate descending)
  const sortedVideos = [...videos].sort((a, b) => new Date(b.sessionDate).getTime() - new Date(a.sessionDate).getTime());

  return (
    <main className="min-h-screen bg-gray-900 text-white p-6">
      {/* Header */}
      <div className="mb-6">
        <Link href="/dashboard" className="flex items-center gap-2 text-blue-400 hover:text-blue-300 transition-colors mb-4">
          <ArrowLeft className="w-4 h-4" />
          Back to Dashboard
        </Link>
        
        <div className="flex items-center gap-3 mb-2">
          <Video className="w-8 h-8 text-red-400" />
          <h1 className="text-3xl font-bold">Session Videos</h1>
        </div>
        
        <p className="text-gray-400">
          Browse all recorded session videos, sorted from newest to oldest. Monitor student engagement and review class performance.
        </p>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {sortedVideos.map((video) => (
          <VideoBox
            key={video.id}
            sessionDate={video.sessionDate}
            duration={video.duration}
            studentsPresent={video.studentsPresent}
            totalStudents={video.totalStudents}
            topics={video.topics}
            subject={video.subject}
          />
        ))}
      </div>
    </main>
  );
} 