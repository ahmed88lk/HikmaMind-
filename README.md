# 🧠 HikmaMind

## AI-Powered Research Assistant

HikmaMind is an intelligent research assistant that helps professionals, academics, and researchers understand complex content through personalized explanations and visual analogies.



## ✨ Features

- **YouTube Video Analysis**: Extract key concepts and create analogies from educational videos
- **PDF Document Analysis**: Understand research papers with customized explanations based on your expertise level
- **Personalized Learning**: Tailors explanations to your field, knowledge level, and preferred analogy style
- **AI Image Generation**: Create visual representations of complex concepts
- **Export Results**: Download analyses as text files for future reference

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- A Google API key with access to Gemini models

### Installation




2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your Google Gemini API key:
```
GOOGLE_GENAI_API_KEY=your_api_key_here
```

### Usage

1. Run the Streamlit application:
```bash
streamlit run app.py
```

2. Open your browser and go to http://localhost:8501
3. Complete your user profile
4. Choose what to analyze:
   - YouTube videos
   - PDFs via URLs
   - Uploaded PDFs

## 🔧 How It Works

HikmaMind uses Google's Gemini AI to:
1. Process research papers and videos
2. Generate personalized explanations based on your profile
3. Create analogies that match your learning style
4. Generate visual explanations when needed

## 🧪 Technologies Used

- [Streamlit](https://streamlit.io/) - Frontend UI
- [Google Gemini AI](https://ai.google.dev/gemini-api) - AI models for text and image generation
- [Python dotenv](https://pypi.org/project/python-dotenv/) - Environment management
- [HTTPX](https://www.python-httpx.org/) - API requests



## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
