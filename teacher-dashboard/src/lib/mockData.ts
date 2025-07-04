export interface DashboardData {
  kpis: {
    attendance: { value: string; delta: number };
    engagement: { value: string; delta: number };
    sessions: { value: string; delta: number };
    transcripts: { value: string; delta: number };
  };
  charts: {
    engagement: Array<{ name: string; engagement: number }>;
    emotions: Array<{ name: string; count: number }>;
    attendance: Array<{ name: string; attendance: number }>;
    performance: Array<{ name: string; score: number }>;
  };
  transcripts: Array<{
    id: string;
    name: string;
    date: string;
    size: string;
    url: string;
  }>;
  systemHealth: {
    apiStatus: boolean;
    diskUsage: number;
    memoryUsage: number;
    systemMessages: string[];
  };
  videoSession: {
    sessionDate: string;
    duration: string;
    studentsPresent: number;
    totalStudents: number;
    topics: string[];
    videoUrl: string;
  };
}

export const mockDashboardData: DashboardData = {
  kpis: {
    attendance: { value: "92.5%", delta: 2.1 },
    engagement: { value: "87.3%", delta: -1.2 },
    sessions: { value: "156", delta: 8.5 },
    transcripts: { value: "89", delta: 12.3 },
  },
  charts: {
    engagement: [
      { name: "Mon", engagement: 80 },
      { name: "Tue", engagement: 85 },
      { name: "Wed", engagement: 78 },
      { name: "Thu", engagement: 90 },
      { name: "Fri", engagement: 88 },
      { name: "Sat", engagement: 82 },
      { name: "Sun", engagement: 75 },
    ],
    emotions: [
      { name: "Happy", count: 15 },
      { name: "Neutral", count: 8 },
      { name: "Confused", count: 3 },
      { name: "Bored", count: 2 },
      { name: "Excited", count: 12 },
    ],
    attendance: [
      { name: "Week 1", attendance: 95 },
      { name: "Week 2", attendance: 92 },
      { name: "Week 3", attendance: 88 },
      { name: "Week 4", attendance: 94 },
      { name: "Week 5", attendance: 91 },
    ],
    performance: [
      { name: "Quiz 1", score: 85 },
      { name: "Quiz 2", score: 78 },
      { name: "Quiz 3", score: 92 },
      { name: "Quiz 4", score: 88 },
      { name: "Quiz 5", score: 95 },
    ],
  },
  transcripts: [
    {
      id: "1",
      name: "Mathematics_Lesson_01.pdf",
      date: "2024-01-15",
      size: "2.3 MB",
      url: "#",
    },
    {
      id: "2",
      name: "Physics_Experiment_Notes.pdf",
      date: "2024-01-14",
      size: "1.8 MB",
      url: "#",
    },
    {
      id: "3",
      name: "Chemistry_Lab_Report.pdf",
      date: "2024-01-13",
      size: "3.1 MB",
      url: "#",
    },
    {
      id: "4",
      name: "Biology_Discussion.pdf",
      date: "2024-01-12",
      size: "2.7 MB",
      url: "#",
    },
    {
      id: "5",
      name: "English_Literature_Analysis.pdf",
      date: "2024-01-11",
      size: "1.5 MB",
      url: "#",
    },
  ],
  systemHealth: {
    apiStatus: true,
    diskUsage: 65.2,
    memoryUsage: 48.7,
    systemMessages: [
      "Session recording completed successfully",
      "Transcript generation completed",
      "High CPU usage detected during video processing",
      "Backup scheduled for tonight at 2:00 AM",
      "System update available",
    ],
  },
  videoSession: {
    sessionDate: "2024-01-15",
    duration: "45:30",
    studentsPresent: 28,
    totalStudents: 30,
    topics: ["Algebra", "Quadratic Equations", "Problem Solving"],
    videoUrl: "#",
  },
};

// Simulate API delay
export const fetchDashboardData = (): Promise<DashboardData> => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(mockDashboardData);
    }, 500);
  });
};

export const fetchSystemHealth = (): Promise<DashboardData['systemHealth']> => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(mockDashboardData.systemHealth);
    }, 300);
  });
}; 