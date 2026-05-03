"""
AI Product Recommendation Agent - Streamlit Frontend
"""
import streamlit as st
from dify_client import DifyClient
import time

# Page config
st.set_page_config(
    page_title="AI Product Recommender",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful UI
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .stButton>button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.7rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 10px;
        width: 100%;
    }
    .stButton>button:hover {
        opacity: 0.9;
        transform: translateY(-2px);
        transition: 0.3s;
    }
    .example-box {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
    }
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = ""
if "messages" not in st.session_state:
    st.session_state.messages = []
if "recommendations" not in st.session_state:
    st.session_state.recommendations = []

# Initialize Dify client
@st.cache_resource
def get_dify_client():
    return DifyClient()

dify = get_dify_client()

# Sidebar
with st.sidebar:
    st.markdown("## 🛍️ About")
    st.info("""
    **AI Product Recommendation Agent**
    
    Powered by:
    - 🤖 Dify AI
    - 🧠 Google Gemini
    - 🔍 Real-time Web Search
    - ⚡ Streamlit
    """)
    
    st.markdown("## 💡 How It Works")
    st.markdown("""
    1. **Tell us** what you need
    2. **AI searches** the web for real products
    3. **AI analyzes** prices, features, reviews
    4. **Get** top 3 personalized picks
    """)
    
    st.markdown("## 🎯 Categories")
    categories = ["💻 Laptops", "📱 Phones", "🎧 Headphones", 
                  "⌚ Smartwatches", "📺 TVs", "🎮 Gaming"]
    for cat in categories:
        st.markdown(f"- {cat}")
    
    st.markdown("---")
    if st.button("🔄 New Search"):
        st.session_state.conversation_id = ""
        st.session_state.messages = []
        st.session_state.recommendations = []
        st.rerun()

# Main content
st.markdown('<div class="main-header">🛍️ AI Product Recommender</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Find the perfect product with AI-powered recommendations</div>', unsafe_allow_html=True)

# Search Section
col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    # Example prompts
    st.markdown("### 💡 Try these examples:")
    
    examples = [
        "Best laptop under ₹60,000 for programming",
        "Wireless earbuds under ₹3,000 with great bass",
        "Smartphone with best camera under ₹25,000",
        "Gaming mouse under ₹2,000 for FPS games"
    ]
    
    cols = st.columns(2)
    for idx, example in enumerate(examples):
        with cols[idx % 2]:
            if st.button(f"💬 {example}", key=f"ex_{idx}"):
                st.session_state.user_query = example
    
    st.markdown("---")
    
    # Main input
    user_query = st.text_area(
        "**What product are you looking for?**",
        value=st.session_state.get("user_query", ""),
        placeholder="E.g., I need a laptop under ₹50,000 for video editing and college projects...",
        height=100
    )
    
    # Search button
    search_clicked = st.button("🔍 Find Best Products", type="primary")

# Process search
if search_clicked and user_query:
    with st.spinner("🤖 AI is analyzing thousands of products for you..."):
        # Show progress steps
        progress_container = st.container()
        
        with progress_container:
            progress_text = st.empty()
            progress_bar = st.progress(0)
            
            steps = [
                ("🧠 Understanding your needs...", 20),
                ("🔍 Searching the web...", 40),
                ("📊 Analyzing products...", 60),
                ("💰 Comparing prices...", 80),
                ("✨ Preparing recommendations...", 100)
            ]
            
            for step, progress in steps:
                progress_text.text(step)
                progress_bar.progress(progress)
                time.sleep(0.5)  # Visual effect
        
        # Actual API call
        result = dify.get_recommendation(
            query=user_query,
            conversation_id=st.session_state.conversation_id
        )
        
        # Clear progress
        progress_container.empty()
        
        if result["success"]:
            st.session_state.conversation_id = result["conversation_id"]
            
            # Save to history
            st.session_state.messages.append({
                "query": user_query,
                "response": result["answer"]
            })
            
            # Display result
            st.success("✅ Found the best products for you!")
            st.markdown("---")
            st.markdown(result["answer"])
            
            # Action buttons
            st.markdown("---")
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.button("👍 Helpful")
            with col_b:
                st.button("🔄 Refine Search")
            with col_c:
                st.button("📋 Copy Results")
        else:
            st.error(f"❌ Error: {result['error']}")
            st.info("💡 Tip: Try a simpler query or check your internet connection.")

elif search_clicked and not user_query:
    st.warning("⚠️ Please enter a product query first!")

# Show recent searches
if st.session_state.messages:
    st.markdown("---")
    with st.expander("📝 View Search History"):
        for idx, msg in enumerate(reversed(st.session_state.messages[-5:])):
            st.markdown(f"**Search {len(st.session_state.messages) - idx}:** {msg['query']}")
            with st.expander("View recommendations"):
                st.markdown(msg["response"])

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888;'>
    Built with ❤️ using Streamlit, Dify, and Gemini AI<br>
    🏆 Made for the AI Innovation Competition
</div>
""", unsafe_allow_html=True)