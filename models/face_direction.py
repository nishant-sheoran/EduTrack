# models/face_direction.py

import numpy as np
import os
import cv2
from openvino.runtime import Core

class HeadPoseEstimator:
    def __init__(self, model_precision='FP32'):
        model_dir = os.path.join('models', 'weights', 'intel', 'head-pose-estimation-adas-0001', model_precision)
        model_xml = os.path.join(model_dir, 'head-pose-estimation-adas-0001.xml')
        model_bin = os.path.join(model_dir, 'head-pose-estimation-adas-0001.bin')

        if not os.path.exists(model_xml) or not os.path.exists(model_bin):
            raise FileNotFoundError("Model files not found. Please check the path.")

        core = Core()
        self.model = core.read_model(model=model_xml)
        self.compiled_model = core.compile_model(self.model, device_name="CPU")

        # Extract input and output layer names
        self.input_layer_name = self.model.inputs[0].get_any_name()
        self.output_layer_names = {
            "yaw": self.model.output("angle_y_fc").get_any_name(),
            "pitch": self.model.output("angle_p_fc").get_any_name(),
            "roll": self.model.output("angle_r_fc").get_any_name()
        }

        print("Head Pose Estimation model loaded using OpenVINO runtime.")

    def predict_angles(self, face_crop):
        if face_crop is None or face_crop.size == 0:
            return 0.0, 0.0, 0.0

        # Resize to 60x60 as required by the model
        resized_face = cv2.resize(face_crop, (60, 60))
        input_blob = np.expand_dims(resized_face.transpose(2, 0, 1), axis=0).astype(np.float32)

        # Inference using input/output **names**
        results = self.compiled_model({self.input_layer_name: input_blob})

        yaw = float(results[self.output_layer_names["yaw"]])
        pitch = float(results[self.output_layer_names["pitch"]])
        roll = float(results[self.output_layer_names["roll"]])

        return yaw, pitch, roll
