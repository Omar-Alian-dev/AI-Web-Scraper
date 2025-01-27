import streamlit as st
from scrape import scrape_website, split_dom_content, clean_body_content, extract_body_content
from parse import parse_with_ollama

def set_custom_style():
    # Custom CSS for enhanced styling
    st.markdown("""
        <style>
        /* Main background with gradient */
        .stApp {
            background: linear-gradient(to bottom right, #1a1a2e, #16213e, #0f3460);
        }
        
        /* Custom container style */
        .css-1d391kg {
            padding: 2rem;
            border-radius: 15px;
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
        }
        
        /* Header styling */
        .main-header {
            text-align: center;
            padding: 2rem;
            color: #e94560;
            font-size: 3rem;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        
        /* Card-like containers */
        .content-card {
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 10px;
            margin: 10px 0;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        /* Button styling */
        .stButton>button {
            background: linear-gradient(45deg, #e94560, #0f3460);
            color: white;
            border: none;
            padding: 0.5rem 2rem;
            border-radius: 25px;
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(233, 69, 96, 0.4);
        }
        
        /* Input field styling */
        .stTextInput>div>div>input {
            border-radius: 25px;
            border: 2px solid #e94560;
            padding: 1rem;
            background: rgba(255, 255, 255, 0.1);
            color: white;
        }
        
        /* Text area styling */
        .stTextArea>div>div>textarea {
            border-radius: 15px;
            border: 2px solid #0f3460;
            background: rgba(255, 255, 255, 0.1);
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

def main():
    # Set page configuration
    st.set_page_config(
        page_title="Web Scraper AI",
        page_icon="🌐",
        layout="wide"
    )
    
    # Apply custom styling
    set_custom_style()
    
    # Title and description with custom HTML
    st.markdown('<h1 class="main-header">🌐 Web Scraper AI</h1>', unsafe_allow_html=True)
    
    # Decorative elements
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("""
            <div class="content-card">
                <h3 style="color: #e94560; text-align: center;">
                    Transform Web Content into Structured Data
                </h3>
                <p style="text-align: center; color: #ffffff;">
                    Enter a URL below to begin scraping and analyzing web content using AI
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    # URL input section with custom styling
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    url = st.text_input(
        "🔗 Enter Website URL:",
        placeholder="https://example.com",
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Scraping section
    if st.button("🚀 Start Scraping", type="primary"):
        if not url:
            st.error("⚠️ Please enter a valid URL")
            return
            
        try:
            with st.spinner("🔄 Scraping website..."):
                result = scrape_website(url)
                body_content = extract_body_content(result)
                cleaned_content = clean_body_content(body_content)
                st.session_state.dom_content = cleaned_content
                
                st.success("✅ Website scraped successfully!")
                
                with st.expander("📄 View DOM Content", expanded=False):
                    st.markdown('<div class="content-card">', unsafe_allow_html=True)
                    st.text_area(
                        label="DOM Content",
                        value=cleaned_content,
                        height=300,
                        disabled=True
                    )
                    st.markdown('</div>', unsafe_allow_html=True)
        
        except Exception as e:
            st.error(f"❌ Error scraping website: {str(e)}")
            return
    
    # Parsing section
    if "dom_content" in st.session_state:
        st.markdown("---")
        st.markdown('<h2 style="color: #e94560; text-align: center;">AI Content Parser</h2>', unsafe_allow_html=True)
        
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        parse_description = st.text_area(
            "🤖 What would you like to extract?",
            placeholder="Example: Extract all product names and prices",
            help="Be specific about what information you want to parse from the webpage"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("🎯 Parse Content", type="primary"):
            if not parse_description:
                st.error("⚠️ Please describe what you want to parse")
                return
                
            try:
                with st.spinner("🔄 AI is analyzing the content..."):
                    dom_chunks = split_dom_content(st.session_state.dom_content)
                    result = parse_with_ollama(dom_chunks, parse_description)
                    
                    st.success("✨ Content parsed successfully!")
                    st.markdown('<div class="content-card">', unsafe_allow_html=True)
                    st.markdown("### 📊 Results")
                    st.markdown(result)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
            except Exception as e:
                st.error(f"❌ Error parsing content: {str(e)}")

    # Footer
    st.markdown("""
        <div style="position: fixed; bottom: 0; left: 0; right: 0; text-align: center; padding: 1rem; background: rgba(0,0,0,0.5);">
            <p style="color: #ffffff; margin: 0;">Made with ❤️ by Omar Alian</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()