import cv2
import numpy as np
import os
from openvino.runtime import Core

class EmotionRecognizer:
    """
    A class to load and perform inference with the emotions-recognition-retail-0003
    OpenVINO model. This version uses manual preprocessing for maximum reliability.
    """
    def __init__(self, model_xml_path=r'models\weights\intel\emotions-recognition-retail-0003\FP32\emotions-recognition-retail-0003.xml', model_bin_path=r'models\weights\intel\emotions-recognition-retail-0003\FP32\emotions-recognition-retail-0003.bin'):
        """
        Initializes the EmotionRecognizer by loading and compiling the OpenVINO model.
        All preprocessing is handled manually in the `infer` method.

        Args:
            model_xml_path (str): Path to the .xml file of the emotion recognition model.
            model_bin_path (str): Path to the .bin file of the emotion recognition model.
        """
        self.emotion_labels = ['neutral', 'happy', 'sad', 'surprise', 'anger']
        # The model requires a specific 64x64 input size
        self.input_height = 64
        self.input_width = 64

        try:
            core = Core()
            # 1. Load the original model from the files
            emotion_model = core.read_model(model=model_xml_path, weights=model_bin_path)

            # 2. Compile the model for the target device (e.g., "CPU")
            # We are not using PrePostProcessor or reshaping the model itself.
            self.compiled_emotion_model = core.compile_model(emotion_model, "CPU")

            # 3. Get the model's output layer
            self.output_layer = self.compiled_emotion_model.outputs[0]
            
            print("Emotion recognition model loaded successfully (using manual preprocessing).")
            # For debugging, confirm the model's expected input shape
            print(f"Model expects input shape: {emotion_model.input(0).shape}")

        except Exception as e:
            print(f"Error initializing EmotionRecognizer: {e}")
            raise RuntimeError(f"Could not load emotion recognition model from {model_xml_path}") from e

    def infer(self, face_roi: np.ndarray) -> tuple[str, float]:
        """
        Performs emotion recognition by manually preprocessing the face crop
        and then running inference.

        Args:
            face_roi (np.ndarray): A NumPy array representing the cropped face region (HWC, BGR).

        Returns:
            tuple[str, float]: A tuple containing the predicted emotion label and its confidence score.
        """
        if face_roi is None or face_roi.size == 0:
            return "unknown", 0.0

        try:
            # --- MANUAL PREPROCESSING ---
            # 1. Resize the image to the model's required input size (64x64).
            resized_face = cv2.resize(face_roi, (self.input_width, self.input_height))

            # 2. Transpose the image from HWC to CHW format.
            # OpenCV provides (Height, Width, Channels)
            # The model requires (Channels, Height, Width)
            transposed_face = resized_face.transpose(2, 0, 1)

            # 3. Add a batch dimension (N) to create the final NCHW tensor.
            input_tensor = np.expand_dims(transposed_face, axis=0)
            
            # 4. Run inference on the manually preprocessed tensor.
            # The result is a dictionary where the key is the output layer.
            results = self.compiled_emotion_model([input_tensor])[self.output_layer]
            
            # --- POST-PROCESSING ---
            emotion_probabilities = results.flatten()
            predicted_emotion_idx = np.argmax(emotion_probabilities)
            predicted_emotion = self.emotion_labels[predicted_emotion_idx]
            confidence = emotion_probabilities[predicted_emotion_idx]

            return predicted_emotion, confidence

        except Exception as e:
            print(f"Error during emotion inference: {e}")
            return "error", 0.0