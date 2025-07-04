"use client";

import React from "react";
import { Play, Calendar, Clock, Users, BookOpen, Eye } from "lucide-react";

interface VideoBoxProps {
  sessionDate?: string;
  duration?: string;
  studentsPresent?: number;
  totalStudents?: number;
  topics?: string[];
  subject?: string;
}

export default function VideoBox({
  sessionDate = "2024-01-15",
  duration = "45:30",
  studentsPresent = 28,
  totalStudents = 30,
  topics = ["Algebra", "Quadratic Equations", "Problem Solving"],
  subject = "Mathematics"
}: VideoBoxProps) {
  return (
    <div className="bg-gray-800 rounded-xl p-4 shadow-lg flex flex-col h-full hover:shadow-xl transition-all duration-300">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <Play className="w-4 h-4 text-red-400" />
          <span className="text-sm font-semibold text-white">Latest Session</span>
        </div>
        <span className="px-2 py-1 bg-blue-600 text-xs text-white rounded-full">{subject}</span>
      </div>

      <div className="flex-1 space-y-3">
        {/* Video Placeholder */}
        <div className="relative bg-gray-900 rounded-lg overflow-hidden aspect-video">
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="text-center">
              <Play className="w-8 h-8 text-gray-400 mx-auto mb-1" />
              <p className="text-gray-400 text-xs">Session Video</p>
            </div>
          </div>
          <div className="absolute bottom-2 right-2 bg-black bg-opacity-70 px-2 py-1 rounded text-xs text-white">
            {duration}
          </div>
        </div>

        {/* Session Details */}
        <div className="space-y-2 text-xs">
          {/* Date and Duration */}
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-1 text-gray-300">
              <Calendar className="w-3 h-3" />
              <span>{sessionDate}</span>
            </div>
            <div className="flex items-center gap-1 text-gray-300">
              <Clock className="w-3 h-3" />
              <span>{duration}</span>
            </div>
          </div>

          {/* Students Present */}
          <div className="flex items-center gap-2">
            <Users className="w-3 h-3 text-blue-400" />
            <span className="text-white text-xs">
              {studentsPresent}/{totalStudents} students
            </span>
            <span className="text-gray-400 text-xs">
              ({Math.round((studentsPresent / totalStudents) * 100)}%)
            </span>
          </div>

          {/* Topics Covered */}
          <div className="space-y-1">
            <div className="flex items-center gap-1">
              <BookOpen className="w-3 h-3 text-green-400" />
              <span className="text-white font-medium text-xs">Topics:</span>
            </div>
            <div className="flex flex-wrap gap-1">
              {topics.slice(0, 2).map((topic, index) => (
                <span
                  key={index}
                  className="px-2 py-0.5 bg-gray-700 text-xs text-gray-300 rounded"
                >
                  {topic}
                </span>
              ))}
              {topics.length > 2 && (
                <span className="px-2 py-0.5 bg-gray-700 text-xs text-gray-300 rounded">
                  +{topics.length - 2}
                </span>
              )}
            </div>
          </div>

          {/* View Session Button */}
          <button className="w-full flex items-center justify-center gap-2 px-3 py-2 bg-red-600 hover:bg-red-500 rounded-lg text-white text-xs btn-interactive mt-2">
            <Eye className="w-3 h-3" />
            View Session
          </button>
        </div>
      </div>
    </div>
  );
} 