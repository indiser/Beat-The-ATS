# 🤖 ATS Resume Scanner

> **Beat the Applicant Tracking System.** Analyze your resume against job descriptions using advanced NLP and semantic matching to optimize your chances of passing automated screening.

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.8+-3776ab?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Latest-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Contributors](https://img.shields.io/badge/Contributors-Welcome-brightgreen)](CONTRIBUTING.md)

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [How It Works](#-how-it-works) • [Project Structure](#-project-structure)

</div>

---

## 📋 Overview

Applying to jobs in today's market means competing against Applicant Tracking Systems (ATS) before your resume even reaches a human recruiter. This project provides intelligent analysis tools to help you optimize your resume for ATS systems using two powerful approaches:

1. **Keyword Matching** - Extract and compare critical keywords from your resume against job requirements
2. **Semantic Analysis** - Use machine learning (cosine similarity) to understand contextual relevance beyond exact matches

With both **Streamlit** and **Flask** interfaces, you can analyze your resume against any job description and receive actionable feedback to improve your match score.

---

## ✨ Features

### Core Analysis Engine
- 📊 **Dual-Mode Scoring System**
  - **Keyword Match Score** (0-100%): Exact keyword extraction and comparison
  - **AI Semantic Score** (0-100%): Advanced cosine similarity using machine learning vectors
  
- 🔍 **Intelligent Text Processing**
  - PDF resume extraction with multi-page support
  - NLTK-powered stopword removal and word tokenization
  - Porter stemmer for word root normalization
  - Custom boilerplate filtering for recruitment terminology

- 📈 **Comprehensive Analysis Report**
  - Matched keywords visualization
  - Missing critical keywords identification (actionable recommendations)
  - AI-powered match strength assessment
  - Verdicts: 🚀 Interview Likely | ⚠️ Application at Risk | 🗑️ High Rejection Probability

### User Interfaces
- **Streamlit Web App** (`app.py`)
  - Lightweight, modern, interactive interface
  - Real-time analysis feedback
  - Perfect for quick resume checks

- **Flask Web Application** (`ats-web-app/`)
  - Full-featured web interface with Bootstrap 5
  - Light/Dark theme toggle
  - Professional dashboard with progress indicators
  - Responsive design for mobile and desktop

### Development Features
- Multiple algorithm versions for learning and experimentation
- Modular `ATSScanner` class for easy integration
- Comprehensive error handling
- NLTK data auto-download on first run

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager
- A PDF resume file
- A job description (text)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/indiser/ats-resume-scanner.git
   cd ats-resume-scanner
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Usage

#### Option 1: Streamlit Web Interface (Recommended for Quick Analysis)
```bash
streamlit run app.py
```
- Opens in your browser at `http://localhost:8501`
- Upload PDF resume and paste job description
- Get instant analysis with interactive metrics

#### Option 2: Flask Web Application (Full-Featured)
```bash
cd ats-web-app
python server.py
```
- Access at `http://localhost:5000`
- Professional interface with theme toggling
- Detailed visual report with gradient progress bars

#### Option 3: Command-Line Analysis (Script-Based)
```bash
python version3.py
```
- Place `resume.pdf` and `job_description.txt` in the root directory
- Outputs detailed terminal report with color-coded missing keywords
- Best for batch processing or integration with other tools

---

## 🧠 How It Works

### Algorithm Overview

```
Input: Resume (PDF) + Job Description (Text)
                    ↓
         ┌──────────────────────┐
         │   TEXT PREPROCESSING │
         └──────────────────────┘
                    ↓
    ┌─────────────────────────────────┐
    │ • Lowercase conversion            │
    │ • NLTK tokenization              │
    │ • Stopword removal               │
    │ • Porter stemmer normalization   │
    │ • Boilerplate filtering          │
    └─────────────────────────────────┘
                    ↓
    ┌──────────────────┐    ┌──────────────────────────┐
    │  KEYWORD MATCH   │    │  SEMANTIC ANALYSIS       │
    │  (Set Theory)    │    │  (Cosine Similarity)     │
    └──────────────────┘    └──────────────────────────┘
              ↓                           ↓
    • Intersection            • CountVectorizer
    • Difference              • TF-IDF weighting
    • Percentage calc         • Cosine similarity
              ↓                           ↓
    ┌──────────────────┐    ┌──────────────────────────┐
    │  Match Score %   │    │  AI Semantic Score %     │
    │  Matched words   │    │  Contextual relevance    │
    │  Missing words   │    │  Semantic alignment      │
    └──────────────────┘    └──────────────────────────┘
                    ↓
         ┌──────────────────────┐
         │  VERDICT GENERATION  │
         └──────────────────────┘
                    ↓
    🚀 Score ≥ 80%: Interview Likely
    ⚠️ Score 50-80%: Application at Risk  
    🗑️ Score < 50%: High Rejection Probability
```

### Key Components

**Text Cleaning Pipeline**
- Removes case variations with lowercasing
- Tokenizes sentences into individual words using NLTK
- Filters out 170+ English stopwords plus recruitment boilerplate
- Applies Porter stemmer to normalize word roots (e.g., "running" → "run")
- Returns a clean set of meaningful keywords

**Keyword Matching Algorithm**
- Treats both resume and job description as mathematical sets
- Finds intersection: keywords present in BOTH documents
- Finds difference: critical keywords missing from resume
- Calculates match percentage: (matched keywords / total JD keywords) × 100

**Semantic Analysis (Machine Learning)**
- Converts text to numerical vectors using CountVectorizer
- Calculates cosine similarity between resume and JD vectors
- Returns percentage representing contextual relevance
- More sophisticated than exact keyword matching alone

---

## 📁 Project Structure

```
ats-resume-scanner/
│
├── app.py                          # Streamlit main application
├── version1.py                     # Basic keyword-only algorithm (educational)
├── version2.py                     # NLTK-enhanced algorithm with stemming
├── version3.py                     # Advanced dual-scoring with semantic analysis
│
├── ats-web-app/                    # Flask web application
│   ├── server.py                   # Flask server with routes
│   ├── ats_scanner.py              # Core ATS analysis engine
│   └── templates/
│       └── index.html              # Professional responsive UI
│
├── requirements.txt                # Python dependencies
├── job_description.txt             # Sample job posting
├── alternative_job_description.txt # Alternative job sample
├── Readme.md                       # This file
└── __pycache__/                    # Python cache (ignore)
```

### File Descriptions

| File | Purpose |
|------|---------|
| `app.py` | Streamlit interface - fast, interactive resume scanning |
| `version1.py` | Basic implementation with manual stopword list |
| `version2.py` | Enhanced with NLTK, stemming, and better preprocessing |
| `version3.py` | Production-ready with dual-scoring and cosine similarity |
| `server.py` | Flask backend with REST routes and form handling |
| `ats_scanner.py` | Reusable ATS analysis class with all algorithms |
| `index.html` | Modern Bootstrap 5 interface with dark mode support |

---

## 🛠️ Technical Stack

### Core Libraries
- **PyPDF2** - PDF text extraction
- **NLTK** - Natural Language Toolkit for text processing
- **scikit-learn** - Machine learning for vectorization and similarity
- **Flask** - Lightweight web framework
- **Streamlit** - Rapid web app development

### Frontend
- **Bootstrap 5** - Responsive CSS framework
- **Bootstrap Icons** - Icon library
- **Vanilla JavaScript** - Theme toggle and interactions

### Python Version
- 3.8+ (tested on 3.9, 3.10, 3.11)

---

## 📊 Example Output

### Streamlit Interface
```
🚀 Smart ATS Resume Scanner
Upload your Resume and paste the Job Description to see if you survive the robots.

┌─────────────────────────────────┐
│ Keyword Match: 78.5%            │
│ AI Match: 85.2%                 │
├─────────────────────────────────┤
│ Missing Keywords:                │
│ kubernetes | terraform | jenkins │
│ docker | aws | ci/cd            │
└─────────────────────────────────┘
```

### Flask Dashboard
```
VERDICT: 🚀 Interview Likely
═══════════════════════════════════
Keyword Match: 78.5%  |  AI Semantic Match: 85.2%

Overall Match Strength: ████████████████░░ 85%

⚠️ Missing Keywords (7):
[kubernetes] [terraform] [jenkins] [docker] [aws] [cicd] [golang]
```

### Terminal Output
```
==============================
MATCH SCORE: 78.5%
COSINE (AI) SCORE: 85.2%
==============================

✅ MATCHED KEYWORDS (34):
kubernetes, docker, python, aws, jenkins, cicd, ...

⚠️ MISSING CRITICAL KEYWORDS (7):
- terraform
- golang  
- ansible
- mongodb
- cassandra
- nginx
- apache

Verdict: 🚀 INTERVIEW LIKELY. Great job.
```

---

## 💡 How to Use for Resume Optimization

### Step 1: Get Your Job Target
Copy the full job description from the posting

### Step 2: Upload Your Resume
Provide your current resume in PDF format

### Step 3: Analyze Results
The tool will show:
- How many critical keywords you have
- Which keywords are missing from your resume
- Your overall match percentage

### Step 4: Optimize Your Resume
- Add missing keywords naturally into your resume
- Highlight relevant skills and experience
- Use the exact terminology from the job description
- Re-upload to verify improvements

### Step 5: Iterate
Repeat for each job application to maximize ATS pass-through rates

---

## ⚙️ Configuration & Customization

### Modify Stopwords
Edit the boilerplate set in `version3.py` or `ats_scanner.py`:
```python
boilerplate = {
    "job", "title", "candidate", "description", 
    # Add your custom stopwords here
}
```

### Adjust Scoring Thresholds
In `server.py`, modify verdict thresholds:
```python
if cosine_match >= 80:
    verdict = "🚀 Interview Likely"
elif cosine_match >= 50:
    verdict = "⚠️ Application at Risk"
```

### Change UI Styling
Customize colors and layout in `index.html` Bootstrap classes and CSS variables

---

## 🔬 Comparison of Versions

| Feature | v1 | v2 | v3 |
|---------|----|----|-----|
| Keyword Extraction | ✓ | ✓ | ✓ |
| Basic Stopwords | ✓ | ✓ | ✓ |
| NLTK Tokenization | ✗ | ✓ | ✓ |
| Porter Stemming | ✗ | ✓ | ✓ |
| Cosine Similarity | ✗ | ✗ | ✓ |
| Dual Scoring | ✗ | ✗ | ✓ |
| Production Ready | ✗ | ~ | ✓ |

---

## 🚨 Limitations & Considerations

- **Resume Format**: Currently supports PDF files only (not Word, Google Docs)
- **OCR Not Included**: Won't work with image-based PDFs; use text-based PDFs
- **Language Support**: Optimized for English text
- **Accuracy**: No guarantees of ATS passing; ATS systems vary by company
- **Context Blind**: Doesn't understand context (e.g., 5 years vs 5 months)
- **Synonyms**: May miss industry synonyms; use exact job description terminology

---

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Multi-language support
- OCR capability for scanned PDFs
- More sophisticated NLP models
- Resume formatting suggestions
- Integration with job boards
- Additional interface options

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- NLTK team for excellent NLP tools
- scikit-learn for machine learning algorithms
- Bootstrap team for responsive design framework
- PyPDF2 for reliable PDF handling

---

## 📧 Support & Feedback

- **Found a bug?** Open an [Issue](../../issues)
- **Have suggestions?** Start a [Discussion](../../discussions)
- **Want to collaborate?** Submit a [Pull Request](../../pulls)

---

## 📚 Additional Resources

- [NLTK Documentation](https://www.nltk.org/)
- [scikit-learn Guide](https://scikit-learn.org/)
- [ATS Tips & Tricks](https://www.indeed.com/career-advice/resumes-cover-letters)
- [Job Description Analysis](https://www.jobdescriptionhub.com/)

---

<div align="center">

**Made with ❤️ to help you beat the robots**

⭐ If this project helped you, please consider giving it a star!

</div>