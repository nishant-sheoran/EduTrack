"use client";

import React, { useEffect, useState } from "react";
import TranscriptList from "@/components/TranscriptList";
import { fetchDashboardData } from "@/lib/mockData";

interface Transcript {
  id: string;
  name: string;
  date: string;
  size: string;
  url: string;
  subject: string;
}

export default function TranscriptsPage() {
  const [transcripts, setTranscripts] = useState<Transcript[]>([]);
  const [selectedSubject, setSelectedSubject] = useState<string>("All");
  const [subjects, setSubjects] = useState<string[]>(["All"]);

  useEffect(() => {
    fetchDashboardData().then((data) => {
      setTranscripts(data.transcripts);
      const unique = Array.from(new Set(data.transcripts.map((t) => t.subject)));
      setSubjects(["All", ...unique]);
    });
  }, []);

  const filtered = selectedSubject === "All" ? transcripts : transcripts.filter((t) => t.subject === selectedSubject);

  return (
    <main className="min-h-screen bg-gray-900 text-white p-6 space-y-4">
      <h1 className="text-2xl font-semibold">All Transcripts</h1>
      <div className="flex items-center gap-2 mb-4">
        <label htmlFor="subject" className="text-sm">Filter by subject:</label>
        <select
          id="subject"
          value={selectedSubject}
          onChange={(e) => setSelectedSubject(e.target.value)}
          className="px-2 py-1 bg-gray-800 border border-gray-700 rounded text-white text-sm focus:outline-none"
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