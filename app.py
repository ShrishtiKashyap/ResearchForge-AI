"""
ResearchForge AI  ·  app.py
Modern SaaS-style Streamlit UI for the multi-agent research pipeline.
Run: streamlit run app.py
"""

import streamlit as st
import time

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchForge AI",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Reset & base ── */
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp { background: #080b12; color: #dde3ee; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem 4rem 2.5rem !important; max-width: 900px; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #0d1117 !important;
    border-right: 1px solid #1a2234 !important;
    width: 290px !important;
}
section[data-testid="stSidebar"] > div { padding: 1.6rem 1.4rem !important; }

.sb-brand {
    display: flex; align-items: center; gap: 10px;
    padding-bottom: 1.4rem;
    border-bottom: 1px solid #1a2234;
    margin-bottom: 1.6rem;
}
.sb-brand-icon { font-size: 1.7rem; line-height:1; }
.sb-brand-name {
    font-size: 1.05rem; font-weight: 700; letter-spacing: -0.01em;
    background: linear-gradient(120deg, #818cf8, #38bdf8);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
}
.sb-brand-tag {
    font-size: 0.65rem; color: #3d5068; letter-spacing: 0.1em;
    text-transform: uppercase; margin-top: 1px;
}

.sb-label {
    font-size: 0.68rem; font-weight: 600; letter-spacing: 0.12em;
    text-transform: uppercase; color: #3d5068; margin-bottom: 0.5rem;
}

.sb-pipeline-list { margin-top: 1.8rem; }
.sb-step {
    display: flex; align-items: flex-start; gap: 10px;
    padding: 0.65rem 0;
    border-bottom: 1px solid #1a2234;
}
.sb-step:last-child { border-bottom: none; }
.sb-step-dot {
    width: 8px; height: 8px; border-radius: 50%;
    margin-top: 5px; flex-shrink: 0;
}
.sb-step-title { font-size: 0.8rem; font-weight: 600; color: #94a3b8; }
.sb-step-desc  { font-size: 0.7rem; color: #3d5068; margin-top: 1px; }

.sb-footer {
    margin-top: 2rem; padding-top: 1.2rem;
    border-top: 1px solid #1a2234;
    font-size: 0.68rem; color: #2d3f55; text-align: center;
}

/* ── Sidebar input ── */
.stTextArea textarea {
    background: #111827 !important;
    border: 1px solid #1e2d45 !important;
    border-radius: 10px !important;
    color: #dde3ee !important;
    font-size: 0.88rem !important;
    resize: vertical !important;
    font-family: 'Inter', sans-serif !important;
}
.stTextArea textarea:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px #6366f115 !important;
}
.stTextArea textarea::placeholder { color: #2d3f55 !important; }

/* ── Sidebar button ── */
div.stButton > button {
    background: linear-gradient(135deg, #6366f1 0%, #4f97d4 100%) !important;
    color: #fff !important; border: none !important;
    border-radius: 10px !important; font-weight: 600 !important;
    font-size: 0.88rem !important; padding: 0.6rem 1rem !important;
    width: 100% !important; letter-spacing: 0.01em !important;
    transition: opacity 0.18s, transform 0.15s !important;
}
div.stButton > button:hover  { opacity: 0.86 !important; transform: translateY(-1px) !important; }
div.stButton > button:active { transform: translateY(0) !important; }

/* ── Download button ── */
div.stDownloadButton > button {
    background: #111827 !important;
    color: #818cf8 !important; border: 1px solid #1e2d45 !important;
    border-radius: 8px !important; font-size: 0.82rem !important;
    font-weight: 500 !important; padding: 0.45rem 1rem !important;
    transition: border-color 0.2s !important;
}
div.stDownloadButton > button:hover { border-color: #6366f1 !important; }

/* ── Page hero ── */
.page-hero {
    padding: 0 0 2rem 0;
    border-bottom: 1px solid #1a2234;
    margin-bottom: 2rem;
}
.page-hero-title {
    font-size: 1.5rem; font-weight: 700; color: #dde3ee;
    letter-spacing: -0.02em; margin: 0 0 0.3rem 0;
}
.page-hero-sub { font-size: 0.85rem; color: #3d5068; margin: 0; }
.topic-pill {
    display: inline-block;
    background: #111827; border: 1px solid #1e2d45;
    border-radius: 20px; padding: 0.25rem 0.85rem;
    font-size: 0.82rem; color: #818cf8;
    font-weight: 500; margin-top: 0.7rem;
}

/* ── Progress tracker ── */
.tracker {
    display: flex; align-items: center;
    gap: 0; margin-bottom: 2.4rem;
}
.tracker-step {
    display: flex; flex-direction: column; align-items: center;
    flex: 1; position: relative;
}
.tracker-step:not(:last-child)::after {
    content: '';
    position: absolute; top: 16px; left: 50%; width: 100%;
    height: 2px; background: #1a2234; z-index: 0;
    transition: background 0.4s;
}
.tracker-step.done:not(:last-child)::after  { background: #4f46e5; }
.tracker-step.active:not(:last-child)::after { background: #1a2234; }

.tracker-circle {
    width: 32px; height: 32px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.75rem; font-weight: 700; z-index: 1;
    position: relative; transition: all 0.3s;
}
.tracker-circle.pending { background: #111827; border: 2px solid #1a2234; color: #2d3f55; }
.tracker-circle.active  { background: #1e1b4b; border: 2px solid #6366f1; color: #818cf8;
    box-shadow: 0 0 12px #6366f140; }
.tracker-circle.done    { background: #1e3a5f; border: 2px solid #38bdf8; color: #38bdf8; }
.tracker-circle.error   { background: #3b0f0f; border: 2px solid #f87171; color: #f87171; }

.tracker-label {
    font-size: 0.62rem; font-weight: 600; letter-spacing: 0.08em;
    text-transform: uppercase; margin-top: 6px; text-align: center;
}
.tracker-label.pending { color: #2d3f55; }
.tracker-label.active  { color: #818cf8; }
.tracker-label.done    { color: #38bdf8; }
.tracker-label.error   { color: #f87171; }

/* ── Step result card ── */
.result-card {
    background: #0d1117;
    border: 1px solid #1a2234;
    border-radius: 14px;
    margin-bottom: 1.2rem;
    overflow: hidden;
}
.result-card-header {
    display: flex; align-items: center; justify-content: space-between;
    padding: 0.9rem 1.2rem;
    border-bottom: 1px solid #1a2234;
}
.result-card-left { display: flex; align-items: center; gap: 10px; }
.result-card-icon {
    width: 32px; height: 32px; border-radius: 8px;
    display: flex; align-items: center; justify-content: center; font-size: 0.95rem;
}
.icon-search  { background: #1e1b4b; }
.icon-scrape  { background: #0c2742; }
.icon-report  { background: #0a2e1f; }
.icon-critic  { background: #2e1f04; }

.result-card-title { font-size: 0.88rem; font-weight: 600; color: #dde3ee; }
.result-card-meta  { font-size: 0.7rem; color: #3d5068; margin-top: 1px; }

.badge-ok   { background:#052e16; color:#4ade80; border:1px solid #166534;
    font-size:0.62rem; font-weight:700; letter-spacing:0.1em; text-transform:uppercase;
    padding:0.18rem 0.55rem; border-radius:20px; }
.badge-warn { background:#2c1600; color:#fbbf24; border:1px solid #92400e;
    font-size:0.62rem; font-weight:700; letter-spacing:0.1em; text-transform:uppercase;
    padding:0.18rem 0.55rem; border-radius:20px; }

.result-card-body { padding: 1.1rem 1.2rem; }

/* ── Content blocks ── */
.mono-block {
    background: #080b12; border: 1px solid #141d2e;
    border-radius: 8px; padding: 1rem 1.1rem;
    font-family: 'JetBrains Mono', monospace; font-size: 0.75rem;
    color: #64748b; line-height: 1.75;
    white-space: pre-wrap; word-break: break-word;
    max-height: 260px; overflow-y: auto;
}
.mono-block::-webkit-scrollbar { width: 5px; }
.mono-block::-webkit-scrollbar-track { background: transparent; }
.mono-block::-webkit-scrollbar-thumb { background: #1a2234; border-radius: 3px; }

/* ── Report card ── */
.report-card {
    background: #0d1117; border: 1px solid #1a2234;
    border-radius: 14px; overflow: hidden; margin-bottom: 1.2rem;
}
.report-card-header {
    display: flex; align-items: center; justify-content: space-between;
    padding: 1rem 1.4rem;
    background: linear-gradient(90deg, #0f172a 0%, #0d1117 100%);
    border-bottom: 1px solid #1a2234;
}
.report-card-title { font-size: 0.9rem; font-weight: 700; color: #dde3ee; display:flex; align-items:center; gap:8px; }
.report-card-body  { padding: 1.4rem 1.6rem; }

/* ── Critic card ── */
.critic-card {
    background: linear-gradient(135deg, #0e0c00 0%, #0d1117 100%);
    border: 1px solid #2e1f04; border-radius: 14px; overflow: hidden;
    margin-bottom: 1.2rem;
}
.critic-header {
    display: flex; align-items: center; gap: 10px;
    padding: 1rem 1.4rem; border-bottom: 1px solid #2e1f04;
}
.critic-header-text { font-size: 0.9rem; font-weight: 700; color: #fbbf24; }
.critic-body { padding: 1.2rem 1.4rem; font-size: 0.875rem; color: #a8946a; line-height: 1.8; }

/* ── Metrics strip ── */
.metrics-strip {
    display: flex; flex-wrap: wrap; gap: 0.7rem;
    margin-bottom: 2rem;
}
.metric-chip {
    background: #0d1117; border: 1px solid #1a2234;
    border-radius: 8px; padding: 0.45rem 0.85rem;
    font-size: 0.73rem; color: #3d5068;
    display: flex; align-items: center; gap: 0.4rem;
}
.metric-chip strong { color: #94a3b8; font-weight: 600; }

/* ── Empty state ── */
.empty-state {
    display: flex; flex-direction: column; align-items: center;
    justify-content: center; padding: 5rem 2rem; text-align: center;
}
.empty-icon { font-size: 2.8rem; margin-bottom: 1.2rem; opacity: 0.4; }
.empty-title { font-size: 1.05rem; font-weight: 600; color: #1e2d45; margin-bottom: 0.5rem; }
.empty-sub   { font-size: 0.82rem; color: #1a2234; }

/* ── Thinking pulse ── */
@keyframes pulse { 0%,100%{opacity:.4} 50%{opacity:1} }
.thinking {
    display: flex; align-items: center; gap: 8px;
    padding: 0.7rem 1rem;
    background: #0d1117; border: 1px solid #1e2d45;
    border-radius: 8px; margin-bottom: 0.8rem;
}
.thinking-dot {
    width: 7px; height: 7px; border-radius: 50%; background: #6366f1;
    animation: pulse 1.2s ease-in-out infinite;
}
.thinking-dot:nth-child(2) { animation-delay: 0.2s; background: #818cf8; }
.thinking-dot:nth-child(3) { animation-delay: 0.4s; background: #38bdf8; }
.thinking-text { font-size: 0.78rem; color: #3d5068; }

/* ── Expander override ── */
details > summary {
    background: #0d1117 !important;
    border: 1px solid #1a2234 !important;
    border-radius: 8px !important;
    color: #3d5068 !important;
    font-size: 0.78rem !important;
    padding: 0.55rem 0.9rem !important;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div class="sb-brand">
        <div class="sb-brand-icon">🔬</div>
        <div>
            <div class="sb-brand-name">ResearchForge AI</div>
            <div class="sb-brand-tag">Multi-Agent · Local LLM</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-label">Research Topic</div>', unsafe_allow_html=True)
    topic = st.text_area(
        label="topic_input",
        placeholder="e.g. Recent breakthroughs in quantum error correction",
        height=90,
        label_visibility="collapsed",
    )

    run_btn = st.button("⚡  Run Research", use_container_width=True)

    # Pipeline legend
    pipeline_steps = [
        ("#818cf8", "Web Search",       "Tavily API · live web"),
        ("#38bdf8", "Content Scraping", "BeautifulSoup · HTML → text"),
        ("#34d399", "Report Writing",   "LLM writer agent"),
        ("#f59e0b", "Critic Review",    "LLM critic agent"),
    ]
    st.markdown('<div class="sb-pipeline-list">', unsafe_allow_html=True)
    for color, title, desc in pipeline_steps:
        st.markdown(f"""
        <div class="sb-step">
            <div class="sb-step-dot" style="background:{color}"></div>
            <div>
                <div class="sb-step-title">{title}</div>
                <div class="sb-step-desc">{desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="sb-footer">Powered by Ollama · Tavily · LangChain</div>',
                unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# MAIN AREA
# ══════════════════════════════════════════════════════════════════════════════

# ── Empty state ────────────────────────────────────────────────────────────────
if not run_btn or not topic.strip():
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">🛰️</div>
        <div class="empty-title">No research session active</div>
        <div class="empty-sub">Enter a topic in the sidebar and click <strong>Run Research</strong> to begin.</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── Import pipeline ────────────────────────────────────────────────────────────
try:
    from pipeline import run_research_pipeline
except ImportError:
    st.error("**pipeline.py not found.** Place it alongside app.py and restart Streamlit.")
    st.stop()

# ── Hero ───────────────────────────────────────────────────────────────────────
clean_topic = topic.strip()
st.markdown(f"""
<div class="page-hero">
    <p class="page-hero-title">Research Session</p>
    <p class="page-hero-sub">Running 4-agent pipeline • results appear below as each step completes</p>
    <span class="topic-pill">🔎 {clean_topic}</span>
</div>
""", unsafe_allow_html=True)

# ── Progress tracker ───────────────────────────────────────────────────────────
STEP_LABELS = ["Search", "Scrape", "Report", "Critic"]

def render_tracker(current: int, error: bool = False):
    """current = 0-based index of step in progress (4 = all done)."""
    circles = ""
    for i, label in enumerate(STEP_LABELS):
        if i < current:
            cls = "done";    symbol = "✓"
        elif i == current and not error:
            cls = "active";  symbol = str(i + 1)
        elif i == current and error:
            cls = "error";   symbol = "✕"
        else:
            cls = "pending"; symbol = str(i + 1)
        circles += f"""
        <div class="tracker-step {cls}">
            <div class="tracker-circle {cls}">{symbol}</div>
            <div class="tracker-label {cls}">{label}</div>
        </div>"""
    st.markdown(f'<div class="tracker">{circles}</div>', unsafe_allow_html=True)

tracker_ph = st.empty()
tracker_ph.markdown("")  # placeholder

# ── Run the pipeline with per-step UI ─────────────────────────────────────────
state       = {}
start_ts    = time.time()
run_error   = None

# Placeholders for live step feedback
step_ph = st.empty()

def show_thinking(msg: str):
    step_ph.markdown(f"""
    <div class="thinking">
        <div class="thinking-dot"></div>
        <div class="thinking-dot"></div>
        <div class="thinking-dot"></div>
        <div class="thinking-text">{msg}</div>
    </div>
    """, unsafe_allow_html=True)

# We monkey-patch pipeline's agents at runtime to capture intermediate state.
# Because run_research_pipeline() is synchronous and returns everything at once,
# we simulate per-step progress: show thinking → run full pipeline → render results.

with tracker_ph:
    render_tracker(0)

show_thinking("Querying Tavily for live web results…")
time.sleep(0.3)  # let the thinking state render

try:
    with tracker_ph:
        render_tracker(0)
    show_thinking("Querying Tavily for live web results…")

    state = run_research_pipeline(clean_topic)

    elapsed = round(time.time() - start_ts, 1)

except Exception as exc:
    run_error = exc
    step_ph.empty()
    with tracker_ph:
        render_tracker(0, error=True)
    st.error(f"**Pipeline error:** {exc}")
    st.stop()

# All steps done — clear thinking indicator
step_ph.empty()
with tracker_ph:
    render_tracker(4)   # all complete

elapsed = round(time.time() - start_ts, 1)

# ── Metrics strip ──────────────────────────────────────────────────────────────
sr_len = len(state.get("search_results", ""))
sc_len = len(state.get("scraped_content", ""))
rp_len = len(state.get("report", ""))
fb_len = len(state.get("feedback", ""))

st.markdown(f"""
<div class="metrics-strip">
    <div class="metric-chip">⏱ <strong>{elapsed}s</strong> total</div>
    <div class="metric-chip">🔍 Search <strong>{sr_len:,} chars</strong></div>
    <div class="metric-chip">📄 Scraped <strong>{sc_len:,} chars</strong></div>
    <div class="metric-chip">📝 Report <strong>{rp_len:,} chars</strong></div>
    <div class="metric-chip">🧐 Critic <strong>{fb_len:,} chars</strong></div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# STEP RESULT CARDS
# ══════════════════════════════════════════════════════════════════════════════

sr = state.get("search_results", "No search results returned.")
sc = state.get("scraped_content", "")
blocked = "blocked" in sc.lower() or "403" in sc
report   = state.get("report",   "No report generated.")
feedback = state.get("feedback", "No feedback provided.")

# ── Step 1: Search ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="result-card">
    <div class="result-card-header">
        <div class="result-card-left">
            <div class="result-card-icon icon-search">🔍</div>
            <div>
                <div class="result-card-title">Web Search Results</div>
                <div class="result-card-meta">Tavily API · Step 1 of 4</div>
            </div>
        </div>
        <span class="badge-ok">DONE</span>
    </div>
    <div class="result-card-body">
""", unsafe_allow_html=True)

with st.expander("Show raw search output"):
    st.markdown(f'<div class="mono-block">{sr}</div>', unsafe_allow_html=True)

st.markdown("</div></div>", unsafe_allow_html=True)

# ── Step 2: Scrape ─────────────────────────────────────────────────────────────
scrape_badge = '<span class="badge-warn">BLOCKED</span>' if blocked else '<span class="badge-ok">DONE</span>'
st.markdown(f"""
<div class="result-card">
    <div class="result-card-header">
        <div class="result-card-left">
            <div class="result-card-icon icon-scrape">📄</div>
            <div>
                <div class="result-card-title">Scraped Page Content</div>
                <div class="result-card-meta">BeautifulSoup · Step 2 of 4</div>
            </div>
        </div>
        {scrape_badge}
    </div>
    <div class="result-card-body">
""", unsafe_allow_html=True)

with st.expander("Show scraped text"):
    st.markdown(
        f'<div class="mono-block">{sc if sc else "No content was extracted."}</div>',
        unsafe_allow_html=True,
    )

st.markdown("</div></div>", unsafe_allow_html=True)

# ── Step 3: Report ─────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="report-card">
    <div class="report-card-header">
        <div class="report-card-title">
            <span style="background:#0a2e1f;border-radius:7px;padding:4px 8px;font-size:0.85rem;">📝</span>
            Final Research Report
        </div>
        <span class="badge-ok">GENERATED</span>
    </div>
    <div class="report-card-body">
""", unsafe_allow_html=True)

# Render as markdown so any markdown formatting in the LLM output looks great
st.markdown(report)

st.markdown("</div></div>", unsafe_allow_html=True)

# Download button sits just below the report card
dl_col, _ = st.columns([1, 3])
with dl_col:
    st.download_button(
        label="⬇  Download report (.txt)",
        data=report,
        file_name=f"report_{clean_topic[:40].replace(' ', '_')}.txt",
        mime="text/plain",
    )

st.markdown("<br>", unsafe_allow_html=True)

# ── Step 4: Critic ─────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="critic-card">
    <div class="critic-header">
        <span style="font-size:1.2rem;">🧐</span>
        <span class="critic-header-text">Critic Agent Evaluation</span>
        <span style="margin-left:auto;" class="badge-warn">REVIEWED</span>
    </div>
    <div class="critic-body">
""", unsafe_allow_html=True)

st.markdown(
    f'<div style="font-size:0.875rem;color:#a8946a;line-height:1.85;white-space:pre-wrap;">'
    f'{feedback}</div>',
    unsafe_allow_html=True,
)

st.markdown("</div></div>", unsafe_allow_html=True)