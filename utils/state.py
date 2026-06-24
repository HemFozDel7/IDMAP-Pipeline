import streamlit as st

def init_session_state():
    defaults = {
        "pipeline_started": False,
        "current_phase": "phase1",
        "completed_phases": set(),
        "uploaded_files": [],
        "file_names": [],
        "business_intent": "",
        "profile_json": None,
        "sttm_bronze": None,
        "sttm_silver": None,
        "sttm_gold": None,
        "bronze_parquets": [],
        "silver_parquets": [],
        "gold_tables": [],
        "report_html": "",
        "agent_logs": {},
        "bronze_edits": {},
        "silver_edits": {},
        "gold_edits": {},
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

def advance_phase(from_phase, to_phase):
    if "completed_phases" not in st.session_state:
        st.session_state.completed_phases = set()
    st.session_state.completed_phases.add(from_phase)
    st.session_state.current_phase = to_phase

def add_log(phase, message):
    if "agent_logs" not in st.session_state:
        st.session_state.agent_logs = {}
    if phase not in st.session_state.agent_logs:
        st.session_state.agent_logs[phase] = []
    st.session_state.agent_logs[phase].append(message)
