import axios from 'axios';

export interface DashboardData {
  kpis: {
    attendance: { value: string; delta: number };
    engagement: { value: string; delta: number };
    sessions: { value: string; delta: number };
    transcripts: { value: string; delta: number };
  };
  charts: {
    engagement: Array<{ name: string; engagement: number }>;
    emotions: Array<{ name:string; count: number }>;
    attendance: Array<{ name: string; attendance: number }>;
    performance: Array<{ name: string; score: number }>;
  };
  transcripts: Array<{
    id: string;
    name: string;
    date: string;
    size: string;
    url: string;
    subject: string;
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
    classStrength: number;
    videoUrl: string;
    subject: string;
  };
  realTimeEngagement: {
    totalStudents: number,
    lastUpdated: string;
    detectedFaces: Array<{
      id: number;
      engagement: string;
      emotion: string;
      timestamp: string;
    }>;
  };
}

export const mockDashboardData: DashboardData = {
  kpis: {
    sessions: { value: "156", delta: 8.5 },
    transcripts: { value: "89", delta: 12.3 },
    attendance: { value: "0%", delta: 0 }, 
    engagement: { value: "0%", delta: 0 }, 
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
      subject: "Mathematics",
    },
    {
      id: "2",
      name: "Physics_Experiment_Notes.pdf",
      date: "2024-01-14",
      size: "1.8 MB",
      url: "#",
      subject: "Physics",
    },
    {
      id: "3",
      name: "Chemistry_Lab_Report.pdf",
      date: "2024-01-13",
      size: "3.1 MB",
      url: "#",
      subject: "Chemistry",
    },
    {
      id: "4",
      name: "Biology_Discussion.pdf",
      date: "2024-01-12",
      size: "2.7 MB",
      url: "#",
      subject: "Biology",
    },
    {
      id: "5",
      name: "English_Literature_Analysis.pdf",
      date: "2024-01-11",
      size: "1.5 MB",
      url: "#",
      subject: "English",
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
    classStrength: 30,
    videoUrl: "#",
    subject: "Mathematics",
  },
  realTimeEngagement: {
    totalStudents: 0,
    lastUpdated: new Date().toISOString(),
    detectedFaces: [],
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

interface RealtimeData {
  present_ids: number[];
  engagement: Array<{
    id: string;
    emotion: string;
    engagement: string;
  }>;
}

// Fetch real-time engagement data from the FastAPI server
export const fetchRealTimeEngagement = async (): Promise<DashboardData['realTimeEngagement']> => {
  try {
    const response = await axios.get<RealtimeData>('http://127.0.0.1:8001/api/classroom/realtime');
    const data = response.data;

    console.log("API engagement response:", data.engagement);

    const totalStudents = data.present_ids?.length || 0;
    const lastUpdated = new Date().toISOString();

    const detectedFaces = data.engagement.map((face) => ({
      id: Number(face.id),
      engagement: face.engagement.toLowerCase(), // "engaged" or "disengaged"
      emotion: face.emotion,
      timestamp: new Date().toISOString(),
    }));

    return {
      totalStudents,
      lastUpdated,
      detectedFaces,
    };

  } catch (error) {
    console.error("Error fetching real-time engagement data:", error);
    return {
      totalStudents: 0,
      lastUpdated: new Date().toISOString(),
      detectedFaces: [],
    };
  }
};


// Calculate real-time KPIs based on class size and detected students
export const calculateRealTimeKPIs = (
  classStrength: number,
  totalStudents: DashboardData['realTimeEngagement']['totalStudents'],
  detectedFaces: DashboardData['realTimeEngagement']['detectedFaces']
) => {
  // Calculate attendance percentage
  const attendancePercentage = classStrength > 0 ? Math.min((totalStudents / classStrength) * 100, 100) : 0;
  
  // Calculate average engagement from detected faces
  const avgEngagement = (() => {
    const engagedCount = detectedFaces.filter(face => face.engagement === "engaged").length;
    return totalStudents > 0 ? (engagedCount / totalStudents) * 100 : 0;
  })();

  return {
    attendance: {
      value: `${attendancePercentage.toFixed(1)}%`,
      delta: Math.random() * 10 - 5, // Random delta for demo
    },
    engagement: {
      value: `${avgEngagement.toFixed(1)}%`,
      delta: Math.random() * 10 - 5, // Random delta for demo
    },
  };
};

export const calculateEmotionChartData = (
  detectedFaces: DashboardData['realTimeEngagement']['detectedFaces']
): DashboardData['charts']['emotions'] => {
  const emotionCountMap: Record<string, number> = {};

  detectedFaces.forEach((face) => {
    const emotion = face.emotion.toLowerCase(); // normalize casing
    emotionCountMap[emotion] = (emotionCountMap[emotion] || 0) + 1;
  });

  return Object.entries(emotionCountMap).map(([name, count]) => ({ name, count }));
};

