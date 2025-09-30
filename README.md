<div align="center">
  <img src="https://via.placeholder.com/1200x400/3b82f6/ffffff?text=Website+Summarizer+with+Gemini+AI" alt="Website Summarizer with Gemini AI" width="100%" style="max-width: 1200px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
</div>

---

# 🌐 Website Summarizer with Gemini AI

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)](https://jupyter.org/)
[![Gradio](https://img.shields.io/badge/Gradio-UI-yellow.svg)](https://gradio.app/)
[![Gemini AI](https://img.shields.io/badge/Google-Gemini_AI-red.svg)](https://ai.google.dev/)

> An intelligent website summarization tool powered by Google's Gemini AI that can analyze and summarize web content with beautiful, interactive user interfaces.

## ✨ Features

![Website Summarizer Demo](https://via.placeholder.com/800x400/3b82f6/ffffff?text=Website+Summarizer+Demo)

- **🚀 AI-Powered Summarization**: Uses Google's advanced Gemini AI models for accurate, contextual summaries
- **🖥️ Dual Interfaces**: Choose between Jupyter Notebook UI or web-based Gradio interface
- **📊 Multiple Summary Types**: Generate short, detailed, or bullet-point summaries
- **🔗 Smart Web Scraping**: Automatically extracts and cleans website content
- **🖼️ Visual Enhancement**: Displays website favicons, logos, and key images in summaries
- **⚡ Real-time Processing**: Fast summarization with progress indicators
- **🎨 Modern UI Design**: Beautiful, responsive interfaces with dark/light themes
- **📱 Cross-Platform**: Works on desktop and mobile devices
- **🔒 Error Handling**: Robust error handling with helpful user feedback

## 🛠️ Installation

### Option 1: Using Conda (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd website-summarizer

# Create conda environment
conda env create -f environment.yml

# Activate environment
conda activate llms
```

### Option 2: Using Pip

```bash
# Clone the repository
git clone <repository-url>
cd website-summarizer

# Install dependencies
pip install -r requirements.txt
```

### Option 3: Using Poetry

```bash
# Install Poetry (if not already installed)
curl -sSL https://install.python-poetry.org | python3 -

# Clone and install
git clone <repository-url>
cd website-summarizer
poetry install
```

## 🔑 API Setup

### Google Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Create a new API key
3. Copy the API key (format: `sk-proj-...`)

### Environment Configuration

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=sk-proj-your-api-key-here
```

## 🖼️ Visual Features

The Website Summarizer now includes enhanced visual capabilities:

### Website Image Display
- **Favicon Extraction**: Automatically displays the website's favicon in the summary
- **Image Gallery**: Shows up to 2 relevant images from the webpage
- **Smart Filtering**: Only displays reasonably-sized images (>100px width)
- **Visual Context**: Images help provide visual context for the summarized content

### UI Enhancements
- **Application Logo**: Professional logo display in the interface header
- **Responsive Images**: Images automatically resize for different screen sizes
- **Loading States**: Visual feedback during content processing

## 🚀 Usage

### Jupyter Notebook Interface

```bash
# Activate conda environment (if using conda)
conda activate llms

# Launch Jupyter Lab
jupyter lab
```

1. Open `Sumaeize a website using Gemini API.ipynb`
2. Run all cells to start the interactive UI
3. Enter any website URL in the input field
4. Click "🚀 Summarize Website" to generate summaries

### Gradio Web Interface

```bash
# Activate conda environment (if using conda)
conda activate llms

# Run the Gradio app
python app.py
```

The web interface will be available at `http://localhost:7860` with:
- **Single URL Tab**: Summarize individual websites
- **Batch Processing Tab**: Summarize multiple URLs at once
- **History Tab**: View and export previous summaries

## 📁 Project Structure

```
website-summarizer/
├── 📄 README.md                    # This file
├── 📄 LICENSE                      # MIT License
├── 📄 requirements.txt             # Python dependencies
├── 📄 environment.yml              # Conda environment
├── 📄 .env                         # API keys (create this)
├── 📄 .gitignore                   # Git ignore rules
│
├── 📋 Sumaeize a website using Gemini API.ipynb  # Jupyter interface
├── 📄 app.py                       # Gradio web interface
│
└── 📁 .taskmaster/                 # Task management (optional)
    ├── 📄 docs/
    └── 📁 tasks/
```

## 🛠️ Technologies Used

- **🤖 Google Gemini AI**: Advanced language model for summarization
- **🕷️ BeautifulSoup**: Web scraping and content extraction
- **📊 ipywidgets**: Interactive Jupyter notebook widgets
- **🌐 Gradio**: Web interface framework
- **🐍 Python 3.11+**: Core programming language
- **📚 LangChain**: LLM framework integration
- **🎨 CSS/Styling**: Custom responsive design

## 🔧 Configuration Options

### Summary Types

The application supports three summary types:

1. **Short**: Concise 2-3 sentence summaries
2. **Detailed**: Comprehensive analysis with key points
3. **Bullet Points**: Structured list format

### Customization

Modify `app.py` to customize:
- Default summary length
- UI themes and styling
- Supported websites/languages

## 🚨 Troubleshooting

### Common Issues

**❌ "No API key found"**
- Ensure `.env` file exists with correct `GEMINI_API_KEY`
- Check API key format (should start with `sk-proj-`)

**❌ "Website cannot be summarized"**
- Some sites block scraping (check robots.txt)
- Try sites without heavy JavaScript
- Consider using Selenium for dynamic content

**❌ "Import errors"**
- Activate the correct conda environment
- Install missing dependencies: `pip install -r requirements.txt`

**❌ "Gradio interface not loading"**
- Check port availability (default: 7860)
- Restart Python kernel if needed

### Debug Mode

Enable debug logging in `app.py`:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone your fork
git clone <your-fork-url>
cd website-summarizer

# Create development environment
conda env create -f environment.yml
conda activate llms

# Install in development mode
pip install -e .
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini AI** for providing the powerful language model
- **Gradio Team** for the excellent web interface framework
- **BeautifulSoup Community** for robust web scraping tools


**⭐ If you found this project helpful, please give it a star!**