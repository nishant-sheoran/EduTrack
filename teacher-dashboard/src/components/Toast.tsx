"use client";

import React, { useEffect } from 'react';
import { CheckCircle, XCircle, AlertTriangle, Info, X } from 'lucide-react';

export interface ToastProps {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  title: string;
  message?: string;
  duration?: number;
  onDismiss: (id: string) => void;
}

const toastStyles = {
  success: {
    bg: 'bg-emerald-600',
    border: 'border-emerald-500',
    icon: CheckCircle,
    iconColor: 'text-emerald-400',
  },
  error: {
    bg: 'bg-red-600',
    border: 'border-red-500',
    icon: XCircle,
    iconColor: 'text-red-400',
  },
  warning: {
    bg: 'bg-yellow-600',
    border: 'border-yellow-500',
    icon: AlertTriangle,
    iconColor: 'text-yellow-400',
  },
  info: {
    bg: 'bg-blue-600',
    border: 'border-blue-500',
    icon: Info,
    iconColor: 'text-blue-400',
  },
};

export default function Toast({ id, type, title, message, duration = 5000, onDismiss }: ToastProps) {
  const style = toastStyles[type];
  const Icon = style.icon;

  useEffect(() => {
    const timer = setTimeout(() => {
      onDismiss(id);
    }, duration);

    return () => clearTimeout(timer);
  }, [id, duration, onDismiss]);

  return (
    <div
      className={`${style.bg} ${style.border} border rounded-lg p-4 shadow-lg max-w-sm w-full transform transition-all duration-300 ease-in-out`}
    >
      <div className="flex items-start gap-3">
        <Icon className={`w-5 h-5 ${style.iconColor} flex-shrink-0 mt-0.5`} />
        <div className="flex-1 min-w-0">
          <h4 className="text-sm font-medium text-white">{title}</h4>
          {message && <p className="text-sm text-gray-200 mt-1">{message}</p>}
        </div>
        <button
          onClick={() => onDismiss(id)}
          className="text-gray-300 hover:text-white transition-colors flex-shrink-0"
        >
          <X className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
} 