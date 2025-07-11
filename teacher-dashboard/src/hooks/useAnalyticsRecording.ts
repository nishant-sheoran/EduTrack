import { useCallback, useState } from 'react';

const BACKEND_URL = 'http://localhost:8080/recording';

export interface RecordingResult {
  videoUrl: string;
  transcriptUrl: string;
}

export const useAnalyticsRecording = () => {
  const [recordingResult, setRecordingResult] = useState<RecordingResult | null>(null);

  const sendAnalyticsState = useCallback(
    async (action: 'start' | 'stop', session_id: string) => {
      const endpoint = `${BACKEND_URL}/${action}`;

      try {
        const response = await fetch(endpoint, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ session_id }),
        });

        if (!response.ok) {
          console.error(`Failed to ${action} recording:`, response.statusText);
          return;
        }

        if (action === 'stop') {
          const data = await response.json();
          const { videoUrl, transcriptUrl } = data;

          if (videoUrl && transcriptUrl) {
            setRecordingResult({ videoUrl, transcriptUrl });
          } else {
            console.warn("Missing videoUrl or transcriptUrl in stop response:", data);
          }
        }
      } catch (error) {
        console.error(`Error during ${action} recording request:`, error);
      }
    },
    []
  );

  return { sendAnalyticsState, recordingResult };
};
