import streamlit as st

EXAMPLE_INTENTS = [
    "Which properties have the highest cap rate growth over the last 12 months?",
    "Identify top-performing zip codes by median sale price and days-on-market.",
    "Flag inventory replenishment risks and evaluate supplier on-time rates.",
    "Analyse order fulfilment bottlenecks and carrier performance by region.",
    "Which customer segments drive the highest revenue per transaction?",
]

def render():
    st.markdown("""
    <div class='hero'>
      <div class='hero-eye'>Accelerate with AI Training Demo</div>
      <h1>🏭 IDAMP Pipeline</h1>
      <p>Intent-Driven Agentic Medallion Pipeline — Upload your CSVs, state your business question,
         and let autonomous AI agents transform your data through Bronze → Silver → Gold.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='qs'>
      💡 <strong>Quick start:</strong> Use the files in the <code>test_data/</code> folder —
      <code>properties.csv</code>, <code>transactions.csv</code>, <code>listings.csv</code>.
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("<div class='card-t'>📁 Upload Data Files</div>", unsafe_allow_html=True)
        st.caption("Select one or more CSV files")
        uploaded = st.file_uploader(
            "CSV files", type=["csv"], accept_multiple_files=True,
            label_visibility="collapsed",
        )
        if uploaded:
            st.session_state.uploaded_files = uploaded
            st.session_state.file_names = [f.name for f in uploaded]
            for f in uploaded:
                st.markdown(
                    f"<span class='pill pg'>✓ {f.name}</span>&nbsp;",
                    unsafe_allow_html=True,
                )

    with col2:
        st.markdown("<div class='card-t'>🎯 Business Intent</div>", unsafe_allow_html=True)
        st.caption("What business question should the pipeline answer?")
        intent = st.text_area(
            "intent", value=st.session_state.get("business_intent", ""),
            height=130, label_visibility="collapsed",
            placeholder="e.g. Which zip codes show the highest cap rate growth over the last 12 months and what drives it?",
        )
        if intent:
            st.session_state.business_intent = intent

        st.markdown("<div style='margin-top:.5rem;font-size:.78rem;color:var(--txt2)'>Example intents:</div>", unsafe_allow_html=True)
        for ex in EXAMPLE_INTENTS[:3]:
            if st.button(f"↗ {ex[:65]}…" if len(ex) > 65 else f"↗ {ex}", key=f"ex_{ex[:20]}", use_container_width=True):
                st.session_state.business_intent = ex
                st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)

    # Architecture overview
    st.markdown("<div class='card-t' style='margin-bottom:.85rem'>Pipeline Architecture</div>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    layers = [
        ("🔶", "Bronze", "CSV → Parquet\nMetadata injection\nRaw fidelity", "pb"),
        ("⚙️",  "Silver", "Cleansing & dedup\nType casting\nSurrogate keys",  "ps"),
        ("🏆", "Gold",   "Joins & aggregation\nKPI materialisation\nSQL-ready", "pgo"),
        ("📊", "Report", "Intent-driven SQL\nPlotly charts\nHTML output", "pg"),
    ]
    for col, (icon, name, desc, pill_cls) in zip([c1, c2, c3, c4], layers):
        with col:
            st.markdown(f"""
            <div class='card' style='text-align:center;padding:1rem'>
              <div style='font-size:1.6rem;margin-bottom:.5rem'>{icon}</div>
              <div><span class='pill {pill_cls}'>{name}</span></div>
              <div style='font-size:.78rem;color:var(--txt2);margin-top:.6rem;line-height:1.5;white-space:pre-line'>{desc}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # Launch button
    has_files  = bool(st.session_state.get("uploaded_files"))
    has_intent = bool(st.session_state.get("business_intent","").strip())

    if not has_files:
        st.warning("⬆️ Upload at least one CSV file to begin.")
    elif not has_intent:
        st.warning("🎯 Enter your business intent to begin.")
    else:
        if st.button("🚀 Start Pipeline — Phase 1", use_container_width=True):
            st.session_state.pipeline_started = True
            st.session_state.current_phase    = "phase1"
            st.rerun()
