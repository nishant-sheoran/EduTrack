# 🚀 Getting Started - Voice to Educational Video Generator

## Quick Start (5 minutes)

### 1. Install Dependencies
```bash
# Windows
setup.bat

# Or manually:
pip install streamlit openai gTTS pydub reportlab python-dotenv aiofiles requests numpy matplotlib
```

### 2. Set Up API Key
1. Get your OpenAI API key from https://platform.openai.com/
2. Edit `.env` file:
   ```
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```

### 3. Run the App
```bash
streamlit run app.py
```

## 📱 Using the Web Interface

1. **Open your browser** to `http://localhost:8501`
2. **Enter your OpenAI API key** in the sidebar
3. **Upload an audio file** (WAV, MP3, MP4, etc.)
4. **Add a topic hint** (optional) like "Linear Algebra" or "Machine Learning"
5. **Click "Generate Educational Video"**
6. **Wait for processing** (2-5 minutes depending on audio length)
7. **Download your results:**
   - 🎥 Educational video (MP4)
   - 📄 PDF transcript

## 🎤 Sample Audio Ideas

Record yourself explaining:
- Math concepts (derivatives, integrals, linear algebra)
- Programming topics (algorithms, data structures)
- Science topics (physics laws, chemistry reactions)
- Any educational subject you know well!

**Tips for better results:**
- Speak clearly and at moderate pace
- Keep recordings 2-10 minutes long
- Use topic hint for better AI processing
- Explain concepts step-by-step

## 💻 Command Line Usage

```bash
# Process single file
python cli.py process my_audio.wav --topic "Calculus" --quality high

# Batch processing
python cli.py batch *.wav --topics "Math" "Physics" "Chemistry"

# Check system
python cli.py config --check
```

## 🎬 What Gets Generated

### Educational Video Features:
- ✨ 3Blue1Brown-style animations
- 📊 Mathematical graphs and equations
- 🎨 Professional color scheme
- 🎵 Synchronized narration
- 📈 Step-by-step visual explanations

### PDF Transcript Features:
- 📖 Structured sections
- 🧮 Formatted mathematical expressions
- 📝 Visual cue annotations
- 🏷️ Keywords and metadata
- 📄 Professional formatting

## 🔧 Troubleshooting

### Common Issues:

**"OpenAI API error"**
- Check your API key in `.env` file
- Ensure you have API credits
- Try with a shorter audio file first

**"Import errors"**
- Run `python setup.py` to install dependencies
- Some packages are optional - the app will use fallbacks

**"No audio detected"**
- Check file format (WAV, MP3, MP4 supported)
- Ensure file isn't corrupted
- Try converting to WAV format

**"Video generation failed"**
- Manim installation is optional for basic functionality
- PDF generation will still work
- Try the narrator and script generator first

### Performance Tips:
- Start with short audio files (30 seconds - 2 minutes)
- Use topic hints for better results
- Check your internet connection for API calls

## 🎯 Example Workflow

1. **Record a 2-minute explanation** of a concept you know well
2. **Save as "my_lesson.wav"**
3. **Open the web app** (`streamlit run app.py`)
4. **Upload the file** with topic hint "Your Subject"
5. **Wait for processing** (grab a coffee ☕)
6. **Download and enjoy** your educational video!

## 📚 Next Steps

- Experiment with different topics and audio lengths
- Try the command-line interface for batch processing
- Customize the animation style in the settings
- Share your educational videos with others!

## ❓ Need Help?

- Check the main [README.md](README.md) for detailed documentation
- Look at [example_test.py](example_test.py) for code examples
- Open an issue if you find bugs
- The app works best with clear, educational audio content

---

**Ready to create your first educational video? Let's go! 🚀**
