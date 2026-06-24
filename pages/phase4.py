"""Phase 4 — Gold Execute & Report"""
import streamlit as st, time
from utils.state import advance_phase, add_log
from agents import gold_agent, reporter

def render():
    st.markdown("""
    <div class='hero'>
      <div class='hero-eye'>Phase 4 of 4 — Final</div>
      <h1>Gold Execute &amp; Report</h1>
      <p>The Gold Agent materialises analytics-ready tables and the Reporter
         generates your executive HTML report. No further gates.</p>
    </div>
    <div class='ph-strip ph-gold'>
      <span class='badge gold-badge'>Gold</span>
      <span style='font-size:.82rem;color:var(--txt2)'>
        Tools: <code style='font-size:.78rem'>gold_agent_tool</code> &nbsp;·&nbsp;
               <code style='font-size:.78rem'>reporter_agent_tool</code> &nbsp;·&nbsp;
               No HITL gate
      </span>
    </div>""", unsafe_allow_html=True)

    silver  = st.session_state.get("silver_parquets", {})
    sttm_g  = st.session_state.get("sttm_gold")
    gold    = st.session_state.get("gold_tables", {})
    report  = st.session_state.get("report_html", "")
    profile = st.session_state.get("profile_json", {})
    intent  = st.session_state.get("business_intent", "")

    if not gold:
        if st.button("▶ Run Gold Agent + Reporter (Final)", use_container_width=True):
            with st.spinner("Gold Agent materialising tables..."):
                add_log("phase4", "🤖 [Supervisor] Dispatching Gold Agent...")
                time.sleep(0.3)
                add_log("phase4", f"🏆 [Gold] Executing {len(sttm_g)} Gold STTM rules...")
                gold_result = gold_agent.run(silver, sttm_g, intent)
                st.session_state.gold_tables = gold_result
                for fname, fd in gold_result.items():
                    add_log("phase4", f"<span class='lgo'>✓ [Gold] {fname} — {fd['rows']} rows</span>")
                add_log("phase4", "<span class='la'>→ [Supervisor] Gold complete. Dispatching Reporter agent...</span>")
                time.sleep(0.3)
                add_log("phase4", "📊 [Reporter] Executing intent-driven SQL queries on Gold tables...")
                html = reporter.run(gold_result, intent, profile)
                st.session_state.report_html = html
                add_log("phase4", "<span class='lg'>✓ [Reporter] report.html generated successfully</span>")
                add_log("phase4", "<span class='lg'>✅ [Supervisor] Pipeline complete!</span>")
            advance_phase("phase4", "complete")
            st.rerun()
    else:
        # Gold tables
        st.markdown("<div class='card-t'>🏆 Gold Tables</div>", unsafe_allow_html=True)
        cols = st.columns(min(len(gold), 4))
        for col, (fname, fd) in zip(cols, gold.items()):
            with col:
                st.markdown(f"""<div class='card' style='text-align:center'>
                  <div class='mv' style='color:var(--gold);font-size:1.4rem;font-weight:700'>{fd['rows']:,}</div>
                  <div style='font-size:.68rem;color:var(--txt2);margin:.3rem 0'>{fname}</div>
                  <div><span class='pill pgo'>{fd['cols']} cols</span></div>
                </div>""", unsafe_allow_html=True)
                st.download_button(f"⬇ {fname}", fd["bytes"], fname, key=f"dl_g_{fname}")

        # Report download
        if report:
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown("<div class='card-t'>📊 Executive Report Ready</div>", unsafe_allow_html=True)
            st.success("✅ report.html has been generated. Download below or view in the Pipeline Complete page.")
            st.download_button(
                "⬇ Download report.html", report.encode(),
                "report_idamp.html", "text/html",
                use_container_width=True,
            )
            if st.button("🏁 View Pipeline Complete →", use_container_width=True):
                st.session_state.current_phase = "complete"
                st.rerun()

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<div class='card-t'>🖥 Agent Log</div>", unsafe_allow_html=True)
        logs = st.session_state.agent_logs.get("phase4", [])
        st.markdown(f"<div class='log'>{'<br>'.join(logs)}</div>", unsafe_allow_html=True)
