"""HITL Gate 3 — Gold Review"""
import streamlit as st
from utils.state import advance_phase

def render():
    st.markdown("""
    <div class='hero'>
      <div class='hero-eye'>HITL Gate 3 of 3</div>
      <h1>⏸ Gold Review</h1>
      <p>Final approval gate — review join logic, aggregation strategies, and KPI formulas
         before Gold materialisation and reporting.</p>
    </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class='hitl'>
      <h3>⚠️ Human Approval Required</h3>
      <p>Review the Gold STTM output table definitions, join keys, aggregation logic,
         and KPI formulas. Once approved, the Gold Agent will materialise all tables
         and the Reporter will generate the executive report — no further gates.</p>
    </div>""", unsafe_allow_html=True)

    sttm = st.session_state.get("sttm_gold")
    if sttm is None:
        st.error("No Gold STTM found. Please run Phase 3 first.")
        return

    st.markdown("<div class='card-t'>📋 Approve / Edit Gold STTM Rules</div>", unsafe_allow_html=True)
    edited = st.data_editor(
        sttm, use_container_width=True, hide_index=True,
        column_config={
            "approved":     st.column_config.CheckboxColumn("Approved", default=True),
            "join_type":    st.column_config.SelectboxColumn("Join Type",
                options=["N/A","INNER","LEFT","RIGHT","FULL OUTER","CROSS"]),
            "aggregation":  st.column_config.TextColumn("Aggregation", width="large"),
            "kpi_formula":  st.column_config.TextColumn("KPI Formula", width="large"),
        },
    )

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='card-t'>✅ Approval Checklist</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        chk1 = st.checkbox("Join keys and cardinality are correct", value=True)
        chk2 = st.checkbox("Aggregation logic is appropriate", value=True)
    with c2:
        chk3 = st.checkbox("KPI formulas are validated", value=True)
        chk4 = st.checkbox("Output table names are acceptable", value=True)

    all_checked = all([chk1, chk2, chk3, chk4])
    st.markdown("<hr>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Phase 3"):
            st.session_state.current_phase = "phase3"
            st.rerun()
    with col2:
        if all_checked:
            if st.button("✅ Approve & Run Phase 4 — Final →", use_container_width=True):
                st.session_state.sttm_gold = edited
                st.session_state.gold_approved = True
                advance_phase("hitl_gold", "phase4")
                st.rerun()
        else:
            st.warning("Complete all checklist items to approve.")
