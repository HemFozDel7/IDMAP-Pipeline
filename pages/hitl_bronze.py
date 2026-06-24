"""HITL Gate 1 — Bronze Review"""
import streamlit as st
import pandas as pd
from utils.state import advance_phase

def render():
    st.markdown("""
    <div class='hero'>
      <div class='hero-eye'>HITL Gate 1 of 3</div>
      <h1>⏸ Bronze Review</h1>
      <p>Review and approve the Bronze STTM rules before ingestion begins.
         You can edit rules directly in the table below.</p>
    </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class='hitl'>
      <h3>⚠️ Human Approval Required</h3>
      <p>The Profiler and STTM Generator agents have proposed Bronze mapping rules.
         Review column renames, type assertions, and metadata injections.
         Approve to allow the Bronze Agent to execute ingestion.</p>
    </div>""", unsafe_allow_html=True)

    sttm = st.session_state.get("sttm_bronze")
    if sttm is None:
        st.error("No Bronze STTM found. Please run Phase 1 first.")
        return

    # Editable table
    st.markdown("<div class='card-t'>📋 Approve / Edit Bronze STTM Rules</div>", unsafe_allow_html=True)
    edited = st.data_editor(
        sttm, use_container_width=True, hide_index=True,
        column_config={
            "approved": st.column_config.CheckboxColumn("Approved", default=True),
            "transformation": st.column_config.TextColumn("Transformation", width="medium"),
            "target_col": st.column_config.TextColumn("Target Column", width="medium"),
            "notes": st.column_config.TextColumn("Notes", width="large"),
        },
    )

    # Checklist
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='card-t'>✅ Approval Checklist</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        chk1 = st.checkbox("Column renames are accurate", value=True)
        chk2 = st.checkbox("Metadata fields (_source_file, _run_id, _ingest_ts) are correct", value=True)
    with c2:
        chk3 = st.checkbox("Data type assertions are appropriate", value=True)
        chk4 = st.checkbox("No sensitive PII columns included in Bronze", value=True)

    all_checked = all([chk1, chk2, chk3, chk4])
    all_approved = edited["approved"].all() if "approved" in edited.columns else True

    st.markdown("<hr>", unsafe_allow_html=True)
    col1, col2 = st.columns([1,1])

    with col1:
        if st.button("← Back to Phase 1"):
            advance_phase("hitl_bronze", "phase1")
            st.session_state.completed_phases.discard("hitl_bronze")
            st.session_state.current_phase = "phase1"
            st.rerun()

    with col2:
        if all_checked:
            if st.button("✅ Approve & Proceed to Phase 2 →", use_container_width=True):
                st.session_state.sttm_bronze = edited
                st.session_state.bronze_approved = True
                advance_phase("hitl_bronze", "phase2")
                st.rerun()
        else:
            st.warning("Complete all checklist items to approve.")
