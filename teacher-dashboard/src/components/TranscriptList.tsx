"use client";

import React, { useMemo } from "react";
import { Download, FileText, Calendar, HardDrive } from "lucide-react";
import { useToast } from "../contexts/ToastContext";
import { RippleButton } from "./magicui/ripple-button";
import { useConfig } from "../contexts/ConfigContext";

interface Transcript {
  id: string;
  name: string;
  date: string;
  size: string;
  url: string;
  subject: string;
}

interface TranscriptListProps {
  transcripts?: Transcript[];
}

// Mock data can be kept for development or as a fallback
const mockTranscripts: Transcript[] = [
  {
    id: "1",
    name: "Mathematics_Lesson_01.pdf",
    date: "2025-07-10",
    size: "2.3 MB",
    url: "#",
    subject: "Mathematics",
  },
  {
    id: "2",
    name: "Physics_Experiment_Notes.pdf",
    date: "2025-07-09",
    size: "1.8 MB",
    url: "#",
    subject: "Physics",
  },
];

// Helper to format bytes into a readable string
const formatBytes = (bytes: number, decimals = 2) => {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
};

export default function TranscriptList({ transcripts = [] }: TranscriptListProps) {
  const { showToast } = useToast();
  const { config } = useConfig();

  // useMemo will re-calculate the list only when config or props change
  const allTranscripts = useMemo(() => {
    const realTranscripts: Transcript[] = [];

    // Check for a valid transcript URL from the config
    if (config.transcriptURL && !config.transcriptURL.includes('path/to/transcript')) {
      realTranscripts.push({
        id: "real-time-session",
        name: config.transcriptURL.split("/").pop() || "Session_Transcript.pdf",
        date: new Date().toISOString().slice(0, 10),
        size: "Fetching...", // We can't know the size yet
        url: config.transcriptURL,
        subject: config.currentSubject,
      });
    }

    // Combine the real transcript with provided or mock transcripts
    return [...realTranscripts, ...(transcripts.length > 0 ? transcripts : mockTranscripts)];
  }, [config.transcriptURL, config.currentSubject, transcripts]);

  const handleDownload = async (transcript: Transcript) => {
    // Prevent download for placeholder URLs
    if (transcript.url === "#") {
      showToast({
        type: 'error',
        title: 'Download Unavailable',
        message: 'This is a mock transcript and cannot be downloaded.',
      });
      return;
    }

    showToast({
      type: 'info',
      title: 'Preparing Download',
      message: `Fetching ${transcript.name}...`,
    });

    try {
      // Fetch the file from the URL as a blob (binary data)
      const response = await fetch(transcript.url);
      if (!response.ok) {
        throw new Error(`Failed to fetch file: ${response.statusText}`);
      }
      const blob = await response.blob();

      // Create a temporary URL for the blob
      const blobUrl = window.URL.createObjectURL(blob);

      // Create a temporary link to trigger the download
      const link = document.createElement("a");
      link.href = blobUrl;
      link.download = transcript.name;
      document.body.appendChild(link);
      link.click();

      // Clean up by removing the link and revoking the blob URL
      document.body.removeChild(link);
      window.URL.revokeObjectURL(blobUrl);

      showToast({
        type: "success",
        title: "Download Started",
        message: `${transcript.name} (${formatBytes(blob.size)}) is downloading.`,
      });
    } catch (error) {
      console.error("Download failed:", error);
      showToast({
        type: "error",
        title: "Download Failed",
        message: "Could not download the transcript. See console for details.",
      });
    }
  };

  return (
    <div className="bg-gray-800 rounded-xl p-4 shadow-lg flex flex-col h-full hover:shadow-xl transition-all duration-300">
      <div className="flex items-center gap-2 mb-3">
        <FileText className="w-4 h-4 text-blue-400" />
        <span className="text-sm font-semibold text-white">Transcripts</span>
      </div>

      <div className="flex-1 space-y-2 overflow-y-auto custom-scrollbar">
        {allTranscripts.length === 0 ? (
          <div className="flex items-center justify-center h-full">
            <span className="text-gray-400 text-xs text-center">No transcripts available</span>
          </div>
        ) : (
          allTranscripts.map((transcript) => (
            <div
              key={transcript.id}
              className="bg-gray-700 rounded-lg p-3 hover:bg-gray-600 transition-colors"
            >
              <div className="flex items-start justify-between gap-2">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <h4 className="text-xs font-medium text-white truncate" title={transcript.name}>
                      {transcript.name.replace(".pdf", "").replace(/_/g, " ")}
                    </h4>
                    <span className="px-2 py-0.5 bg-blue-600 text-xs text-white rounded flex-shrink-0">
                      {transcript.subject}
                    </span>
                  </div>
                  <div className="flex items-center gap-3 text-xs text-gray-400">
                    <div className="flex items-center gap-1">
                      <Calendar className="w-3 h-3" />
                      <span>{transcript.date}</span>
                    </div>
                    <div className="flex items-center gap-1">
                      <HardDrive className="w-3 h-3" />
                      <span>{transcript.size}</span>
                    </div>
                  </div>
                </div>
                <RippleButton
                  onClick={() => handleDownload(transcript)}
                  className="bg-blue-600 hover:bg-blue-500 text-white border-blue-600 hover:border-blue-500 flex-shrink-0"
                  rippleColor="#ffffff"
                  duration="600ms"
                  title={`Download ${transcript.name}`}
                >
                  <Download className="w-3 h-3 text-white" />
                </RippleButton>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}