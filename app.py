import streamlit as st
import os
import time
import pandas as pd
from urllib.parse import urlparse
from dotenv import load_dotenv

# Load API key from .env or .env.example
load_dotenv(".env")
load_dotenv(".env.example")

# Page configuration
st.set_page_config(
    page_title="TinyFish Keyword Finder",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom High-End Styling & Colorful Professional Palette
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Hero Banner */
    .hero-container {
        background: linear-gradient(135deg, #1E1B4B 0%, #312E81 40%, #4338CA 100%);
        padding: 2rem 2.5rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 12px 30px -8px rgba(49, 46, 129, 0.35);
        border: 1px solid rgba(255, 255, 255, 0.15);
    }
    .hero-badge {
        background: linear-gradient(90deg, #EC4899, #8B5CF6);
        color: #FFFFFF !important;
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        display: inline-block;
        margin-bottom: 0.6rem;
        box-shadow: 0 4px 12px rgba(236, 72, 153, 0.3);
    }
    .hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: #FFFFFF !important;
        margin-bottom: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    /* Result Card Styling */
    .card-container {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-left: 5px solid #6366F1;
        border-radius: 14px;
        padding: 1.5rem;
        margin-bottom: 1.2rem;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 12px -2px rgba(0, 0, 0, 0.05);
    }
    .card-container:hover {
        border-color: #818CF8;
        border-left: 5px solid #4F46E5;
        box-shadow: 0 12px 28px -4px rgba(79, 70, 229, 0.15);
        transform: translateY(-3px);
    }
    
    .card-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #0F172A !important;
        margin-bottom: 0.5rem;
        line-height: 1.4;
    }
    .card-snippet {
        font-size: 0.98rem;
        color: #334155 !important;
        line-height: 1.6;
        margin-bottom: 1rem;
    }
    
    /* Colorful Badges & Pills */
    .domain-badge {
        background: #F0FDF4;
        color: #15803D !important;
        border: 1px solid #BBF7D0;
        font-size: 0.8rem;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 8px;
        display: inline-flex;
        align-items: center;
        gap: 5px;
    }
    
    .kw-chip {
        background: #EEF2FF;
        color: #4338CA !important;
        border: 1px solid #C7D2FE;
        font-size: 0.8rem;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 8px;
        display: inline-block;
        margin-right: 6px;
    }
    
    .link-button {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: linear-gradient(135deg, #4F46E5 0%, #6366F1 100%);
        color: #FFFFFF !important;
        font-size: 0.88rem;
        font-weight: 600;
        padding: 8px 16px;
        border-radius: 10px;
        text-decoration: none;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.25);
        transition: all 0.2s ease;
    }
    .link-button:hover {
        background: linear-gradient(135deg, #4338CA 0%, #4F46E5 100%);
        box-shadow: 0 6px 16px rgba(79, 70, 229, 0.4);
        transform: translateY(-1px);
        color: #FFFFFF !important;
        text-decoration: none;
    }

    .summary-box {
        background: linear-gradient(135deg, #EFF6FF 0%, #F5F3FF 100%);
        border: 1px solid #C7D2FE;
        border-radius: 12px;
        padding: 1.2rem 1.4rem;
        color: #1E1B4B;
        font-size: 1.02rem;
        font-weight: 500;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Helper function to extract domain
def get_domain(url_str: str) -> str:
    try:
        parsed = urlparse(url_str)
        return parsed.netloc or "web"
    except Exception:
        return "web"

# Read API Key from environment (.env / .env.example)
api_key = os.getenv("TINYFISH_API_KEY", "").strip()

# Header Hero Section
st.markdown("""
<div class="hero-container">
    <div class="hero-badge">AI Web Intelligence</div>
    <div class="hero-title">TinyFish Keyword Finder</div>
</div>
""", unsafe_allow_html=True)

# Input Form
with st.form("search_form", border=True):
    st.subheader("Define Your Search")
    
    goal_input = st.text_area(
        "Main Goal",
        placeholder="e.g. Find complete course roadmaps, beginner guides, and tutorials for learning AI agents with Python",
        height=90,
        help="Describe what information or outcome you want extracted in plain English."
    )
    
    col1, col2 = st.columns([1, 1])
    with col1:
        kw_input = st.text_input(
            "Keywords",
            placeholder="e.g. Python, AI agents, LangChain (comma-separated)"
        )
    with col2:
        url_input = st.text_input(
            "Target URL (Optional)",
            placeholder="Leave blank to search the web, or enter a specific website"
        )
    
    search_submitted = st.form_submit_button("Find Results", type="primary", use_container_width=True)

# Process Search
if search_submitted:
    if not goal_input.strip() or not kw_input.strip():
        st.warning("Please enter both your **Main Goal** and **Keywords** to continue.")
    else:
        kw_list = [k.strip() for k in kw_input.split(",") if k.strip()]
        
        with st.status("Searching with TinyFish...", expanded=True) as status:
            st.write(f"Goal: **{goal_input}**")
            st.write(f"Keywords: **{', '.join(kw_list)}**")
            
            highlights = []
            summary = ""
            
            if api_key and not api_key.startswith("your_"):
                try:
                    from tinyfish import TinyFish
                    client = TinyFish(api_key=api_key)
                    
                    if url_input.strip():
                        st.write(f"Deploying Web Agent to `{url_input.strip()}`...")
                        prompt = f"Goal: {goal_input}. Find all mentions and detailed information regarding keywords: {kw_input}. Return structured summary and key highlights."
                        resp = client.agent.run(url=url_input.strip(), goal=prompt)
                        
                        raw_result = resp.result if hasattr(resp, "result") else str(resp)
                        summary = f"Agent successfully analyzed {url_input.strip()} for keywords [{kw_input}]."
                        highlights = [{
                            "title": f"Extracted Findings from {get_domain(url_input.strip())}",
                            "context": str(raw_result),
                            "url": url_input.strip()
                        }]
                    else:
                        st.write("Querying TinyFish live web search index...")
                        search_resp = client.search.query(
                            query=" ".join(kw_list),
                            purpose=goal_input
                        )
                        results_list = getattr(search_resp, "results", [])
                        summary = f"Found {len(results_list)} live web resources matching your goal."
                        
                        for item in results_list:
                            title = getattr(item, "title", "Result")
                            snippet = getattr(item, "snippet", "")
                            link = getattr(item, "url", "#")
                            highlights.append({
                                "title": title,
                                "context": snippet,
                                "url": link
                            })
                            
                    status.update(label="Search completed successfully!", state="complete", expanded=False)
                except Exception as e:
                    status.update(label="Search encountered an error", state="error")
                    st.error(f"TinyFish Error: {e}")
                    summary = "Execution failed."
            else:
                # Simulation fallback mode if no key provided
                time.sleep(1.0)
                summary = f"Simulated results for goal: '{goal_input}' and keywords [{kw_input}]."
                highlights = [
                    {
                        "title": f"Comprehensive Guide to {kw_list[0] if kw_list else 'Topic'}",
                        "context": f"Detailed resource covering core concepts and advanced workflows matching '{goal_input}'. Includes architectural patterns and hands-on examples.",
                        "url": url_input.strip() if url_input.strip() else "https://news.ycombinator.com"
                    },
                    {
                        "title": f"Community Showcase & Practical Implementations",
                        "context": f"Top developer discussions and tutorials highlighting best practices for {kw_input}.",
                        "url": url_input.strip() if url_input.strip() else "https://github.com"
                    }
                ]
                status.update(label="Simulated results ready!", state="complete", expanded=False)

        # Render Results Section
        st.write("")
        st.subheader("Extracted Results")
        
        st.markdown(f"""
        <div class="summary-box">
            <strong>Summary:</strong> {summary}
        </div>
        """, unsafe_allow_html=True)

        if highlights:
            for idx, item in enumerate(highlights, 1):
                title = item.get("title", f"Result #{idx}")
                context = item.get("context", "")
                url = item.get("url", "#")
                domain = get_domain(url)
                
                st.markdown(f"""
                <div class="card-container">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.6rem;">
                        <div class="card-title">{title}</div>
                        <span class="domain-badge">{domain}</span>
                    </div>
                    <div class="card-snippet">{context}</div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 0.8rem;">
                        <div>
                            {''.join([f'<span class="kw-chip">#{k}</span>' for k in kw_list])}
                        </div>
                        <a href="{url}" target="_blank" class="link-button">Open Source &rarr;</a>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Export options
            st.write("")
            df_export = pd.DataFrame(highlights)
            col_e1, col_e2 = st.columns(2)
            with col_e1:
                st.download_button(
                    "Export as CSV",
                    data=df_export.to_csv(index=False),
                    file_name="tinyfish_results.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            with col_e2:
                with st.expander("View Raw JSON"):
                    st.json(highlights)
