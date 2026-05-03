# 🛍️ AI Product Recommendation Agent

> **An intelligent shopping assistant powered by AI agents that finds, analyzes, and recommends the best products based on your needs and budget.**

## 🌟 Live Demo

🔗 **Try it now:** [Your Streamlit URL]

## 🎯 Problem Solved

Online shopping is overwhelming. Users spend hours comparing products, reading reviews, and checking prices across multiple sites. Our AI agent does this in seconds.

## ✨ Features

- 🤖 **AI-Powered Recommendations** - Personalized to your needs
- 🔍 **Real-Time Web Search** - Always current prices and products
- 📊 **Smart Comparison** - Analyzes features, prices, reviews
- 💰 **Budget-Conscious** - Respects your spending limit
- 🎨 **Beautiful UI** - Clean, intuitive interface
- ⚡ **Fast Results** - Recommendations in seconds

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| AI Agent | Dify + Google Gemini 2.0 Flash |
| Frontend | Streamlit |
| Backend API | Dify Cloud API |
| Search | Tavily AI Search |
| Hosting | Streamlit Community Cloud |
| Version Control | GitHub |

## 🏗️ Architecture

\`\`\`
User → Streamlit UI → Dify API → AI Agent → Tools → Recommendations
\`\`\`

The AI agent autonomously:
1. Understands user requirements
2. Searches multiple web sources
3. Scrapes product details
4. Calculates value scores
5. Generates personalized recommendations

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Dify account
- Google AI Studio API key
- Tavily Search API key

### Installation

\`\`\`bash
# Clone repo
git clone https://github.com/yourusername/ai-product-recommender.git
cd ai-product-recommender

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Add your API keys
cp .env.example .env
# Edit .env with your keys

# Run the app
streamlit run app.py
\`\`\`

## 📸 Screenshots

[Add 3-4 screenshots of your app]

## 🎬 Demo Video

[Link to your demo video]

## 🤖 How the AI Agent Works

The agent uses Dify's function calling capability to autonomously decide which tools to use:

1. **Tavily Search** - Finds product listings
2. **Web Scraper** - Extracts detailed information
3. **Calculator** - Computes value scores
4. **Time Tool** - Ensures current data

## 📊 Example Queries

- "Best laptop under ₹60,000 for programming"
- "Wireless earbuds with great bass under ₹5,000"
- "Smart TV under ₹40,000 with 4K"
- "Gaming mouse for FPS games under ₹2,500"

## 🏆 Competition Highlights

✅ Full-stack AI application
✅ Production-ready deployment
✅ Real-world problem solving
✅ Modern tech stack
✅ Scalable architecture
✅ Beautiful UX

## 👥 Team

- **[Your Name]** - Developer
- LinkedIn: [Your LinkedIn]
- GitHub: [@yourusername]

## 📝 License

MIT License

## 🙏 Acknowledgments

- Dify AI for the powerful agent platform
- Google Gemini for the LLM
- Streamlit for the amazing framework
- Tavily for search API