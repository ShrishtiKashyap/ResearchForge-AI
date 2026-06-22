"""
ResearchForge-AI — Streamlit UI for the multi-agent research pipeline.
Drop this file alongside pipeline.py and run: streamlit run app.py
"""

import streamlit as st
import time

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchForge-AI",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* ---------- base ---------- */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Force dark canvas */
    .stApp {
        background: #0d0f14;
        color: #e2e8f0;
    }

    /* ---------- header ---------- */
    .rf-header {
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 2.4rem 0 0.6rem 0;
    }
    .rf-logo {
        font-size: 2.6rem;
        line-height: 1;
    }
    .rf-title {
        font-size: 2rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #818cf8 0%, #38bdf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
    }
    .rf-subtitle {
        font-size: 0.82rem;
        color: #64748b;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin: 0;
    }
    .rf-divider {
        height: 1px;
        background: linear-gradient(90deg, #818cf820 0%, #38bdf840 50%, transparent 100%);
        margin: 1.2rem 0 2rem 0;
        border: none;
    }

    /* ---------- input area ---------- */
    .stTextInput > div > div > input {
        background: #161b27 !important;
        border: 1px solid #2d3748 !important;
        border-radius: 10px !important;
        color: #e2e8f0 !important;
        font-size: 1rem !important;
        padding: 0.75rem 1rem !important;
        transition: border-color 0.2s;
    }
    .stTextInput > div > div > input:focus {
        border-color: #818cf8 !important;
        box-shadow: 0 0 0 3px #818cf820 !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: #475569 !important;
    }

    /* ---------- button ---------- */
    div.stButton > button {
        background: linear-gradient(135deg, #6366f1, #38bdf8) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        padding: 0.65rem 2rem !important;
        letter-spacing: 0.02em !important;
        transition: opacity 0.2s, transform 0.15s !important;
        width: 100% !important;
    }
    div.stButton > button:hover {
        opacity: 0.88 !important;
        transform: translateY(-1px) !important;
    }
    div.stButton > button:active {
        transform: translateY(0) !important;
    }

    /* ---------- step cards ---------- */
    .step-card {
        background: #161b27;
        border: 1px solid #1e2534;
        border-radius: 12px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1.2rem;
        position: relative;
        overflow: hidden;
    }
    .step-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0;
        width: 3px; height: 100%;
        border-radius: 3px 0 0 3px;
    }
    .step-card.search::before  { background: #818cf8; }
    .step-card.scrape::before  { background: #38bdf8; }
    .step-card.report::before  { background: #34d399; }
    .step-card.critic::before  { background: #f59e0b; }

    .step-label {
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        margin-bottom: 0.35rem;
    }
    .step-card.search .step-label  { color: #818cf8; }
    .step-card.scrape .step-label  { color: #38bdf8; }
    .step-card.report .step-label  { color: #34d399; }
    .step-card.critic .step-label  { color: #f59e0b; }

    .step-title {
        font-size: 1.05rem;
        font-weight: 600;
        color: #e2e8f0;
        margin: 0 0 0.2rem 0;
    }
    .step-desc {
        font-size: 0.82rem;
        color: #64748b;
        margin: 0;
    }

    /* ---------- content blocks ---------- */
    .content-block {
        background: #0d1117;
        border: 1px solid #1e2534;
        border-radius: 8px;
        padding: 1.1rem 1.2rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        color: #94a3b8;
        line-height: 1.7;
        white-space: pre-wrap;
        word-break: break-word;
        max-height: 320px;
        overflow-y: auto;
    }
    .content-block::-webkit-scrollbar { width: 6px; }
    .content-block::-webkit-scrollbar-track { background: transparent; }
    .content-block::-webkit-scrollbar-thumb { background: #2d3748; border-radius: 3px; }

    /* report uses prose styling */
    .report-block {
        background: #0d1117;
        border: 1px solid #1e2534;
        border-radius: 8px;
        padding: 1.4rem 1.6rem;
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        color: #cbd5e1;
        line-height: 1.8;
        white-space: pre-wrap;
        word-break: break-word;
        max-height: 420px;
        overflow-y: auto;
    }

    /* ---------- status badge ---------- */
    .badge {
        display: inline-block;
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        margin-left: 0.5rem;
        vertical-align: middle;
    }
    .badge-ok   { background: #14532d; color: #4ade80; }
    .badge-warn { background: #451a03; color: #fbbf24; }

    /* ---------- expander override ---------- */
    details summary {
        list-style: none;
    }
    .streamlit-expanderHeader {
        background: #161b27 !important;
        border: 1px solid #1e2534 !important;
        border-radius: 8px !important;
        color: #94a3b8 !important;
        font-size: 0.85rem !important;
    }
    .streamlit-expanderContent {
        background: #0d1117 !important;
        border: 1px solid #1e2534 !important;
        border-top: none !important;
        border-radius: 0 0 8px 8px !important;
    }

    /* ---------- sidebar ---------- */
    section[data-testid="stSidebar"] {
        background: #0a0d12 !important;
        border-right: 1px solid #1e2534 !important;
    }

    /* ---------- metrics row ---------- */
    .metrics-row {
        display: flex;
        gap: 1rem;
        margin-bottom: 1.6rem;
        flex-wrap: wrap;
    }
    .metric-chip {
        background: #161b27;
        border: 1px solid #1e2534;
        border-radius: 8px;
        padding: 0.55rem 1rem;
        font-size: 0.8rem;
        color: #64748b;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }
    .metric-chip span { color: #e2e8f0; font-weight: 600; }

    /* ---------- empty state ---------- */
    .empty-state {
        text-align: center;
        padding: 4rem 2rem;
        color: #334155;
    }
    .empty-state-icon { font-size: 3rem; margin-bottom: 1rem; }
    .empty-state-text { font-size: 0.95rem; }

    /* hide streamlit default elements */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 0 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="rf-header">
        <div class="rf-logo">🔬</div>
        <div>
            <p class="rf-title">ResearchForge-AI</p>
            <p class="rf-subtitle">Multi-Agent Research Assistant</p>
        </div>
    </div>
    <hr class="rf-divider">
    """,
    unsafe_allow_html=True,
)

# ── Layout: two columns (input + results) ──────────────────────────────────────
left, right = st.columns([1, 2], gap="large")

with left:
    st.markdown("##### Research Topic")
    topic = st.text_input(
        label="topic",
        placeholder="e.g. Quantum computing advances in 2025",
        label_visibility="collapsed",
    )

    run = st.button("⚡  Generate Research", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Pipeline step overview cards
    steps = [
        ("search",  "01", "Web Search",      "Tavily API scans the web for relevant sources"),
        ("scrape",  "02", "Content Scraping", "BeautifulSoup extracts and cleans page text"),
        ("report",  "03", "Report Writing",   "LLM drafts a structured research report"),
        ("critic",  "04", "Critic Review",    "Second LLM evaluates and suggests improvements"),
    ]
    for cls, num, title, desc in steps:
        st.markdown(
            f"""
            <div class="step-card {cls}">
                <p class="step-label">Step {num}</p>
                <p class="step-title">{title}</p>
                <p class="step-desc">{desc}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ── Right panel ────────────────────────────────────────────────────────────────
with right:

    # ── Empty state ─────────────────────────────────────────────────────────────
    if not run or not topic.strip():
        st.markdown(
            """
            <div class="empty-state">
                <div class="empty-state-icon">🛰️</div>
                <p class="empty-state-text">
                    Enter a research topic on the left<br>and hit <strong>Generate Research</strong> to begin.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── Run pipeline ────────────────────────────────────────────────────────────
    else:
        # Lazy import so app doesn't crash if pipeline.py isn't present yet
        try:
            from pipeline import run_research_pipeline
        except ImportError:
            st.error(
                "**pipeline.py not found.** Place `pipeline.py` (and `agents.py`) "
                "in the same directory as this `app.py` and restart Streamlit."
            )
            st.stop()

        start_ts = time.time()

        # Progress placeholders
        status_bar  = st.empty()
        progress_ph = st.empty()

        status_bar.markdown(
            "<p style='color:#818cf8;font-size:0.85rem;'>🔄 Starting pipeline…</p>",
            unsafe_allow_html=True,
        )
        prog = progress_ph.progress(0)

        try:
            # ── Step 1: Search ────────────────────────────────────────────────
            status_bar.markdown(
                "<p style='color:#818cf8;font-size:0.85rem;'>🔍 Step 1 — Searching the web…</p>",
                unsafe_allow_html=True,
            )
            prog.progress(10)

            state = {}

            # We run the full pipeline in one call; progress bar is illustrative
            # (pipeline is synchronous and doesn't yield intermediate state).
            with st.spinner("Running multi-agent pipeline — this may take 30–90 seconds…"):
                state = run_research_pipeline(topic.strip())

            elapsed = round(time.time() - start_ts, 1)

            prog.progress(100)
            status_bar.markdown(
                f"<p style='color:#34d399;font-size:0.85rem;'>✅ Pipeline complete in {elapsed}s</p>",
                unsafe_allow_html=True,
            )

        except Exception as exc:
            prog.progress(0)
            status_bar.markdown(
                "<p style='color:#f87171;font-size:0.85rem;'>❌ Pipeline failed — see error below</p>",
                unsafe_allow_html=True,
            )
            st.error(f"**Error:** {exc}")
            st.stop()

        # ── Metrics chips ─────────────────────────────────────────────────────
        sr_len = len(state.get("search_results", ""))
        sc_len = len(state.get("scraped_content", ""))
        rp_len = len(state.get("report", ""))
        fb_len = len(state.get("feedback", ""))

        st.markdown(
            f"""
            <div class="metrics-row">
                <div class="metric-chip">🔍 Search results <span>{sr_len} chars</span></div>
                <div class="metric-chip">📄 Scraped content <span>{sc_len} chars</span></div>
                <div class="metric-chip">📝 Report <span>{rp_len} chars</span></div>
                <div class="metric-chip">🧐 Feedback <span>{fb_len} chars</span></div>
                <div class="metric-chip">⏱ Time <span>{elapsed}s</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ── Step 1: Search Results ────────────────────────────────────────────
        st.markdown(
            """
            <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.5rem;">
                <span style="font-size:1rem;">🔍</span>
                <span style="font-weight:600;color:#818cf8;">Step 1 — Search Results</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        with st.expander("View raw search output", expanded=False):
            sr = state.get("search_results", "No search results returned.")
            st.markdown(
                f'<div class="content-block">{sr}</div>',
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Step 2: Scraped Content ───────────────────────────────────────────
        st.markdown(
            """
            <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.5rem;">
                <span style="font-size:1rem;">📄</span>
                <span style="font-weight:600;color:#38bdf8;">Step 2 — Scraped Content</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        sc = state.get("scraped_content", "")
        blocked = "blocked" in sc.lower() or "403" in sc
        badge_html = (
            '<span class="badge badge-warn">Blocked</span>'
            if blocked
            else '<span class="badge badge-ok">OK</span>'
        )
        with st.expander(f"View scraped page text {badge_html}", expanded=False):
            st.markdown(
                f'<div class="content-block">{sc or "No content scraped."}</div>',
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Step 3: Final Report ──────────────────────────────────────────────
        st.markdown(
            """
            <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.6rem;">
                <span style="font-size:1rem;">📝</span>
                <span style="font-weight:600;color:#34d399;">Step 3 — Final Report</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        report = state.get("report", "No report generated.")
        st.markdown(
            f'<div class="report-block">{report}</div>',
            unsafe_allow_html=True,
        )

        # Download button
        st.download_button(
            label="⬇  Download Report (.txt)",
            data=report,
            file_name=f"report_{topic[:40].replace(' ', '_')}.txt",
            mime="text/plain",
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Step 4: Critic Feedback ───────────────────────────────────────────
        st.markdown(
            """
            <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.5rem;">
                <span style="font-size:1rem;">🧐</span>
                <span style="font-weight:600;color:#f59e0b;">Step 4 — Critic Feedback</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        feedback = state.get("feedback", "No feedback provided.")
        with st.expander("View critic agent evaluation", expanded=True):
            st.markdown(
                f'<div class="report-block">{feedback}</div>',
                unsafe_allow_html=True,
            )