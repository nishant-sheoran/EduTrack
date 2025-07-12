"use client";

import React from "react";
import { Marquee } from "@/components/magicui/marquee";
import { HardDrive, Cpu, CheckCircle, XCircle } from "lucide-react";
import { useSystemHealth } from "@/hooks/useSystemHealth";
import { cn } from "@/lib/utils";

const StatusCard = ({
  icon,
  label,
  value,
  color,
}: {
  icon: React.ReactNode;
  label: string;
  value: string;
  color: string;
}) => {
  return (
    <figure
      className={cn(
        "relative h-full w-64 cursor-pointer overflow-hidden rounded-xl border p-4",
        "border-gray-600 bg-gray-800 hover:bg-gray-700 transition-colors",
      )}
    >
      <div className="flex flex-row items-center gap-3">
        <div className="flex items-center justify-center w-8 h-8 rounded-full bg-gray-700">
          {icon}
        </div>
        <div className="flex flex-col">
          <figcaption className="text-sm font-medium text-white">
            {label}
          </figcaption>
          <p className={`text-xs font-medium ${color}`}>{value}</p>
        </div>
      </div>
    </figure>
  );
};

export default function SystemHealthMarquee() {
  const { health, loading } = useSystemHealth();

  if (loading || !health) {
    return (
      <div className="relative flex w-full flex-col items-center justify-center overflow-hidden bg-gray-900 py-6">
        <Marquee pauseOnHover className="[--duration:30s]">
          <StatusCard
            icon={<div className="w-4 h-4 bg-gray-500 rounded animate-pulse" />}
            label="Loading..."
            value="Please wait"
            color="text-gray-400"
          />
        </Marquee>
      </div>
    );
  }

  const statusCards = [
    {
      icon: health.apiStatus ? <CheckCircle className="w-4 h-4 text-green-400" /> : <XCircle className="w-4 h-4 text-red-400" />,
      label: "API Status",
      value: health.apiStatus ? "Online" : "Offline",
      color: health.apiStatus ? "text-green-400" : "text-red-400"
    },
    {
      icon: <HardDrive className="w-4 h-4 text-blue-400" />,
      label: "Disk Usage",
      value: `${health.diskUsage.toFixed(1)}%`,
      color: health.diskUsage > 80 ? "text-red-400" : health.diskUsage > 60 ? "text-yellow-400" : "text-green-400"
    },
    {
      icon: <Cpu className="w-4 h-4 text-purple-400" />,
      label: "Memory Usage",
      value: `${health.memoryUsage.toFixed(1)}%`,
      color: health.memoryUsage > 80 ? "text-red-400" : health.memoryUsage > 60 ? "text-yellow-400" : "text-green-400"
    }
  ];

  return (
    <div className="relative flex w-full flex-col items-center justify-center overflow-hidden bg-gray-900 py-6">
      <Marquee pauseOnHover className="[--duration:30s] [--gap:2rem]">
        {statusCards.map((card, index) => (
          <StatusCard key={index} {...card} />
        ))}
      </Marquee>
      <div className="pointer-events-none absolute inset-y-0 left-0 w-1/4 bg-gradient-to-r from-gray-900"></div>
      <div className="pointer-events-none absolute inset-y-0 right-0 w-1/4 bg-gradient-to-l from-gray-900"></div>
    </div>
  );
} 