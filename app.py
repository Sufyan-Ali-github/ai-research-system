import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind · AI Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def extract_text(content) -> str:
    """
    Some LangChain/Gemini responses return message content as a list of
    content blocks like [{'type': 'text', 'text': '...'}] instead of a
    plain string. Normalize either case to plain text.
    """
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            parts.append(block.get("text", "") if isinstance(block, dict) else str(block))
        return "\n".join(parts)
    return str(content)


# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,700;1,300&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

.stApp {
    background: #0a0a0f;
    background-image:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(255,140,50,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(255,80,30,0.08) 0%, transparent 55%);
    color: #f0ebe0;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem; max-width: 1200px; }

/* ── Hero ── */
.hero { text-align: center; padding: 3rem 0 2rem; }
.hero-eyebrow {
    font-family: 'DM Mono', monospace; font-size: 0.7rem; font-weight: 500;
    letter-spacing: 0.25em; text-transform: uppercase; color: #ff8c32; margin-bottom: 1rem;
}
.hero h1 {
    font-family: 'Syne', sans-serif; font-size: clamp(2.8rem, 6vw, 5rem); font-weight: 800;
    line-height: 1.0; letter-spacing: -0.03em; color: #f5f1e8; margin: 0 0 1rem;
}
.hero h1 span { color: #ff8c32; }
.hero-sub { font-size: 1.05rem; font-weight: 300; color: #b8b0a4; max-width: 520px; margin: 0 auto; line-height: 1.65; }

.divider { height: 1px; background: linear-gradient(90deg, transparent, rgba(255,140,50,0.35), transparent); margin: 2rem 0; }

/* ── Generic bordered container (st.container(border=True)) ── */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    border-radius: 16px !important;
}

/* Accent variants via anchor + sibling trick */
.anchor-input + div[data-testid="stVerticalBlockBorderWrapper"] { border-color: rgba(255,140,50,0.25) !important; }
.anchor-report + div[data-testid="stVerticalBlockBorderWrapper"] { border-color: rgba(255,140,50,0.35) !important; }
.anchor-feedback + div[data-testid="stVerticalBlockBorderWrapper"] { border-color: rgba(80,200,120,0.35) !important; }
.anchor-raw + div[data-testid="stVerticalBlockBorderWrapper"] { border-color: rgba(255,255,255,0.08) !important; }

/* ── Inputs ── */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,140,50,0.25) !important;
    border-radius: 10px !important;
    color: #f5f1e8 !important;
    font-size: 1rem !important;
    padding: 0.75rem 1rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #ff8c32 !important;
    box-shadow: 0 0 0 3px rgba(255,140,50,0.12) !important;
}
.stTextInput > label {
    font-family: 'DM Mono', monospace !important; font-size: 0.72rem !important;
    letter-spacing: 0.15em !important; text-transform: uppercase !important; color: #ff8c32 !important;
    font-weight: 500 !important;
}

/* ── Primary button (Run Pipeline) ── */
div[data-testid="stButton"] button[kind="primary"] {
    background: linear-gradient(135deg, #ff8c32 0%, #ff5a1a 100%) !important;
    color: #0a0a0f !important; font-family: 'Syne', sans-serif !important; font-weight: 700 !important;
    font-size: 0.95rem !important; letter-spacing: 0.04em !important; border: none !important;
    border-radius: 10px !important; padding: 0.7rem 2.2rem !important;
    box-shadow: 0 4px 20px rgba(255,140,50,0.3) !important; width: 100%;
    transition: transform 0.15s, box-shadow 0.15s !important;
}
div[data-testid="stButton"] button[kind="primary"]:hover {
    transform: translateY(-2px) !important; box-shadow: 0 8px 28px rgba(255,140,50,0.4) !important;
}

/* ── Secondary buttons (example chips) ── */
div[data-testid="stButton"] button[kind="secondary"] {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 8px !important;
    color: #cdc8bf !important;
    font-size: 0.78rem !important;
    padding: 0.35rem 0.9rem !important;
}
div[data-testid="stButton"] button[kind="secondary"]:hover {
    border-color: #ff8c32 !important; color: #ff8c32 !important;
}

/* ── Step cards ── */
.step-card {
    background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px; padding: 1.3rem 1.6rem; margin-bottom: 1rem; position: relative;
    border-left: 3px solid rgba(255,255,255,0.08); transition: border-color 0.3s, background 0.3s;
}
.step-card.active { border-color: rgba(255,140,50,0.35); border-left-color: #ff8c32; background: rgba(255,140,50,0.05); }
.step-card.done   { border-color: rgba(80,200,120,0.3);  border-left-color: #50c878; background: rgba(80,200,120,0.04); }
.step-header { display: flex; align-items: center; gap: 0.8rem; }
.step-num   { font-family: 'DM Mono', monospace; font-size: 0.68rem; letter-spacing: 0.15em; color: #ff8c32; opacity: 0.8; }
.step-title { font-family: 'Syne', sans-serif; font-size: 0.95rem; font-weight: 700; color: #f5f1e8; }
.step-status { margin-left: auto; font-family: 'DM Mono', monospace; font-size: 0.68rem; letter-spacing: 0.1em; }
.status-waiting { color: #605850; }
.status-running { color: #ff8c32; }
.status-done    { color: #50c878; }
.step-desc { font-size: 0.82rem; color: #8f887e; margin-top: 0.3rem; }

/* ── Panel labels ── */
.panel-label {
    font-family: 'DM Mono', monospace; font-size: 0.7rem; letter-spacing: 0.2em; text-transform: uppercase;
    margin-bottom: 1.1rem; padding-bottom: 0.7rem; border-bottom: 1px solid rgba(255,255,255,0.1);
}
.panel-label.orange { color: #ff8c32; border-bottom-color: rgba(255,140,50,0.2); }
.panel-label.green  { color: #50c878; border-bottom-color: rgba(80,200,120,0.2); }
.panel-label.gray   { color: #a09890; border-bottom-color: rgba(255,255,255,0.1); }

/* ── Bright, readable markdown content inside cards ── */
div[data-testid="stVerticalBlockBorderWrapper"] p,
div[data-testid="stVerticalBlockBorderWrapper"] li,
div[data-testid="stVerticalBlockBorderWrapper"] span {
    color: #d8d2c6 !important; font-size: 0.95rem; line-height: 1.75;
}
div[data-testid="stVerticalBlockBorderWrapper"] h1,
div[data-testid="stVerticalBlockBorderWrapper"] h2,
div[data-testid="stVerticalBlockBorderWrapper"] h3 {
    font-family: 'Syne', sans-serif !important; color: #f5f1e8 !important;
}
div[data-testid="stVerticalBlockBorderWrapper"] strong { color: #ffb877 !important; }
div[data-testid="stVerticalBlockBorderWrapper"] a { color: #ff8c32 !important; }

/* ── Section heading ── */
.section-heading { font-family: 'Syne', sans-serif; font-size: 1.3rem; font-weight: 700; color: #f5f1e8; margin: 2rem 0 1rem; }

.notice { font-family: 'DM Mono', monospace; font-size: 0.72rem; color: #605850; text-align: center; margin-top: 3rem; letter-spacing: 0.08em; }
</style>
""", unsafe_allow_html=True)


# ── Helper: render a step card ────────────────────────────────────────────────
def step_card(num: str, title: str, state: str, desc: str = ""):
    label_map = {"waiting": ("WAITING", "status-waiting"), "running": ("● RUNNING", "status-running"), "done": ("✓ DONE", "status-done")}
    label, cls = label_map.get(state, ("", ""))
    card_cls = {"running": "active", "done": "done"}.get(state, "")
    st.markdown(f"""
    <div class="step-card {card_cls}">
        <div class="step-header">
            <span class="step-num">{num}</span>
            <span class="step-title">{title}</span>
            <span class="step-status {cls}">{label}</span>
        </div>
        <div class="step-desc">{desc}</div>
    </div>
    """, unsafe_allow_html=True)


# ── Session state init ────────────────────────────────────────────────────────
if "results" not in st.session_state:
    st.session_state.results = {}
if "running" not in st.session_state:
    st.session_state.running = False
if "topic_input" not in st.session_state:
    st.session_state.topic_input = ""

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Multi-Agent AI System</div>
    <h1>Research<span>Forge</span></h1>
    <p class="hero-sub">Four specialized AI agents collaborate — searching, scraping, writing,
    and critiquing — to deliver a polished research report on any topic.</p>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)


# ── Layout: input left, pipeline right ───────────────────────────────────────
col_input, col_spacer, col_pipeline = st.columns([5, 0.5, 4])

with col_input:
    st.markdown('<div class="anchor-input"></div>', unsafe_allow_html=True)
    with st.container(border=True):
        topic = st.text_input(
            "Research Topic",
            placeholder="e.g. Quantum computing breakthroughs in 2025",
            key="topic_input",
        )
        run_btn = st.button("⚡  Run Research Pipeline", use_container_width=True, type="primary")

    st.markdown('<div style="margin-top:1rem;font-family:\'DM Mono\',monospace;font-size:0.68rem;color:#605850;letter-spacing:0.1em;">TRY →</div>', unsafe_allow_html=True)
    chip_cols = st.columns(3)
    examples = ["LLM agents 2025", "CRISPR gene editing", "Fusion energy progress"]
    for c, ex in zip(chip_cols, examples):
        with c:
            if st.button(ex, key=f"chip_{ex}", use_container_width=True):
                st.session_state.topic_input = ex
                st.rerun()

with col_pipeline:
    st.markdown('<div class="section-heading">Pipeline</div>', unsafe_allow_html=True)
    r = st.session_state.results
    steps = ["search", "reader", "writer", "critic"]

    def step_state(step):
        if step in r:
            return "done"
        if st.session_state.running:
            for k in steps:
                if k not in r:
                    return "running" if k == step else "waiting"
        return "waiting"

    step_card("01", "Search Agent", step_state("search"), "Gathers recent web information")
    step_card("02", "Reader Agent", step_state("reader"), "Scrapes & extracts deep content")
    step_card("03", "Writer Chain", step_state("writer"), "Drafts the full research report")
    step_card("04", "Critic Chain", step_state("critic"), "Reviews & scores the report")


# ── Trigger run ───────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.rerun()

# ── Run pipeline ──────────────────────────────────────────────────────────────
if st.session_state.running:
    topic_val = st.session_state.topic_input
    results = {}
    try:
        with st.spinner("🔍  Search Agent is working…"):
            search_agent = build_search_agent()
            sr = search_agent.invoke({"messages": [("user", f"Find recent, reliable and detailed information about: {topic_val}")]})
            results["search"] = extract_text(sr["messages"][-1].content)
            st.session_state.results = dict(results)

        with st.spinner("📄  Reader Agent is scraping top resources…"):
            reader_agent = build_reader_agent()
            rr = reader_agent.invoke({
                "messages": [("user",
                    f"Based on the following search results about '{topic_val}', "
                    f"pick the most relevant URL and scrape it for deeper content.\n\n"
                    f"Search Results:\n{results['search'][:800]}"
                )]
            })
            results["reader"] = extract_text(rr["messages"][-1].content)
            st.session_state.results = dict(results)

        with st.spinner("✍️  Writer is drafting the report…"):
            research_combined = f"SEARCH RESULTS:\n{results['search']}\n\nDETAILED SCRAPED CONTENT:\n{results['reader']}"
            results["writer"] = writer_chain.invoke({"topic": topic_val, "research": research_combined})
            st.session_state.results = dict(results)

        with st.spinner("🧐  Critic is reviewing the report…"):
            results["critic"] = critic_chain.invoke({"report": results["writer"]})
            st.session_state.results = dict(results)

        st.session_state.running = False
        st.rerun()
    except Exception as e:
        st.session_state.running = False
        st.error(f"Pipeline failed: {e}")


# ── Results display ───────────────────────────────────────────────────────────
r = st.session_state.results

if r and not st.session_state.running:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Results</div>', unsafe_allow_html=True)

    if "search" in r:
        st.markdown('<div class="anchor-raw"></div>', unsafe_allow_html=True)
        with st.container(border=True):
            with st.expander("🔍 Search Results (raw)", expanded=False):
                st.markdown('<div class="panel-label gray">Search Agent Output</div>', unsafe_allow_html=True)
                st.markdown(r["search"])

    if "reader" in r:
        st.markdown('<div class="anchor-raw"></div>', unsafe_allow_html=True)
        with st.container(border=True):
            with st.expander("📄 Scraped Content (raw)", expanded=False):
                st.markdown('<div class="panel-label gray">Reader Agent Output</div>', unsafe_allow_html=True)
                st.markdown(r["reader"])

    if "writer" in r:
        st.markdown('<div class="anchor-report"></div>', unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown('<div class="panel-label orange">📝 Final Research Report</div>', unsafe_allow_html=True)
            st.markdown(r["writer"])
            st.download_button(
                "⬇  Download Report (.md)",
                data=r["writer"],
                file_name=f"research_report_{int(time.time())}.md",
                mime="text/markdown",
            )

    if "critic" in r:
        st.markdown('<div class="anchor-feedback"></div>', unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown('<div class="panel-label green">🧐 Critic Feedback</div>', unsafe_allow_html=True)
            st.markdown(r["critic"])

st.markdown('<div class="notice">ResearchMind · Powered by LangChain multi-agent pipeline · Built with Streamlit</div>', unsafe_allow_html=True)