"""Phase 2 — Bronze Execute & Silver STTM"""
import streamlit as st, time, pandas as pd
from utils.state import advance_phase, add_log
from agents import bronze_agent, sttm_generator

def render():
    st.markdown("""
    <div class='hero'>
      <div class='hero-eye'>Phase 2 of 4</div>
      <h1>Bronze Execute &amp; Silver STTM</h1>
      <p>The Bronze Agent ingests your CSVs into Parquet, then the STTM Generator
         proposes Silver cleansing rules.</p>
    </div>
    <div class='ph-strip ph-bronze'>
      <span class='badge bronze-badge'>Bronze → Silver</span>
      <span style='font-size:.82rem;color:var(--txt2)'>
        Tools: <code style='font-size:.78rem'>bronze_agent_tool</code> &nbsp;·&nbsp;
               <code style='font-size:.78rem'>sttm_agent_tool</code>
      </span>
    </div>""", unsafe_allow_html=True)

    files   = st.session_state.get("uploaded_files", [])
    sttm_b  = st.session_state.get("sttm_bronze")
    bronze  = st.session_state.get("bronze_parquets", {})
    sttm_s  = st.session_state.get("sttm_silver")
    profile = st.session_state.get("profile_json", {})
    intent  = st.session_state.get("business_intent", "")

    if not bronze:
        if st.button("▶ Run Bronze Agent", use_container_width=True):
            with st.spinner("Bronze Agent ingesting files..."):
                add_log("phase2", "🤖 [Supervisor] Dispatching Bronze Agent...")
                time.sleep(0.3)
                add_log("phase2", f"🔶 [Bronze] Reading approved sttm_bronze.csv ({len(sttm_b)} rules)...")
                result = bronze_agent.run(files, sttm_b)
                st.session_state.bronze_parquets = result
                for fname, fd in result.items():
                    add_log("phase2", f"<span class='lb'>✓ [Bronze] {fname} — {fd['rows']} rows, {fd['cols']} cols</span>")
                add_log("phase2", "<span class='la'>→ [Supervisor] Bronze complete. Dispatching STTM Generator (Silver)...</span>")
                time.sleep(0.2)
                sttm_result = sttm_generator.generate_silver_sttm(profile, intent)
                st.session_state.sttm_silver = sttm_result
                add_log("phase2", f"<span class='ls'>✓ [STTM Gen] sttm_silver.csv — {len(sttm_result)} rules</span>")
                add_log("phase2", "<span class='lm'>⏸  [Supervisor] Awaiting HITL Gate 2 — Silver Review</span>")
            st.rerun()
    else:
        # Bronze results
        st.markdown("<div class='card-t'>🔶 Bronze Layer Output</div>", unsafe_allow_html=True)
        mc = st.columns(len(bronze))
        for col, (fname, fd) in zip(mc, bronze.items()):
            with col:
                st.markdown(f"""<div class='card' style='text-align:center'>
                  <div class='mv' style='color:var(--bronze);font-size:1.5rem;font-weight:700'>{fd['rows']:,}</div>
                  <div style='font-size:.72rem;color:var(--txt2);margin:.3rem 0'>{fname}</div>
                  <div><span class='pill pb'>{fd['cols']} cols</span></div>
                  </div>""", unsafe_allow_html=True)
                st.download_button(f"⬇ {fname}", fd["bytes"], fname, key=f"dl_b_{fname}")

        # Silver STTM
        if sttm_s is not None:
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown("<div class='card-t'>⚙️ Silver STTM — Cleansing Rules</div>", unsafe_allow_html=True)
            st.dataframe(sttm_s, use_container_width=True, hide_index=True)

            c1, c2 = st.columns([3,1])
            with c1:
                buf = sttm_s.to_csv(index=False).encode()
                st.download_button("⬇ Download sttm_silver.csv", buf, "sttm_silver.csv", "text/csv")
            with c2:
                if st.button("Proceed to HITL Gate 2 →", use_container_width=True):
                    advance_phase("phase2", "hitl_silver")
                    st.rerun()

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<div class='card-t'>🖥 Agent Log</div>", unsafe_allow_html=True)
        logs = st.session_state.agent_logs.get("phase2", [])
        st.markdown(f"<div class='log'>{'<br>'.join(logs)}</div>", unsafe_allow_html=True)
