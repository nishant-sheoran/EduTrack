"use client";

import React, { useState, useRef, useEffect } from "react";
import { Play, Calendar, Clock, Users, BookOpen, Maximize, Pause, X, FileText, Download } from "lucide-react";
import { RippleButton } from "./magicui/ripple-button";
import { useConfig } from "@/contexts/ConfigContext";

interface VideoBoxProps {
  sessionDate?: string;
  duration?: string;
  studentsPresent?: number;
  totalStudents?: number;
  subject?: string;
  videoUrl?: string; // This prop can override the one from context
}

export default function VideoBox({
  sessionDate,
  duration,
  studentsPresent,
  totalStudents,
  subject,
  videoUrl,
}: VideoBoxProps) {
  const [isPlaying, setIsPlaying] = useState(false);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [hasError, setHasError] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const videoRef = useRef<HTMLVideoElement>(null);
  const { config } = useConfig();

  // **CORRECTED**: Use props first, then config, then a default.
  const finalSubject = subject ?? config.currentSubject ?? "Not Set";
  const finalStudentsPresent = studentsPresent ?? config.studentAttendance ?? 0;
  const finalTotalStudents = totalStudents ?? config.classStrength ?? 0;
  const finalDuration = duration ?? config.session_duration ?? "00:00";
  
  // **FIX**: Only use videoUrl prop if it's a valid URL (not "#" or default values)
  const isValidVideoUrl = (url: string | undefined): boolean => {
    return !!(url && url !== '#' && url !== 'path/to/video' && url.startsWith('http'));
  };
  
  const finalVideoURL = isValidVideoUrl(videoUrl) ? videoUrl : 
                       isValidVideoUrl(config.videoURL) ? config.videoURL : 
                       null;
  
  const finalTranscriptURL = config.transcriptURL;

  // **ADD DEBUG LOGGING**
  console.log('VideoBox Debug:', {
    finalVideoURL,
    finalTranscriptURL,
    hasError,
    isLoading,
    configVideoURL: config.videoURL,
    propVideoUrl: videoUrl,
    isValidPropUrl: isValidVideoUrl(videoUrl),
    isValidConfigUrl: isValidVideoUrl(config.videoURL)
  });

  // **CORRECTED**: Properly format the date
  const displayDate = new Date(sessionDate ?? Date.now()).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });

  // Effect to check if the video URL is valid when it changes
  useEffect(() => {
    console.log('VideoBox useEffect triggered:', { finalVideoURL });
    
    if (!finalVideoURL) {
      console.log('No valid video URL available');
      setHasError(true);
      setIsLoading(false);
    } else {
      console.log('Video URL looks valid, resetting states');
      setHasError(false);
      setIsLoading(true); // Reset loading state when new URL is provided
      
      // **ADD**: Test if the video URL is actually accessible
      const testVideo = document.createElement('video');
      testVideo.src = finalVideoURL;
      testVideo.onloadedmetadata = () => {
        console.log('Video URL test successful');
        setIsLoading(false);
      };
      testVideo.onerror = (e) => {
        console.error('Video URL test failed:', e);
        setHasError(true);
        setIsLoading(false);
      };
    }
  }, [finalVideoURL]);

  // **ADD**: Missing functions
  const handlePlayPause = () => {
    if (videoRef.current) {
      if (isPlaying) {
        videoRef.current.pause();
      } else {
        videoRef.current.play();
      }
    }
  };

  const handleFullscreen = () => {
    if (videoRef.current) {
      if (videoRef.current.requestFullscreen) {
        videoRef.current.requestFullscreen();
        setIsFullscreen(true);
      }
    }
  };

  const handleExitFullscreen = () => {
    if (document.exitFullscreen) {
      document.exitFullscreen();
      setIsFullscreen(false);
    }
  };

  // **ADD**: Additional video event handlers for debugging
  const handleVideoError = (e: React.SyntheticEvent<HTMLVideoElement, Event>) => {
    console.error('Video error:', e);
    const video = e.currentTarget;
    console.error('Video error details:', {
      networkState: video.networkState,
      readyState: video.readyState,
      error: video.error
    });
    setHasError(true);
    setIsLoading(false);
  };

  const handleVideoLoadStart = () => {
    console.log('Video load start');
    setIsLoading(true);
  };

  const handleVideoLoadedData = () => {
    console.log('Video loaded data');
    setIsLoading(false);
  };

  const handleVideoCanPlay = () => {
    console.log('Video can play');
    setIsLoading(false);
  };

  // **ADD**: Listen for fullscreen changes
  useEffect(() => {
    const handleFullscreenChange = () => {
      setIsFullscreen(!!document.fullscreenElement);
    };

    document.addEventListener('fullscreenchange', handleFullscreenChange);
    return () => {
      document.removeEventListener('fullscreenchange', handleFullscreenChange);
    };
  }, []);

  return (
    <div className="bg-gray-800 rounded-xl p-4 shadow-lg flex flex-col h-full hover:shadow-xl transition-all duration-300">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <Play className="w-4 h-4 text-red-400" />
          <span className="text-sm font-semibold text-white">Latest Session</span>
        </div>
        <span className="px-2 py-1 bg-blue-600 text-xs text-white rounded-full">{finalSubject}</span>
      </div>

      <div className="flex-1 space-y-3">
        {/* Video Player */}
        <div className="relative bg-gray-900 rounded-lg overflow-hidden aspect-video cursor-pointer">
          {/* **ADD**: Debug info overlay */}
          {process.env.NODE_ENV === 'development' && (
            <div className="absolute top-2 left-2 bg-black bg-opacity-70 text-white text-xs p-2 rounded z-10">
              URL: {finalVideoURL || 'No valid URL'}<br/>
              Error: {hasError ? 'Yes' : 'No'}<br/>
              Loading: {isLoading ? 'Yes' : 'No'}
            </div>
          )}
          
          {/* **CONDITIONAL**: Only render video if we have a valid URL */}
          {finalVideoURL && (
            <video
              ref={videoRef}
              className="w-full h-full object-contain"
              onPlay={() => setIsPlaying(true)}
              onPause={() => setIsPlaying(false)}
              onEnded={() => setIsPlaying(false)}
              onError={handleVideoError}
              onLoadStart={handleVideoLoadStart}
              onLoadedData={handleVideoLoadedData}
              onCanPlay={handleVideoCanPlay}
              // **CHANGED**: Use key to force re-render when src changes
              key={finalVideoURL}
              preload="metadata"
            >
              {/* **CORRECTED**: Use the finalVideoURL variable */}
              <source src={finalVideoURL} type="video/mp4" />
              Your browser does not support the video tag.
            </video>
          )}
          
          {/* Overlay */}
          {!isPlaying && (
            <div
              className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-40 hover:bg-opacity-60 transition-all"
              onClick={!hasError && finalVideoURL ? handlePlayPause : undefined}
            >
              <div className="text-center">
                {hasError || !finalVideoURL ? (
                  <>
                    <X className="w-12 h-12 text-red-400 mx-auto mb-2" />
                    <p className="text-red-400 text-sm">Video Unavailable</p>
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
          
          {/* Controls */}
          {isPlaying && !hasError && finalVideoURL && (
             <div className="absolute inset-0 bg-black bg-opacity-0 hover:bg-opacity-30 transition-all group" onClick={handlePlayPause}>
                <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                    <button className="p-3 rounded-full bg-black bg-opacity-50 hover:bg-opacity-70">
                        <Pause className="w-8 h-8 text-white" />
                    </button>
                </div>
            </div>
          )}

          {/* Duration Badge */}
          <div className="absolute bottom-2 right-2 bg-black bg-opacity-70 px-2 py-1 rounded text-xs text-white">
            {finalDuration}
          </div>

          {/* Fullscreen Exit Button */}
          {isFullscreen && (
            <button
              onClick={handleExitFullscreen}
              className="absolute top-2 right-2 p-2 rounded-full bg-black bg-opacity-50 hover:bg-opacity-70"
            >
              <X className="w-5 h-5 text-white" />
            </button>
          )}
        </div>

        {/* Session Details */}
        <div className="space-y-2 text-xs">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-1 text-gray-300">
              <Calendar className="w-3 h-3" />
              <span>{displayDate}</span>
            </div>
            <div className="flex items-center gap-1 text-gray-300">
              <Clock className="w-3 h-3" />
              <span>{finalDuration}</span>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <Users className="w-3 h-3 text-blue-400" />
            {/* **CORRECTED**: Use final variables for consistency */}
            <span className="text-white text-xs">
              {finalStudentsPresent}/{finalTotalStudents} students
            </span>
            <span className="text-gray-400 text-xs">
              ({finalTotalStudents > 0 ? Math.round((finalStudentsPresent / finalTotalStudents) * 100) : 0}%)
            </span>
          </div>

          {/* **NEW**: Transcript and Fullscreen Buttons in a grid */}
          <div className="grid grid-cols-3 gap-2 pt-1">
             <a
                href={finalTranscriptURL}
                target="_blank"
                rel="noopener noreferrer"
                className={`flex items-center justify-center gap-2 text-xs font-medium py-2 rounded-lg transition-all ${
                    !finalTranscriptURL || hasError
                    ? "bg-gray-600 text-gray-400 cursor-not-allowed"
                    : "bg-teal-600 hover:bg-teal-500 text-white"
                }`}
            >
                <FileText className="w-3 h-3" />
                <span>Transcript</span>
            </a>
            {/* Download Button */}
           <a
             href={finalVideoURL || '#'}
             download
              onClick={(e) => {
                if (!finalVideoURL || hasError) {
                  e.preventDefault();
                }
              }}
              className={`flex items-center justify-center gap-2 text-xs font-medium py-2 rounded-lg transition-all ${
                !finalVideoURL || hasError
                  ? "bg-gray-600 text-gray-400 cursor-not-allowed"
                  : "bg-green-600 hover:bg-green-500 text-white"
              }`}
            >
              <Download className="w-3 h-3" />
              <span>Download</span>
            </a>
            <RippleButton
              onClick={!hasError && finalVideoURL ? handleFullscreen : undefined}
              className={`w-full text-xs font-medium ${
                hasError || !finalVideoURL
                  ? "bg-gray-600 text-gray-400 cursor-not-allowed border-gray-600"
                  : "bg-purple-600 hover:bg-purple-500 text-white border-purple-600"
              }`}
            >
              <div className="flex items-center justify-center gap-2">
                <Maximize className="w-3 h-3" />
                <span>Fullscreen</span>
              </div>
            </RippleButton>
          </div>
        </div>
      </div>
    </div>
  );
}