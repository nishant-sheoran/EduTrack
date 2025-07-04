import React from "react";
import "../styles/bento-grid.css";

interface BentoGridProps {
  children?: React.ReactNode;
}

export default function BentoGrid({ children }: BentoGridProps) {
  return (
    <div className="bento-grid">
      {children}
    </div>
  );
} 