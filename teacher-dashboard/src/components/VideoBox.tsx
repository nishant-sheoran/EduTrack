"use client";

import React, { useState, useRef } from "react";
import { Play, Calendar, Clock, Users, BookOpen, Eye, Maximize, Pause, X } from "lucide-react";
import { RippleButton } from "./magicui/ripple-button";

interface VideoBoxProps {
  sessionDate?: string;
  duration?: string;
  studentsPresent?: number;
  totalStudents?: number;
  topics?: string[];
  subject?: string;
  videoUrl?: string;
}

export default function VideoBox({
  sessionDate = "2024-01-15",
  duration = "45:30",
  studentsPresent = 28,
  totalStudents = 30,
  topics = ["Algebra", "Quadratic Equations", "Problem Solving"],
  subject = "Mathematics",
  videoUrl = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"
}: VideoBoxProps) {
  const [isPlaying, setIsPlaying] = useState(false);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [hasError, setHasError] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const videoRef = useRef<HTMLVideoElement>(null);

  const handlePlayPause = async () => {
    if (videoRef.current && !hasError) {
      try {
        setIsLoading(true);
        if (isPlaying) {
          videoRef.current.pause();
          setIsPlaying(false);
        } else {
          await videoRef.current.play();
          setIsPlaying(true);
        }
      } catch (error) {
        console.warn('Error playing video:', error);
        setHasError(true);
        setIsPlaying(false);
      } finally {
        setIsLoading(false);
      }
    }
  };

  const handleFullscreen = () => {
    setIsFullscreen(true);
    if (videoRef.current) {
      if (videoRef.current.requestFullscreen) {
        videoRef.current.requestFullscreen();
      }
    }
  };

  const handleExitFullscreen = async () => {
    setIsFullscreen(false);
    try {
      if (document.fullscreenElement && document.exitFullscreen) {
        await document.exitFullscreen();
      }
    } catch (error) {
      console.warn('Error exiting fullscreen:', error);
      // Fallback: just update the state
      setIsFullscreen(false);
    }
  };

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
        {/* Video Player */}
        <div className="relative bg-gray-900 rounded-lg overflow-hidden aspect-video cursor-pointer">
          <video
            ref={videoRef}
            className="w-full h-full object-cover"
            poster=""
            onPlay={() => setIsPlaying(true)}
            onPause={() => setIsPlaying(false)}
            onEnded={() => setIsPlaying(false)}
            onError={(e) => {
              console.warn('Video error:', e);
              setHasError(true);
              setIsPlaying(false);
              setIsLoading(false);
            }}
            onLoadStart={() => setIsLoading(true)}
            onLoadedData={() => setIsLoading(false)}
            onWaiting={() => setIsLoading(true)}
            onCanPlay={() => setIsLoading(false)}
          >
            <source src={videoUrl} type="video/mp4" />
            Your browser does not support the video tag.
          </video>
          
          {/* Play Button Overlay */}
          {!isPlaying && (
            <div 
              className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-40 hover:bg-opacity-60 transition-all"
              onClick={!hasError ? handlePlayPause : undefined}
            >
              <div className="text-center">
                {hasError ? (
                  <>
                    <X className="w-12 h-12 text-red-400 mx-auto mb-2" />
                    <p className="text-red-400 text-sm">Video unavailable</p>
                    <p className="text-gray-400 text-xs mt-1">Demo content</p>
                  </>
                ) : isLoading ? (
                  <>
                    <div className="w-12 h-12 border-2 border-white border-t-transparent rounded-full animate-spin mx-auto mb-2"></div>
                    <p className="text-white text-sm">Loading...</p>
                  </>
                ) : (
                  <>
                    <Play className="w-12 h-12 text-white mx-auto mb-2 hover:scale-110 transition-transform" />
                    <p className="text-white text-sm">Play Session</p>
                  </>
                )}
              </div>
            </div>
          )}

          {/* Video Controls Overlay */}
          {isPlaying && (
            <div className="absolute inset-0 bg-black bg-opacity-0 hover:bg-opacity-30 transition-all group">
              <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                <button
                  onClick={handlePlayPause}
                  className="p-3 rounded-full bg-black bg-opacity-50 hover:bg-opacity-70 transition-all"
                >
                  <Pause className="w-8 h-8 text-white" />
                </button>
              </div>
            </div>
          )}

          {/* Duration Badge */}
          <div className="absolute bottom-2 right-2 bg-black bg-opacity-70 px-2 py-1 rounded text-xs text-white">
            {duration}
          </div>

          {/* Fullscreen Exit Button (only visible in fullscreen) */}
          {isFullscreen && (
            <button
              onClick={handleExitFullscreen}
              className="absolute top-4 right-4 p-2 rounded-full bg-black bg-opacity-50 hover:bg-opacity-70 transition-all"
            >
              <X className="w-6 h-6 text-white" />
            </button>
          )}
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
          <RippleButton 
            onClick={!hasError ? handleFullscreen : undefined}
            className={`w-full text-xs font-medium mt-2 ${
              hasError 
                ? "bg-gray-600 text-gray-400 cursor-not-allowed border-gray-600" 
                : "bg-purple-600 hover:bg-purple-500 text-white border-purple-600 hover:border-purple-500"
            }`}
            rippleColor={hasError ? "#666666" : "#ffffff"}
            duration="600ms"
          >
            <div className="flex items-center justify-center gap-2">
              <Maximize className="w-3 h-3" />
              <span>{hasError ? "Demo Content" : "View Fullscreen"}</span>
            </div>
          </RippleButton>
        </div>
      </div>
    </div>
  );
} 