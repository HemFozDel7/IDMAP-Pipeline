"""Pipeline Complete page"""
import streamlit as st

def render():
    st.markdown("""
    <div class='hero'>
      <div class='hero-eye'>✅ Pipeline Complete</div>
      <h1>Pipeline Finished!</h1>
      <p>All four phases executed successfully. Your data has been transformed
         from raw CSV through Bronze → Silver → Gold, and the executive report is ready.</p>
    </div>""", unsafe_allow_html=True)

    # Summary metrics
    profile = st.session_state.get("profile_json", {})
    bronze  = st.session_state.get("bronze_parquets", {})
    silver  = st.session_state.get("silver_parquets", {})
    gold    = st.session_state.get("gold_tables", {})
    intent  = st.session_state.get("business_intent", "")
    report  = st.session_state.get("report_html", "")

    total_src  = sum(fp["row_count"] for fp in profile.values()) if profile else 0
    total_gold = sum(v["rows"] for v in gold.values()) if gold else 0

    st.markdown(f"""
    <div class='mrow'>
      <div class='mc mg'><div class='mv'>{len(profile)}</div><div class='ml'>Source Files</div></div>
      <div class='mc mb'><div class='mv'>{len(bronze)}</div><div class='ml'>Bronze Files</div></div>
      <div class='mc ms'><div class='mv'>{len(silver)}</div><div class='ml'>Silver Files</div></div>
      <div class='mc mgo'><div class='mv'>{len(gold)}</div><div class='ml'>Gold Tables</div></div>
      <div class='mc mg'><div class='mv'>{total_gold:,}</div><div class='ml'>Gold Rows</div></div>
    </div>""", unsafe_allow_html=True)

    # Business intent answered
    if intent:
        st.markdown(f"""
        <div style='background:rgba(134,188,37,.07);border:1px solid rgba(134,188,37,.3);
             border-radius:8px;padding:1rem 1.25rem;margin:1rem 0'>
          <div style='font-size:.72rem;font-weight:600;text-transform:uppercase;
               letter-spacing:.09em;color:var(--green);margin-bottom:.35rem'>
            🎯 Business Intent Answered
          </div>
          <div style='font-size:.9rem;color:var(--txt2);line-height:1.5'>{intent}</div>
        </div>""", unsafe_allow_html=True)

    # Downloads
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='card-t'>⬇️ Downloads</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Bronze Parquets**")
        for fname, fd in bronze.items():
            st.download_button(f"⬇ {fname}", fd["bytes"], fname, key=f"fin_b_{fname}")

    with col2:
        st.markdown("**Silver Parquets**")
        for fname, fd in silver.items():
            st.download_button(f"⬇ {fname}", fd["bytes"], fname, key=f"fin_s_{fname}")

    with col3:
        st.markdown("**Gold Tables**")
        for fname, fd in gold.items():
            st.download_button(f"⬇ {fname}", fd["bytes"], fname, key=f"fin_g_{fname}")

    if report:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.download_button(
            "📊 Download Executive Report (report.html)",
            report.encode(), "report_idamp.html", "text/html",
            use_container_width=True,
        )

    # Phase timeline
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='card-t'>Pipeline Timeline</div>", unsafe_allow_html=True)
    phases_summary = [
        ("🔶", "Phase 1", "Profile & Bronze STTM",  "profile.json + sttm_bronze.csv"),
        ("⏸", "Gate 1",  "Bronze HITL Review",       "Human approved Bronze rules"),
        ("⚙️", "Phase 2", "Bronze Execute & Silver STTM", f"{len(bronze)} parquet(s) + sttm_silver.csv"),
        ("⏸", "Gate 2",  "Silver HITL Review",       "Human approved Silver rules"),
        ("🏆", "Phase 3", "Silver Execute & Gold STTM",   f"{len(silver)} parquet(s) + sttm_gold.csv"),
        ("⏸", "Gate 3",  "Gold HITL Review",         "Human approved Gold rules"),
        ("📊", "Phase 4", "Gold Execute & Report",    f"{len(gold)} gold table(s) + report.html"),
    ]
    for icon, tag, title, output in phases_summary:
        st.markdown(f"""
        <div style='display:flex;align-items:flex-start;gap:12px;padding:9px 0;
             border-bottom:1px solid var(--border);font-size:.84rem'>
          <span style='font-size:1.1rem;line-height:1.2'>{icon}</span>
          <div>
            <span class='pill pg' style='margin-right:6px'>{tag}</span>
            <strong style='color:var(--txt)'>{title}</strong>
            <div style='color:var(--txt2);margin-top:3px;font-size:.78rem'>{output}</div>
          </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    if st.button("🔄 Run Another Pipeline", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
