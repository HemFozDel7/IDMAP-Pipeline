"""
IDAMP — Intent-Driven Agentic Medallion Pipeline
Accelerate with AI Training | Demo Application
Run: streamlit run app.py
"""
import streamlit as st
from utils.state import init_session_state
from utils.styles import load_css

st.set_page_config(
    page_title="IDAMP Pipeline",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_css()
init_session_state()

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class='sb-header'>
      <span class='sb-icon'>🏭</span>
      <div>
        <div class='sb-title'>IDAMP Pipeline</div>
        <div class='sb-sub'>Real Estate Analytics</div>
      </div>
    </div>
    <div class='sb-div'></div>
    """, unsafe_allow_html=True)

    phases = [
        ("Phase 1 — Profile & Bronze STTM",       "phase1",      False),
        ("HITL: Bronze Review",                    "hitl_bronze", True),
        ("Phase 2 — Bronze Execute & Silver STTM", "phase2",      False),
        ("HITL: Silver Review",                    "hitl_silver", True),
        ("Phase 3 — Silver Execute & Gold STTM",   "phase3",      False),
        ("HITL: Gold Review",                      "hitl_gold",   True),
        ("Phase 4 — Gold Execute & Report",        "phase4",      False),
        ("✅ Pipeline Complete",                   "complete",    False),
    ]

    current   = st.session_state.get("current_phase", "phase1")
    completed = st.session_state.get("completed_phases", set())

    for label, key, is_hitl in phases:
        is_current = key == current
        is_done    = key in completed

        if is_done:
            icon = "✓";  css = "ph-done"
        elif is_current:
            icon = "⏸" if is_hitl else "▶";  css = "ph-active"
        else:
            icon = "○ ⏸" if is_hitl else "○";  css = "ph-pend"

        st.markdown(
            f"<div class='ph-item {css}'>"
            f"<span class='ph-ico'>{icon}</span>"
            f"<span class='ph-lbl'>{label}</span>"
            f"</div>",
            unsafe_allow_html=True,
        )

    st.markdown("<div class='sb-div'></div>", unsafe_allow_html=True)
    if st.button("🔄 Reset", use_container_width=True):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

# ── Router ─────────────────────────────────────────────────────────────────────
from pages import home, phase1, hitl_bronze, phase2, hitl_silver, phase3, hitl_gold, phase4, complete

router = {
    "phase1":      phase1.render,
    "hitl_bronze": hitl_bronze.render,
    "phase2":      phase2.render,
    "hitl_silver": hitl_silver.render,
    "phase3":      phase3.render,
    "hitl_gold":   hitl_gold.render,
    "phase4":      phase4.render,
    "complete":    complete.render,
}

if not st.session_state.get("pipeline_started", False):
    home.render()
else:
    router.get(st.session_state.get("current_phase", "phase1"), home.render)()
