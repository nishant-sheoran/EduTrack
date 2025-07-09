# models/face_detection.py (Corrected Again)

import cv2
import numpy as np

class YoloV8FaceDetector:
    """
    YOLOv8 Face Detector class for detecting faces in an image.
    
    It uses an ONNX model and provides a method to get detections in a format
    suitable for trackers like DeepSORT.
    """
    def __init__(self, model_path='models/weights/yolov8n-face.onnx', conf_threshold=0.45, iou_threshold=0.5):
        """
        Initializes the YOLOv8 Face Detector.

        Args:
            model_path (str): Path to the ONNX model file.
            conf_threshold (float): Confidence threshold for filtering detections.
            iou_threshold (float): IoU threshold for non-maximum suppression.
        """
        self.conf_threshold = conf_threshold
        self.iou_threshold = iou_threshold
        self.net = cv2.dnn.readNet(model_path)
        
        # --- THIS IS THE FIX ---
        # Hardcode the standard input size for YOLOv8-face models for reliability.
        # The previous dynamic method was incorrect.
        self.input_height = 640
        self.input_width = 640
        
        print("YOLOv8 Face Detector initialized successfully.")

    def detect(self, image):
        """
        Detects faces in the input image.

        Args:
            image (np.ndarray): The input image in BGR format.

        Returns:
            list: A list of detections in DeepSORT format.
        """
        input_image, scale, pad_x, pad_y = self._format_image(image)
        
        self.net.setInput(input_image)
        outputs = self.net.forward(self.net.getUnconnectedOutLayersNames())
        
        detections = self._process_output(outputs[0], scale, pad_x, pad_y)
        
        return detections

    def _format_image(self, image):
        """Prepares image for network input by padding and scaling."""
        image_height, image_width = image.shape[:2]
        
        # Calculate scaling factor
        scale = min(self.input_width / image_width, self.input_height / image_height)
        scaled_width = int(image_width * scale)
        scaled_height = int(image_height * scale)
        
        # Resize image
        resized_image = cv2.resize(image, (scaled_width, scaled_height))
        
        # Create a blank canvas of model input size
        padded_image = np.full((self.input_height, self.input_width, 3), 114, dtype=np.uint8)
        
        # Calculate padding
        pad_x = (self.input_width - scaled_width) // 2
        pad_y = (self.input_height - scaled_height) // 2
        
        # Place the resized image on the canvas
        padded_image[pad_y:pad_y + scaled_height, pad_x:pad_x + scaled_width] = resized_image
        
        blob = cv2.dnn.blobFromImage(padded_image, 1/255.0, (self.input_width, self.input_height), swapRB=True, crop=False)
        return blob, scale, pad_x, pad_y

    def _process_output(self, output, scale, pad_x, pad_y):
        """Processes raw network output to generate bounding boxes in original image coordinates."""
        output = output.T  # Transpose the output
        
        boxes = []
        confidences = []

        for row in output:
            xc, yc, w, h, score = row[:5]
            
            if score > self.conf_threshold:
                # 1. Adjust for padding
                x_unpadded = xc - pad_x
                y_unpadded = yc - pad_y
                
                # 2. Scale back to original image size
                x1 = int((x_unpadded - w / 2) / scale)
                y1 = int((y_unpadded - h / 2) / scale)
                width = int(w / scale)
                height = int(h / scale)
                
                boxes.append([x1, y1, width, height])
                confidences.append(float(score))

        # Apply Non-Maximum Suppression
        indices = cv2.dnn.NMSBoxes(boxes, confidences, self.conf_threshold, self.iou_threshold)
        
        detections = []
        if len(indices) > 0:
            for i in indices.flatten():
                box = boxes[i]
                score = confidences[i]
                # Format for DeepSORT: ([x, y, w, h], score, class_name)
                detections.append((box, score, 'face'))
        
        return detections