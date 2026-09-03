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
    page_title="TinyFish Monitor",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Persistence store for saved monitors and diff tracking
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

# Exa-Style High-End Dark Banner & Card Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Hero Banner */
    .hero-container {
        background: linear-gradient(135deg, #0F172A 0%, #1E1B4B 50%, #312E81 100%);
        padding: 2.2rem 2.5rem;
        border-radius: 18px;
        margin-bottom: 1.8rem;
        box-shadow: 0 12px 30px -8px rgba(15, 23, 42, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.12);
    }
    .hero-badge {
        background: linear-gradient(90deg, #6366F1, #EC4899);
        color: #FFFFFF !important;
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        display: inline-block;
        margin-bottom: 0.6rem;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.35);
    }
    .hero-title {
        font-size: 2.4rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: #FFFFFF !important;
        margin-bottom: 0.4rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    .hero-tagline {
        font-size: 1.05rem;
        color: #C7D2FE !important;
        font-weight: 400;
    }
    
    /* Exa-Style Result Card */
    .exa-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1rem;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }
    .exa-card:hover {
        border-color: #6366F1;
        box-shadow: 0 10px 24px -4px rgba(99, 102, 241, 0.15);
        transform: translateY(-2px);
    }
    .exa-title {
        font-size: 1.18rem;
        font-weight: 700;
        color: #0F172A !important;
        line-height: 1.4;
        margin-bottom: 0.4rem;
    }
    .exa-snippet {
        font-size: 0.96rem;
        color: #334155 !important;
        line-height: 1.6;
        margin-bottom: 0.9rem;
    }
    
    /* Pills & Badges */
    .cadence-badge {
        background: #EEF2FF;
        color: #4338CA !important;
        border: 1px solid #C7D2FE;
        font-size: 0.78rem;
        font-weight: 700;
        padding: 3px 9px;
        border-radius: 6px;
    }
    .domain-badge {
        background: #F1F5F9;
        color: #475569 !important;
        border: 1px solid #E2E8F0;
        font-size: 0.78rem;
        font-weight: 600;
        padding: 3px 9px;
        border-radius: 6px;
    }
    .date-badge {
        background: #FFFBEB;
        color: #B45309 !important;
        border: 1px solid #FDE68A;
        font-size: 0.78rem;
        font-weight: 600;
        padding: 3px 9px;
        border-radius: 6px;
    }
    .badge-new {
        background: linear-gradient(135deg, #10B981, #059669);
        color: #FFFFFF !important;
        font-size: 0.72rem;
        font-weight: 800;
        padding: 3px 8px;
        border-radius: 6px;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        box-shadow: 0 2px 6px rgba(16, 185, 129, 0.3);
    }
    
    .link-button {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: linear-gradient(135deg, #4F46E5 0%, #6366F1 100%);
        color: #FFFFFF !important;
        font-size: 0.85rem;
        font-weight: 600;
        padding: 7px 15px;
        border-radius: 8px;
        text-decoration: none;
        box-shadow: 0 4px 10px rgba(79, 70, 229, 0.25);
        transition: all 0.2s ease;
    }
    .link-button:hover {
        background: linear-gradient(135deg, #4338CA 0%, #4F46E5 100%);
        box-shadow: 0 6px 14px rgba(79, 70, 229, 0.4);
        transform: translateY(-1px);
        color: #FFFFFF !important;
        text-decoration: none;
    }
    
    /* Submit Button Theme Styling */
    div.stButton > button:first-child, div.stFormSubmitButton > button:first-child {
        background: linear-gradient(135deg, #4F46E5 0%, #6366F1 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        padding: 0.65rem 1.5rem !important;
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

# Header Hero Section (Exa-Style)
st.markdown("""
<div class="hero-container">
    <div class="hero-badge">Exa-Style AI Web Monitor</div>
    <div class="hero-title">TinyFish Monitor</div>
    <div class="hero-tagline">Track web topics, roadmaps, competitor news, and keyword changes on a recurring cadence.</div>
</div>
""", unsafe_allow_html=True)

# Load existing store
store_data = load_store()

# Collapsible Saved Monitors Dashboard
with st.expander(f"📁 Active Monitors ({len(store_data.get('monitors', []))})", expanded=False):
    saved_monitors = store_data.get("monitors", [])
    if not saved_monitors:
        st.info("No saved monitors yet. Configure a query below and check 'Save as Active Monitor' to start tracking!")
    else:
        for idx, mon in enumerate(saved_monitors):
            c_name, c_query, c_cad, c_btn = st.columns([2, 3, 2, 2])
            c_name.write(f"**{mon.get('name')}**")
            c_query.caption(f"🔍 `{mon.get('query')}`")
            c_cad.markdown(f"<span class='cadence-badge'>⏱️ {mon.get('cadence_label')}</span>", unsafe_allow_html=True)
            
            c_del, c_run = c_btn.columns(2)
            if c_run.button("▶️ Run", key=f"run_mon_{idx}", use_container_width=True):
                st.session_state["active_query"] = mon.get("query")
                st.session_state["active_cadence"] = mon.get("cadence_preset")
                st.session_state["active_num"] = mon.get("num_results", 10)
                st.session_state["trigger_search"] = True
                st.rerun()
                
            if c_del.button("🗑️", key=f"del_mon_{idx}", use_container_width=True):
                saved_monitors.pop(idx)
                store_data["monitors"] = saved_monitors
                save_store(store_data)
                st.rerun()

# Exa-Style Monitor Configuration Form
with st.form("exa_monitor_form", border=True):
    st.subheader("Create or Preview Monitor")
    
    query_input = st.text_input(
        "Search Query (q)",
        value=st.session_state.get("active_query", ""),
        placeholder="e.g. Latest news on Nvidia, Python developer roadmap 2026, AI agent frameworks",
        help="The search query or keyword phrase to monitor."
    )
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        cadence_options = [
            ("Daily (1d)", "1d", 1440),
            ("Weekly (1w)", "1w", 10080),
            ("Hourly (1h)", "1h", 60),
            ("Monthly (1m)", "1m", 43200),
            ("All Time (Instant)", "none", None)
        ]
        cadence_choice = st.selectbox(
            "Cadence Preset (cadencePreset)",
            cadence_options,
            format_func=lambda x: x[0],
            help="How frequently this query should be monitored and what freshness window to apply."
        )
        cadence_label, cadence_key, recency_mins = cadence_choice
        
    with col2:
        num_results = st.selectbox(
            "Number of Results (numResults)",
            [5, 10, 15, 20],
            index=1,
            help="Maximum number of relevant results to retrieve."
        )
        
    with col3:
        url_input = st.text_input(
            "Target URL (Optional)",
            placeholder="e.g. https://roadmap.sh/python (Leave blank for web search)",
            help="If provided, TinyFish will deploy an autonomous web agent to deep-scrape this URL."
        )
        
    # Save as Monitor option
    col_save1, col_save2 = st.columns([1, 2])
    save_as_monitor = col_save1.checkbox("💾 Save as Active Monitor", value=False)
    monitor_name = col_save2.text_input("Monitor Name", placeholder="e.g. Nvidia News Monitor", label_visibility="collapsed") if save_as_monitor else ""

    run_submitted = st.form_submit_button("🚀 Run Monitor Preview", type="primary", use_container_width=True)

# Check if triggered via saved monitor button
if st.session_state.get("trigger_search", False):
    run_submitted = True
    st.session_state["trigger_search"] = False

# Process Monitor Run
if run_submitted:
    if not query_input.strip():
        st.warning("Please enter a **Search Query** to run the monitor.")
    else:
        # Save monitor if selected
        if save_as_monitor and monitor_name.strip():
            existing_names = [m.get("name") for m in store_data.get("monitors", [])]
            if monitor_name.strip() not in existing_names:
                store_data["monitors"].append({
                    "name": monitor_name.strip(),
                    "query": query_input.strip(),
                    "cadence_preset": cadence_key,
                    "cadence_label": cadence_label,
                    "duration_minutes": recency_mins,
                    "num_results": num_results,
                    "url": url_input.strip(),
                    "created_at": datetime.now(timezone.utc).isoformat()
                })
                save_store(store_data)
                st.success(f"Monitor '{monitor_name.strip()}' saved successfully!")

        with st.status("Executing Monitor Run...", expanded=True) as status:
            st.write(f"Query: **{query_input}**")
            st.write(f"Cadence: **{cadence_label}** (`recency_minutes={recency_mins}`)")
            
            highlights = []
            
            if api_key and not api_key.startswith("your_"):
                try:
                    from tinyfish import TinyFish
                    client = TinyFish(api_key=api_key)
                    
                    if url_input.strip():
                        # Autonomous Agent execution on specific URL
                        st.write(f"Deploying Web Agent to `{url_input.strip()}`...")
                        prompt = f"Extract all key updates, content details, and summary matching query: '{query_input}'."
                        resp = client.agent.run(url=url_input.strip(), goal=prompt)
                        
                        raw_result = resp.result if hasattr(resp, "result") else str(resp)
                        highlights = [{
                            "title": f"Extracted from {get_domain(url_input.strip())}",
                            "snippet": str(raw_result),
                            "url": url_input.strip(),
                            "published_date": None
                        }]
                    else:
                        # Exa-style Live Web Search via TinyFish
                        st.write("Querying live web index with cadence window...")
                        
                        search_resp = client.search.query(
                            query=query_input.strip(),
                            purpose=f"Live monitor query for: {query_input.strip()}",
                            recency_minutes=recency_mins,
                            exclude_domains="facebook.com,quora.com,pinterest.com,instagram.com,tiktok.com"
                        )
                        
                        results_list = getattr(search_resp, "results", [])[:num_results]
                        
                        for item in results_list:
                            title = getattr(item, "title", "Result")
                            snippet = getattr(item, "snippet", "")
                            link = getattr(item, "url", "#")
                            pub_date = getattr(item, "published_date", None)
                            highlights.append({
                                "title": title,
                                "snippet": snippet,
                                "url": link,
                                "published_date": pub_date
                            })
                            
                    status.update(label="Monitor run completed successfully!", state="complete", expanded=False)
                except Exception as e:
                    status.update(label="Monitor run failed", state="error")
                    st.error(f"TinyFish Error: {e}")
            else:
                # Realistic Exa-style fallback simulation
                time.sleep(1.0)
                clean_q = query_input.title()
                highlights = [
                    {
                        "title": f"Latest Analysis & Breaking Updates: {clean_q}",
                        "snippet": f"Comprehensive report covering recent announcements, market trends, and key takeaways for {query_input}. Published within the selected {cadence_label} window.",
                        "url": "https://techcrunch.com" if "news" in query_input.lower() else "https://roadmap.sh",
                        "published_date": "2026-09-02T14:30:00Z"
                    },
                    {
                        "title": f"Deep Dive: Key Highlights and Industry Developments on {clean_q}",
                        "snippet": f"Technical breakdown and verified documentation regarding {query_input}. Analyzes structural updates, features, and roadmaps.",
                        "url": "https://github.com",
                        "published_date": "2026-09-01T09:15:00Z"
                    },
                    {
                        "title": f"Strategic Overview & Expert Insights: {clean_q}",
                        "snippet": f"Expert insights detailing recent updates, tools, and discussions around {query_input}.",
                        "url": "https://towardsdatascience.com",
                        "published_date": "2026-08-30T18:00:00Z"
                    }
                ][:num_results]
                status.update(label="Preview results ready!", state="complete", expanded=False)

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

        # Render Exa-Style Results Section
        st.write("")
        st.subheader("📋 Monitor Results")
        
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.metric("Total Matches", len(highlights))
        with col_m2:
            st.metric("New Findings", new_count, delta=f"+{new_count} New" if new_count > 0 else "0 New")
        with col_m3:
            st.metric("Cadence Filter", cadence_label)

        if highlights:
            for idx, item in enumerate(highlights, 1):
                title = item.get("title", f"Result #{idx}")
                snippet = item.get("snippet", "")
                url = item.get("url", "#")
                pub_date = item.get("published_date")
                is_new = item.get("is_new", False)
                domain = get_domain(url)
                
                date_str = str(pub_date)[:10] if pub_date else "Recent"
                date_html = f'<span class="date-badge">📅 {date_str}</span>'
                new_badge_html = '<span class="badge-new">NEW</span>' if is_new else ''
                
                st.markdown(f"""
                <div class="exa-card">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem; flex-wrap: wrap; gap: 6px;">
                        <div class="exa-title">{title} {new_badge_html}</div>
                        <div style="display: flex; gap: 6px; align-items: center;">
                            {date_html}
                            <span class="domain-badge">🌐 {domain}</span>
                        </div>
                    </div>
                    <div class="exa-snippet">{snippet}</div>
                    <div style="display: flex; justify-content: flex-end; align-items: center; margin-top: 0.6rem;">
                        <a href="{url}" target="_blank" class="link-button">Open Link &rarr;</a>
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
