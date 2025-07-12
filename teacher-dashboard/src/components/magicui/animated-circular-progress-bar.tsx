"use client";

import React from "react";

interface AnimatedCircularProgressBarProps {
  className?: string;
  max?: number;
  min?: number;
  value?: number;
  gaugePrimaryColor?: string;
  gaugeSecondaryColor?: string;
}

export const AnimatedCircularProgressBar: React.FC<AnimatedCircularProgressBarProps> = ({
  className = "",
  max = 100,
  min = 0,
  value = 0,
  gaugePrimaryColor = "#4F46E5",
  gaugeSecondaryColor = "rgba(0,0,0,0.1)",
}) => {
  const radius = 48;
  const stroke = 10;
  const normalizedRadius = radius - stroke / 2;
  const circumference = normalizedRadius * 2 * Math.PI;
  const percent = Math.max(0, Math.min(1, (value - min) / (max - min)));
  const strokeDashoffset = circumference * (1 - percent);

  return (
    <div className={`flex flex-col items-center justify-center ${className}`} style={{ minWidth: 120, minHeight: 120 }}>
      <svg
        width={radius * 2}
        height={radius * 2}
        className="block"
      >
        <circle
          stroke={gaugeSecondaryColor}
          fill="transparent"
          strokeWidth={stroke}
          cx={radius}
          cy={radius}
          r={normalizedRadius}
        />
        <circle
          stroke={gaugePrimaryColor}
          fill="transparent"
          strokeWidth={stroke}
          strokeDasharray={circumference}
          strokeDashoffset={strokeDashoffset}
          strokeLinecap="round"
          cx={radius}
          cy={radius}
          r={normalizedRadius}
          style={{
            transition: "stroke-dashoffset 0.7s cubic-bezier(0.4,0,0.2,1)",
            transform: "rotate(-90deg)",
            transformOrigin: "50% 50%",
          }}
        />
      </svg>
      <span className="absolute text-2xl font-bold text-white mt-2">
        {Math.round(percent * 100)}%
      </span>
    </div>
  );
}; 