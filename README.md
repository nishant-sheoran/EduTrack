# EduTrack: AI-Powered Real-Time Engagement Monitor for Classrooms

## 📌 Overview
EduTrack is an AI-powered classroom assistant designed to bridge the gap between teaching and personalized learning. It transcribes lectures in real-time while monitoring student attentiveness using webcam feeds. When inattentiveness is detected, the system logs the timestamp and later generates a personalized summary of the missed content, ensuring that every student has the opportunity to catch up.

This solution is compatible with both **online and offline classroom environments**, and employs **efficient round-robin analysis** for scalable student monitoring. The project is optimized using **Intel OpenVINO Toolkit** to ensure faster inference and deployability.

## 🧠 Key Features

- 🎤 **Real-time Speech-to-Text** using Whisper or Wav2Vec2
- 🎥 **Webcam-based Student Sentiment Monitoring** using MobileNet or CNN-based classifier
- 🧾 **Timestamp Mapping** to log inattentive periods
- 📬 **Personalized Summary Generation** per student post-class
- ⚙️ **OpenVINO Optimization** for model compression & accelerated inference
- 🖥️ **Gradio/Streamlit Frontend** for easy demo and visualization
- 🧠 **Hardware-aware processing** via round-robin sampling across student streams


## 🧱 Project Structure

```
EduTrack/
├── models/                  # Optimized and base models
│   ├── speech_to_text/     # Whisper/Wav2Vec2 models
│   └── sentiment/          # Face/Sentiment detection models
├── data/
│   ├── transcripts/        # Generated transcripts
│   └── logs/               # Engagement logs per session
├── src/                    # Core source code
│   ├── audio_transcriber.py
│   ├── sentiment_detector.py
│   ├── summarizer.py
│   ├── optimizer.py
│   ├── round_robin.py
│   └── utils.py
├── demo/                   # Demo assets
│   ├── demo.gif
│   └── sample_output.mp4
├── frontend/
│   └── app.py              # Gradio/Streamlit interface
├── README.md
├── requirements.txt
├── openvino_benchmark.md  # Optimization metrics and logs
├── .gitignore
└── LICENSE
```


## 🚀 How to Run

### 1. Clone and install dependencies
```bash
git clone https://github.com/yourusername/EduTrack.git
cd EduTrack
pip install -r requirements.txt
```

### 2. Launch the frontend
```bash
python frontend/app.py
```

### 3. View transcripts & logs
- Transcripts will be saved in `data/transcripts/`
- Attention logs and flagged students in `data/logs/`


## 🔧 Optimization Strategy (OpenVINO)

| Component            | Original Model       | Optimization Technique           |
|---------------------|----------------------|----------------------------------|
| Speech-to-Text      | Whisper/Wav2Vec2     | ONNX export + INT8 Quantization |
| Sentiment Detection | MobileNet/CNN        | Pruning + Quantization + INT8   |
| Summary Generator   | T5-small / Pegasus   | ONNX export + Batching          |

Detailed benchmarking and model conversion logs are in [`openvino_benchmark.md`](openvino_benchmark.md).


## 📊 Benchmark Metrics

| Metric              | Before Optimization | After Optimization |
|---------------------|----------------------|---------------------|
| Model Size (STT)    | 120MB                | 35MB                |
| Inference Time (STT)| 220ms                | 70ms                |
| Sentiment FPS       | 8fps                 | 18fps               |

_(Sample values, actual values will be updated based on system performance)_


## 🛠️ Deployment Considerations

This repo is designed to be:
- **Modular & extensible**: You can replace models or pipeline steps easily.
- **Deployable**: Final models are optimized for edge (CPU/GPU/NPU) devices.
- **Adaptable**: Works in online & offline classroom environments with round-robin processing for scalability.

> 💡 Future versions may include REST API endpoints, user authentication, database integration, and batch email delivery.


## 🎯 Use Cases
- Smart classrooms in schools & universities
- Online learning platforms
- Special assistance for slow or struggling learners


## 👥 Contributing

Pull requests are welcome. Please open an issue first to discuss any major changes. We follow a modular coding style and clean commit history.


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## 📽️ Demo

- [✔️ Demo GIF](demo/demo.gif)
- [📺 Sample Output Video](demo/sample_output.mp4)
## 🙌 Team

- Nishant Sheoran
- Piyush
- Satvik

Feel free to reach out or fork this project for further improvements. 🚀
