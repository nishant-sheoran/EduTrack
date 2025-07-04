"use client";

import React from "react";
import { Play, Calendar, Clock, Users, BookOpen, Eye } from "lucide-react";

interface VideoBoxProps {
  sessionDate?: string;
  duration?: string;
  studentsPresent?: number;
  totalStudents?: number;
  topics?: string[];
  videoUrl?: string;
}

export default function VideoBox({
  sessionDate = "2024-01-15",
  duration = "45:30",
  studentsPresent = 28,
  totalStudents = 30,
  topics = ["Algebra", "Quadratic Equations", "Problem Solving"],
  videoUrl = "#"
}: VideoBoxProps) {
  return (
    <div className="bg-gray-800 rounded-xl p-6 shadow-lg flex flex-col h-full">
      <div className="flex items-center gap-2 mb-4">
        <Play className="w-5 h-5 text-red-400" />
        <span className="text-lg font-semibold text-white">Latest Session</span>
      </div>

      <div className="flex-1 space-y-4">
        {/* Video Placeholder */}
        <div className="relative bg-gray-900 rounded-lg overflow-hidden aspect-video">
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="text-center">
              <Play className="w-12 h-12 text-gray-400 mx-auto mb-2" />
              <p className="text-gray-400 text-sm">Session Video</p>
            </div>
          </div>
          <div className="absolute bottom-2 right-2 bg-black bg-opacity-70 px-2 py-1 rounded text-xs text-white">
            {duration}
          </div>
        </div>

        {/* Session Details */}
        <div className="space-y-3">
          {/* Date and Duration */}
          <div className="flex items-center justify-between text-sm">
            <div className="flex items-center gap-2 text-gray-300">
              <Calendar className="w-4 h-4" />
              <span>{sessionDate}</span>
            </div>
            <div className="flex items-center gap-2 text-gray-300">
              <Clock className="w-4 h-4" />
              <span>{duration}</span>
            </div>
          </div>

          {/* Students Present */}
          <div className="flex items-center gap-2 text-sm">
            <Users className="w-4 h-4 text-blue-400" />
            <span className="text-white">
              {studentsPresent}/{totalStudents} students present
            </span>
            <span className="text-gray-400">
              ({Math.round((studentsPresent / totalStudents) * 100)}%)
            </span>
          </div>

          {/* Topics Covered */}
          <div className="space-y-2">
            <div className="flex items-center gap-2 text-sm">
              <BookOpen className="w-4 h-4 text-green-400" />
              <span className="text-white font-medium">Topics Covered:</span>
            </div>
            <div className="flex flex-wrap gap-2">
              {topics.map((topic, index) => (
                <span
                  key={index}
                  className="px-2 py-1 bg-gray-700 text-xs text-gray-300 rounded-full"
                >
                  {topic}
                </span>
              ))}
            </div>
          </div>

          {/* View Session Button */}
          <button className="w-full flex items-center justify-center gap-2 px-4 py-2 bg-red-600 hover:bg-red-500 rounded-lg text-white font-medium btn-interactive">
            <Eye className="w-4 h-4" />
            View Full Session
          </button>
        </div>
      </div>
    </div>
  );
} 