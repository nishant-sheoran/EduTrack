"use client";

import React, { useState } from "react";
import TranscriptList from "@/components/TranscriptList";
import { ArrowLeft, FileText } from "lucide-react";
import Link from "next/link";

// Static data for testing
const staticTranscripts = [
  {
    id: "t1",
    name: "Mathematics Lecture - Algebra Basics",
    date: "2024-01-15",
    size: "2.3 MB",
    url: "#",
    subject: "Mathematics",
  },
  {
    id: "t2", 
    name: "Physics Class - Thermodynamics",
    date: "2024-01-14",
    size: "1.8 MB", 
    url: "#",
    subject: "Physics",
  },
  {
    id: "t3",
    name: "Chemistry Lab - Organic Reactions", 
    date: "2024-01-13",
    size: "3.1 MB",
    url: "#", 
    subject: "Chemistry",
  },
  {
    id: "t4",
    name: "History Discussion - World War II",
    date: "2024-01-12", 
    size: "2.7 MB",
    url: "#",
    subject: "History",
  },
];

export default function TranscriptsPage() {
  const [selectedSubject, setSelectedSubject] = useState<string>("All");
  const subjects = ["All", "Mathematics", "Physics", "Chemistry", "History"];

  const filtered = selectedSubject === "All" ? staticTranscripts : staticTranscripts.filter((t) => t.subject === selectedSubject);

  return (
    <main className="min-h-screen bg-gray-900 text-white p-6">
      {/* Header */}
      <div className="mb-6">
        <Link href="/dashboard" className="flex items-center gap-2 text-blue-400 hover:text-blue-300 transition-colors mb-4">
          <ArrowLeft className="w-4 h-4" />
          Back to Dashboard
        </Link>
        
        <div className="flex items-center gap-3 mb-2">
          <FileText className="w-8 h-8 text-green-400" />
          <h1 className="text-3xl font-bold">Transcripts</h1>
        </div>
        
        <p className="text-gray-400">
          Access all session transcripts organized by subject. Download, review, and analyze class discussions and content.
        </p>
      </div>
      
      {/* Filter Controls */}
      <div className="flex items-center gap-2 mb-6">
        <label htmlFor="subject" className="text-sm font-medium">Filter by subject:</label>
        <select
          id="subject"
          value={selectedSubject}
          onChange={(e) => setSelectedSubject(e.target.value)}
          className="px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white text-sm focus:outline-none focus:border-green-400 transition-colors"
        >
          {subjects.map((s) => (
            <option key={s} value={s}>{s}</option>
          ))}
        </select>
      </div>
      
      <TranscriptList transcripts={filtered} />
    </main>
  );
} 