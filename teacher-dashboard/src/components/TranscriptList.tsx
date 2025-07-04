"use client";

import React from "react";
import { Download, FileText, Calendar, HardDrive } from "lucide-react";
import { useToast } from "../contexts/ToastContext";

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

export default function TranscriptList({ 
  transcripts = [
    {
      id: "1",
      name: "Mathematics_Lesson_01.pdf",
      date: "2024-01-15",
      size: "2.3 MB",
      url: "#",
      subject: "Mathematics"
    },
    {
      id: "2", 
      name: "Physics_Experiment_Notes.pdf",
      date: "2024-01-14",
      size: "1.8 MB",
      url: "#",
      subject: "Physics"
    },
    {
      id: "3",
      name: "Chemistry_Lab_Report.pdf", 
      date: "2024-01-13",
      size: "3.1 MB",
      url: "#",
      subject: "Chemistry"
    },
    {
      id: "4",
      name: "Biology_Discussion.pdf",
      date: "2024-01-12", 
      size: "2.7 MB",
      url: "#",
      subject: "Biology"
    }
  ]
}: TranscriptListProps) {
  const { showToast } = useToast();

  const handleDownload = (transcript: Transcript) => {
    // Placeholder download functionality
    console.log(`Downloading ${transcript.name}`);
    showToast({
      type: 'success',
      title: 'Download Started',
      message: `${transcript.name} is being downloaded...`,
    });
    // In real implementation, this would trigger actual download
  };

  return (
    <div className="bg-gray-800 rounded-xl p-4 shadow-lg flex flex-col h-full hover:shadow-xl transition-all duration-300">
      <div className="flex items-center gap-2 mb-3">
          <FileText className="w-4 h-4 text-blue-400" />
          <span className="text-sm font-semibold text-white">Transcripts</span>
      </div>

      <div className="flex-1 space-y-2 overflow-y-auto custom-scrollbar">
        {transcripts.length === 0 ? (
          <div className="flex items-center justify-center h-full">
            <span className="text-gray-400 text-xs text-center">
              No transcripts available
            </span>
          </div>
        ) : (
          transcripts.map((transcript) => (
            <div 
              key={transcript.id} 
              className="bg-gray-700 rounded-lg p-3 hover:bg-gray-600 transition-colors"
            >
              <div className="flex items-start justify-between gap-2">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <h4 className="text-xs font-medium text-white truncate">
                      {transcript.name.replace('.pdf', '').replace('_', ' ')}
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
                <button
                  onClick={() => handleDownload(transcript)}
                  className="p-2 rounded-lg bg-blue-600 hover:bg-blue-500 btn-interactive flex-shrink-0"
                  title={`Download ${transcript.name}`}
                >
                  <Download className="w-3 h-3 text-white" />
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
} 