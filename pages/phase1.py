"""Phase 1 — Profile & Bronze STTM"""
import streamlit as st
import time
from utils.state import advance_phase, add_log
from agents import profiler, sttm_generator

def render():
    st.markdown("""
    <div class='hero'>
      <div class='hero-eye'>Phase 1 of 4</div>
      <h1>Profile &amp; Bronze STTM</h1>
      <p>The Profiler agent inspects your CSV files and the STTM Generator
         proposes Bronze-layer mapping rules.</p>
    </div>
    <div class='ph-strip ph-bronze'>
      <span class='badge bronze-badge'>Bronze</span>
      <span style='font-size:.82rem;color:var(--txt2)'>
        Tools: <code style='font-size:.78rem'>profiler_agent_tool</code> &nbsp;·&nbsp;
               <code style='font-size:.78rem'>sttm_agent_tool</code>
      </span>
    </div>""", unsafe_allow_html=True)

    files   = st.session_state.get("uploaded_files", [])
    intent  = st.session_state.get("business_intent", "")
    profile = st.session_state.get("profile_json")
    sttm    = st.session_state.get("sttm_bronze")

    if not files:
        st.error("No files uploaded. Please go back to the home page.")
        if st.button("← Back to Home"):
            st.session_state.pipeline_started = False
            st.rerun()
        return

    # ── Run agents ────────────────────────────────────────────────────────────
    if profile is None:
        if st.button("▶ Run Profiler Agent", use_container_width=True):
            with st.spinner("Profiler agent analysing files..."):
                add_log("phase1", "🤖 [Supervisor] Dispatching Profiler agent...")
                time.sleep(0.3)
                add_log("phase1", f"📂 [Profiler] Reading {len(files)} file(s)...")
                result = profiler.run(files)
                st.session_state.profile_json = result
                for fname, fp in result.items():
                    add_log("phase1", f"<span class='lg'>✓ [Profiler] {fname} — {fp['row_count']} rows, {fp['column_count']} cols, quality={fp['quality_score']}%</span>")
                add_log("phase1", "<span class='la'>→ [Supervisor] Profile complete. Dispatching STTM Generator (Bronze)...</span>")
                time.sleep(0.2)
                sttm_result = sttm_generator.generate_bronze_sttm(result)
                st.session_state.sttm_bronze = sttm_result
                add_log("phase1", f"<span class='lb'>✓ [STTM Gen] sttm_bronze.csv — {len(sttm_result)} rules generated</span>")
                add_log("phase1", "<span class='lm'>⏸  [Supervisor] Awaiting HITL Gate 1 — Bronze Review</span>")
            st.rerun()
    else:
        # ── Profile results ───────────────────────────────────────────────────
        st.markdown("<div class='card-t'>📊 Data Profile</div>", unsafe_allow_html=True)
        for fname, fp in profile.items():
            with st.expander(f"📄 {fname}  —  {fp['row_count']:,} rows · {fp['column_count']} cols · Quality: {fp['quality_score']}%", expanded=True):
                import pandas as pd
                rows = []
                for col, info in fp["columns"].items():
                    rows.append({
                        "Column": col,
                        "Semantic": info["semantic"],
                        "Type": info["dtype"],
                        "Nulls %": f"{info['null_pct']}%",
                        "Unique": info["unique_count"],
                        "Cardinality": info["cardinality"],
                        "Top Values": ", ".join(info["top_values"][:3]),
                    })
                st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

        # ── STTM Bronze ───────────────────────────────────────────────────────
        if sttm is not None:
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown("<div class='card-t'>🗺️ Bronze STTM — Source-to-Target Mapping</div>", unsafe_allow_html=True)
            st.caption("Proposed mapping rules for Bronze ingestion. Review then proceed to HITL Gate.")
            st.dataframe(sttm, use_container_width=True, hide_index=True)

            c1, c2 = st.columns([3,1])
            with c1:
                buf = sttm.to_csv(index=False).encode()
                st.download_button("⬇ Download sttm_bronze.csv", buf, "sttm_bronze.csv", "text/csv")
            with c2:
                if st.button("Proceed to HITL Gate 1 →", use_container_width=True):
                    advance_phase("phase1", "hitl_bronze")
                    st.rerun()

        # ── Agent log ─────────────────────────────────────────────────────────
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<div class='card-t'>🖥 Agent Log</div>", unsafe_allow_html=True)
        logs = st.session_state.agent_logs.get("phase1", [])
        log_html = "<br>".join(logs)
        st.markdown(f"<div class='log'>{log_html}</div>", unsafe_allow_html=True)
