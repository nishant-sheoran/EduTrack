"use client";

import React from "react";
import VideoBox from "@/components/VideoBox";

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
    <main className="min-h-screen bg-gray-900 text-white p-6 space-y-4">
      <h1 className="text-2xl font-semibold">Session Videos (Newest to Oldest)</h1>
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