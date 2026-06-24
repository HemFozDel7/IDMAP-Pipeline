"""HITL Gate 2 — Silver Review"""
import streamlit as st
from utils.state import advance_phase

def render():
    st.markdown("""
    <div class='hero'>
      <div class='hero-eye'>HITL Gate 2 of 3</div>
      <h1>⏸ Silver Review</h1>
      <p>Review and approve the Silver STTM cleansing rules before transformation executes.</p>
    </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class='hitl'>
      <h3>⚠️ Human Approval Required</h3>
      <p>The STTM Generator has proposed Silver cleansing rules — null strategies, deduplication keys,
         type casts, date normalisation formats, and surrogate key prefixes.
         Review and approve before the Silver Agent executes.</p>
    </div>""", unsafe_allow_html=True)

    sttm = st.session_state.get("sttm_silver")
    if sttm is None:
        st.error("No Silver STTM found. Please run Phase 2 first.")
        return

    st.markdown("<div class='card-t'>📋 Approve / Edit Silver STTM Rules</div>", unsafe_allow_html=True)
    edited = st.data_editor(
        sttm, use_container_width=True, hide_index=True,
        column_config={
            "approved":      st.column_config.CheckboxColumn("Approved", default=True),
            "null_strategy": st.column_config.SelectboxColumn("Null Strategy",
                options=["none_required","fill_median","fill_mode","fill_forward","flag_unknown","drop_row"]),
            "type_cast":     st.column_config.SelectboxColumn("Type Cast",
                options=["VARCHAR","INT64","DECIMAL(15,2)","DATE","BOOLEAN","FLOAT64"]),
            "dedup_key":     st.column_config.SelectboxColumn("Dedup Key", options=["Yes","No"]),
        },
    )

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='card-t'>✅ Approval Checklist</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        chk1 = st.checkbox("Null strategies are appropriate per column", value=True)
        chk2 = st.checkbox("Deduplication keys are correct", value=True)
    with c2:
        chk3 = st.checkbox("Date format standardised to YYYY-MM-DD", value=True)
        chk4 = st.checkbox("Surrogate key prefixes are acceptable", value=True)

    all_checked = all([chk1, chk2, chk3, chk4])
    st.markdown("<hr>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Phase 2"):
            st.session_state.current_phase = "phase2"
            st.rerun()
    with col2:
        if all_checked:
            if st.button("✅ Approve & Proceed to Phase 3 →", use_container_width=True):
                st.session_state.sttm_silver = edited
                st.session_state.silver_approved = True
                advance_phase("hitl_silver", "phase3")
                st.rerun()
        else:
            st.warning("Complete all checklist items to approve.")
