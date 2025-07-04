import React from "react";
import "../styles/bento-grid.css";

interface BentoGridProps {
  children?: React.ReactNode;
}

export default function BentoGrid({ children }: BentoGridProps) {
  return (
    <div className="bento-grid-areas grid grid-cols-1 auto-rows-min gap-4 w-full h-full
      md:grid-cols-6 md:grid-rows-4 md:[grid-template-areas:'kpi1_kpi1_kpi2_kpi2_video_video''chart1_chart1_chart1_chart2_chart2_chart2''transcripts_transcripts_config_config_system_system''transcripts_transcripts_config_config_system_system']
    ">
      {children}
    </div>
  );
} 