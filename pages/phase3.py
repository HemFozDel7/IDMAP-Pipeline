"""Phase 3 — Silver Execute & Gold STTM"""
import streamlit as st, time
from utils.state import advance_phase, add_log
from agents import silver_agent, sttm_generator

def render():
    st.markdown("""
    <div class='hero'>
      <div class='hero-eye'>Phase 3 of 4</div>
      <h1>Silver Execute &amp; Gold STTM</h1>
      <p>The Silver Agent cleanses and enriches data, then the STTM Generator
         proposes Gold joins, aggregations and KPI rules.</p>
    </div>
    <div class='ph-strip ph-silver'>
      <span class='badge silver-badge'>Silver → Gold</span>
      <span style='font-size:.82rem;color:var(--txt2)'>
        Tools: <code style='font-size:.78rem'>silver_agent_tool</code> &nbsp;·&nbsp;
               <code style='font-size:.78rem'>sttm_agent_tool</code>
      </span>
    </div>""", unsafe_allow_html=True)

    bronze  = st.session_state.get("bronze_parquets", {})
    sttm_s  = st.session_state.get("sttm_silver")
    silver  = st.session_state.get("silver_parquets", {})
    sttm_g  = st.session_state.get("sttm_gold")
    profile = st.session_state.get("profile_json", {})
    intent  = st.session_state.get("business_intent", "")

    if not silver:
        if st.button("▶ Run Silver Agent", use_container_width=True):
            with st.spinner("Silver Agent cleansing data..."):
                add_log("phase3", "🤖 [Supervisor] Dispatching Silver Agent...")
                time.sleep(0.3)
                add_log("phase3", f"⚙️ [Silver] Applying {len(sttm_s)} cleansing rules...")
                result = silver_agent.run(bronze, sttm_s)
                st.session_state.silver_parquets = result
                for fname, fd in result.items():
                    add_log("phase3", f"<span class='ls'>✓ [Silver] {fname} — {fd['rows']} rows, {fd['cols']} cols</span>")
                add_log("phase3", "<span class='la'>→ [Supervisor] Silver complete. Dispatching STTM Generator (Gold)...</span>")
                time.sleep(0.2)
                sttm_result = sttm_generator.generate_gold_sttm(profile, intent)
                st.session_state.sttm_gold = sttm_result
                add_log("phase3", f"<span class='lgo'>✓ [STTM Gen] sttm_gold.csv — {len(sttm_result)} output tables planned</span>")
                add_log("phase3", "<span class='lm'>⏸  [Supervisor] Awaiting HITL Gate 3 — Gold Review</span>")
            st.rerun()
    else:
        st.markdown("<div class='card-t'>⚙️ Silver Layer Output</div>", unsafe_allow_html=True)
        mc = st.columns(len(silver))
        for col, (fname, fd) in zip(mc, silver.items()):
            with col:
                st.markdown(f"""<div class='card' style='text-align:center'>
                  <div class='mv' style='color:var(--silver);font-size:1.5rem;font-weight:700'>{fd['rows']:,}</div>
                  <div style='font-size:.72rem;color:var(--txt2);margin:.3rem 0'>{fname}</div>
                  <div><span class='pill ps'>{fd['cols']} cols</span></div>
                  </div>""", unsafe_allow_html=True)
                st.download_button(f"⬇ {fname}", fd["bytes"], fname, key=f"dl_s_{fname}")

        # Preview
        with st.expander("Preview Silver data", expanded=False):
            import pandas as pd
            for fname, fd in silver.items():
                st.caption(fname)
                st.dataframe(fd["dataframe"].head(5), use_container_width=True, hide_index=True)

        if sttm_g is not None:
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown("<div class='card-t'>🏆 Gold STTM — Join & Aggregation Plan</div>", unsafe_allow_html=True)
            st.dataframe(sttm_g, use_container_width=True, hide_index=True)
            c1, c2 = st.columns([3,1])
            with c1:
                buf = sttm_g.to_csv(index=False).encode()
                st.download_button("⬇ Download sttm_gold.csv", buf, "sttm_gold.csv", "text/csv")
            with c2:
                if st.button("Proceed to HITL Gate 3 →", use_container_width=True):
                    advance_phase("phase3", "hitl_gold")
                    st.rerun()

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<div class='card-t'>🖥 Agent Log</div>", unsafe_allow_html=True)
        logs = st.session_state.agent_logs.get("phase3", [])
        st.markdown(f"<div class='log'>{'<br>'.join(logs)}</div>", unsafe_allow_html=True)
