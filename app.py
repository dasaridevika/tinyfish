import streamlit as st
import os
import json
import time
import pandas as pd
from datetime import datetime, timezone
from urllib.parse import urlparse
from dotenv import load_dotenv

# Load environment variables if .env exists locally
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="TinyFish Keyword Monitor",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Persistence store for saved monitors and match history
DATA_FILE = "monitors_store.json"

def load_store():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"monitors": [], "seen_urls": {}}

def save_store(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception:
        pass

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
        margin-bottom: 1.8rem;
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
        padding: 1.4rem;
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
    
    .badge-new {
        background: linear-gradient(135deg, #10B981, #059669);
        color: #FFFFFF !important;
        font-size: 0.75rem;
        font-weight: 800;
        padding: 3px 9px;
        border-radius: 6px;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        box-shadow: 0 2px 6px rgba(16, 185, 129, 0.35);
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
    }
    
    .date-badge {
        background: #FFFBEB;
        color: #B45309 !important;
        border: 1px solid #FDE68A;
        font-size: 0.78rem;
        font-weight: 600;
        padding: 3px 8px;
        border-radius: 6px;
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
    
    /* Submit Button Theme Styling */
    div.stButton > button:first-child, div.stFormSubmitButton > button:first-child {
        background: linear-gradient(135deg, #4F46E5 0%, #6366F1 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        padding: 0.6rem 1.5rem !important;
        box-shadow: 0 4px 14px rgba(79, 70, 229, 0.3) !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button:first-child:hover, div.stFormSubmitButton > button:first-child:hover {
        background: linear-gradient(135deg, #4338CA 0%, #4F46E5 100%) !important;
        box-shadow: 0 6px 18px rgba(79, 70, 229, 0.45) !important;
        transform: translateY(-1px) !important;
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

# Read API Key from Streamlit Secrets or Environment Variables
api_key = ""
try:
    if hasattr(st, "secrets") and "TINYFISH_API_KEY" in st.secrets:
        api_key = str(st.secrets["TINYFISH_API_KEY"]).strip()
except Exception:
    pass

if not api_key:
    api_key = os.getenv("TINYFISH_API_KEY", "").strip()

# Header Hero Section
st.markdown("""
<div class="hero-container">
    <div class="hero-badge">AI Web Intelligence & Monitor</div>
    <div class="hero-title">TinyFish Keyword Monitor</div>
</div>
""", unsafe_allow_html=True)

# Load existing store
store_data = load_store()

# Collapsible Saved Monitors Dashboard
with st.expander(f"📁 Manage Saved Monitors ({len(store_data.get('monitors', []))} active)", expanded=False):
    saved_monitors = store_data.get("monitors", [])
    if not saved_monitors:
        st.info("No saved monitors yet. Create one below by checking 'Save this as a Monitor'!")
    else:
        for idx, mon in enumerate(saved_monitors):
            c_name, c_query, c_dur, c_btn = st.columns([2, 3, 2, 2])
            c_name.write(f"**{mon.get('name')}**")
            c_query.caption(f"🔑 `{mon.get('query')}`")
            c_dur.caption(f"⏱️ {mon.get('duration_label', 'All Time')}")
            
            c_del, c_run = c_btn.columns(2)
            if c_run.button("▶️ Run", key=f"run_mon_{idx}", use_container_width=True):
                st.session_state["active_query"] = mon.get("query")
                st.session_state["active_goal"] = mon.get("goal")
                st.session_state["active_url"] = mon.get("url", "")
                st.session_state["active_dur"] = mon.get("duration_minutes")
                st.session_state["trigger_search"] = True
                st.rerun()
                
            if c_del.button("🗑️", key=f"del_mon_{idx}", use_container_width=True):
                saved_monitors.pop(idx)
                store_data["monitors"] = saved_monitors
                save_store(store_data)
                st.rerun()

# Input Form
with st.form("search_form", border=True):
    st.subheader("Configure Search & Monitor")
    
    goal_input = st.text_area(
        "Main Goal / Search Intent",
        value=st.session_state.get("active_goal", ""),
        placeholder="e.g. Complete step-by-step course roadmap, beginner to advanced syllabus, and tutorial guides",
        height=85,
        help="Describe what you are looking for in plain English. Used for neural intent ranking."
    )
    
    col1, col2 = st.columns([1, 1])
    with col1:
        query_input = st.text_input(
            "Keywords / Target Query",
            value=st.session_state.get("active_query", ""),
            placeholder="e.g. Python, AI agents, React.js, Full Stack",
            help="Keywords or topics to search."
        )
    with col2:
        url_input = st.text_input(
            "Target URL (Optional)",
            value=st.session_state.get("active_url", ""),
            placeholder="e.g. https://roadmap.sh/python (Leave blank for web search)",
            help="If provided, TinyFish will deploy an autonomous web agent to deep-scrape this specific URL."
        )
    
    col3, col4, col5 = st.columns(3)
    with col3:
        search_mode = st.selectbox(
            "🧠 Search Mode",
            ["Neural / Semantic (Exa Mode)", "Exact Keyword Match"],
            help="Neural Mode optimizes queries to find high-authority roadmaps, guides, and syllabi matching your intent."
        )
        
    with col4:
        duration_options = [
            ("Any Time (All History)", None),
            ("Past 24 Hours", 1440),
            ("Past 7 Days", 10080),
            ("Past 30 Days", 43200),
            ("Past 1 Hour", 60)
        ]
        duration_option = st.selectbox(
            "⏱️ Time Duration / Freshness",
            duration_options,
            format_func=lambda x: x[0]
        )
        recency_minutes_val = duration_option[1]
        
    with col5:
        category_preset = st.selectbox(
            "🎯 Source Domain Category",
            [
                "All Web (Comprehensive)",
                "🎓 Roadmaps & Courses (roadmap.sh, GitHub, FreeCodeCamp, Coursera, Dev.to)",
                "💼 Tech & Developer News (GitHub, HackerNews, ProductHunt, Medium)",
                "Custom Specific Domains"
            ]
        )
        
    custom_domains_input = ""
    if category_preset == "Custom Specific Domains":
        custom_domains_input = st.text_input(
            "Enter Specific Domains (comma-separated)",
            placeholder="e.g. roadmap.sh, github.com, coursera.org"
        )

    # Save as Monitor option
    col_save1, col_save2 = st.columns([1, 2])
    save_as_monitor = col_save1.checkbox("💾 Save this as a Monitor", value=False)
    monitor_name = col_save2.text_input("Monitor Name", placeholder="e.g. Python Roadmap Watcher", label_visibility="collapsed") if save_as_monitor else ""

    search_submitted = st.form_submit_button("🚀 Find Exact Results", type="primary", use_container_width=True)

# Check if triggered via form or saved monitor button
if st.session_state.get("trigger_search", False):
    search_submitted = True
    st.session_state["trigger_search"] = False

# Process Search
if search_submitted:
    if not goal_input.strip() or not query_input.strip():
        st.warning("Please enter both your **Main Goal** and **Keywords / Query**.")
    else:
        kw_list = [k.strip() for k in query_input.split(",") if k.strip()]
        
        # Save monitor if selected
        if save_as_monitor and monitor_name.strip():
            existing_names = [m.get("name") for m in store_data.get("monitors", [])]
            if monitor_name.strip() not in existing_names:
                store_data["monitors"].append({
                    "name": monitor_name.strip(),
                    "goal": goal_input.strip(),
                    "query": query_input.strip(),
                    "url": url_input.strip(),
                    "duration_label": duration_option[0],
                    "duration_minutes": recency_minutes_val,
                    "created_at": datetime.now(timezone.utc).isoformat()
                })
                save_store(store_data)
                st.success(f"Monitor '{monitor_name.strip()}' saved successfully!")

        with st.status("Executing Search with Exa-style Precision...", expanded=True) as status:
            st.write(f"Goal: **{goal_input}**")
            st.write(f"Keywords: **{query_input}**")
            st.write(f"Mode: **{search_mode}**")
            
            highlights = []
            summary = ""
            
            # Resolve domains
            resolved_domains = None
            if category_preset.startswith("🎓"):
                resolved_domains = "roadmap.sh,github.com,freecodecamp.org,coursera.org,dev.to,towardsdatascience.com"
            elif category_preset.startswith("💼"):
                resolved_domains = "github.com,news.ycombinator.com,producthunt.com,medium.com,techcrunch.com"
            elif category_preset == "Custom Specific Domains" and custom_domains_input.strip():
                resolved_domains = custom_domains_input.strip()
                
            # Build Exa-style optimized query
            if "Neural" in search_mode:
                # Synthesize intent + keywords into authoritative roadmap/guide search
                goal_lower = goal_input.lower()
                intent_keywords = []
                if "roadmap" in goal_lower or "curriculum" in goal_lower or "syllabus" in goal_lower:
                    intent_keywords.append("roadmap")
                    intent_keywords.append("syllabus")
                if "tutorial" in goal_lower or "guide" in goal_lower:
                    intent_keywords.append("complete guide")
                    
                final_query = f"{' '.join(kw_list)} {' '.join(intent_keywords)}".strip()
                if not final_query:
                    final_query = query_input
                purpose_prompt = f"Find authoritative, structured learning roadmaps, curricula, and step-by-step guides for: {query_input}"
            else:
                final_query = " ".join([f'"{k}"' if " " in k else k for k in kw_list])
                purpose_prompt = goal_input.strip()

            if api_key and not api_key.startswith("your_"):
                try:
                    from tinyfish import TinyFish
                    client = TinyFish(api_key=api_key)
                    
                    if url_input.strip():
                        # Deep Autonomous Agent on Target URL
                        st.write(f"Deploying Web Agent to `{url_input.strip()}`...")
                        prompt = f"Goal: {goal_input}. Keywords: {query_input}. Extract complete roadmap stages, topics, and structured syllabus from this page."
                        resp = client.agent.run(url=url_input.strip(), goal=prompt)
                        
                        raw_result = resp.result if hasattr(resp, "result") else str(resp)
                        summary = f"Autonomous Web Agent analyzed {url_input.strip()} for '{query_input}'."
                        highlights = [{
                            "title": f"Extracted Findings from {get_domain(url_input.strip())}",
                            "context": str(raw_result),
                            "url": url_input.strip(),
                            "published_date": None
                        }]
                    else:
                        st.write("Executing live search query...")
                        search_resp = client.search.query(
                            query=final_query,
                            purpose=purpose_prompt,
                            recency_minutes=recency_minutes_val,
                            include_domains=resolved_domains
                        )
                        
                        results_list = getattr(search_resp, "results", [])
                        duration_label = f" within {duration_option[0]}" if recency_minutes_val else ""
                        summary = f"Found {len(results_list)} high-precision results matching '{query_input}'{duration_label}."
                        
                        for item in results_list:
                            title = getattr(item, "title", "Result")
                            snippet = getattr(item, "snippet", "")
                            link = getattr(item, "url", "#")
                            pub_date = getattr(item, "published_date", None)
                            highlights.append({
                                "title": title,
                                "context": snippet,
                                "url": link,
                                "published_date": pub_date
                            })
                            
                    status.update(label="Search completed with high precision!", state="complete", expanded=False)
                except Exception as e:
                    status.update(label="Search encountered an error", state="error")
                    st.error(f"TinyFish Error: {e}")
                    summary = "Execution failed."
            else:
                # Simulation fallback mode
                time.sleep(1.0)
                summary = f"Simulated high-precision results for '{query_input}' ({duration_option[0]})."
                highlights = [
                    {
                        "title": f"Official {query_input.title()} Developer Roadmap (2026)",
                        "context": f"Complete sequential learning path for {query_input}. Step-by-step breakdown covering fundamentals, advanced architectural patterns, frameworks, and milestone projects.",
                        "url": "https://roadmap.sh/python" if "python" in query_input.lower() else "https://roadmap.sh",
                        "published_date": "2026-09-01"
                    },
                    {
                        "title": f"The Complete {query_input.title()} Syllabus & Curriculum",
                        "context": f"In-depth guide with structured weekly modules, prerequisites, hands-on repository projects, and recommended resources for mastering {query_input}.",
                        "url": "https://github.com/freeCodeCamp/freeCodeCamp",
                        "published_date": "2026-08-28"
                    },
                    {
                        "title": f"Building End-to-End {query_input.title()} Applications",
                        "context": f"Authoritative guide from industry practitioners detailing best practices, tools, and modern workflows for {query_input}.",
                        "url": "https://towardsdatascience.com",
                        "published_date": "2026-08-15"
                    }
                ]
                status.update(label="Results ready!", state="complete", expanded=False)

        # Diff & Change Detection: Identify New Matches
        seen_urls_map = store_data.setdefault("seen_urls", {})
        query_seen = set(seen_urls_map.get(query_input.strip(), []))
        
        new_count = 0
        for item in highlights:
            u = item.get("url", "")
            if u and u not in query_seen:
                item["is_new"] = True
                new_count += 1
                query_seen.add(u)
            else:
                item["is_new"] = False
                
        seen_urls_map[query_input.strip()] = list(query_seen)
        save_store(store_data)

        # Render Results Section
        st.write("")
        st.subheader("📋 Search & Monitor Results")
        
        col_res1, col_res2 = st.columns([3, 1])
        with col_res1:
            st.markdown(f"""
            <div class="summary-box">
                <strong>Summary:</strong> {summary}
            </div>
            """, unsafe_allow_html=True)
        with col_res2:
            st.metric("New Detections", new_count, delta=f"+{new_count} New" if new_count > 0 else "0 New")

        if highlights:
            for idx, item in enumerate(highlights, 1):
                title = item.get("title", f"Result #{idx}")
                context = item.get("context", "")
                url = item.get("url", "#")
                pub_date = item.get("published_date")
                is_new = item.get("is_new", False)
                domain = get_domain(url)
                
                date_html = f'<span class="date-badge">📅 {str(pub_date)[:10]}</span>' if pub_date else ''
                new_badge_html = '<span class="badge-new">NEW</span>' if is_new else ''
                
                st.markdown(f"""
                <div class="card-container">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.6rem; flex-wrap: wrap; gap: 6px;">
                        <div class="card-title">{title} {new_badge_html}</div>
                        <div style="display: flex; gap: 6px; align-items: center;">
                            {date_html}
                            <span class="domain-badge">{domain}</span>
                        </div>
                    </div>
                    <div class="card-snippet">{context}</div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 0.8rem; flex-wrap: wrap; gap: 8px;">
                        <div style="display: flex; flex-wrap: wrap; gap: 6px;">
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
                    "📥 Export Results as CSV",
                    data=df_export.to_csv(index=False),
                    file_name="tinyfish_monitor_results.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            with col_e2:
                with st.expander("🔍 View Raw JSON"):
                    st.json(highlights)
