import streamlit as st

def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --bg:        #0F1117;
        --bg2:       #1A1D27;
        --bg3:       #1E2130;
        --border:    #2D3148;
        --border2:   #3A3F5C;
        --green:     #86BC25;
        --green-dim: #6A9420;
        --green-glow:rgba(134,188,37,0.12);
        --teal:      #007680;
        --blue:      #0076A8;
        --bronze:    #CD7F32;
        --silver:    #A8AABC;
        --gold:      #C9A84C;
        --amber:     #F59E0B;
        --amber-bg:  rgba(245,158,11,0.10);
        --red:       #EF4444;
        --txt:       #E8EAF0;
        --txt2:      #8B90A8;
        --txt3:      #545870;
        --mono:      'JetBrains Mono', monospace;
        --r:         8px;
    }
    .stApp { background:var(--bg); font-family:'Inter',sans-serif; color:var(--txt); }

    /* hide streamlit chrome */
    [data-testid="stHeader"],footer,[data-testid="stToolbar"],[data-testid="stDecoration"],
    .stDeployButton { display:none!important; }

    /* sidebar */
    [data-testid="stSidebar"] {
        background:var(--bg2)!important;
        border-right:1px solid var(--border)!important;
    }
    [data-testid="stSidebar"] > div:first-child { padding-top:1.25rem; }

    .sb-header { display:flex; align-items:center; gap:12px; padding:0 1rem 1rem; }
    .sb-icon   { font-size:2rem; line-height:1; }
    .sb-title  { font-size:.95rem; font-weight:700; color:var(--txt); letter-spacing:-.01em; }
    .sb-sub    { font-size:.68rem; font-weight:600; text-transform:uppercase;
                 letter-spacing:.1em; color:var(--green); margin-top:2px; }
    .sb-div    { height:1px; background:var(--border); margin:.25rem 0 .75rem; }

    .ph-item   { display:flex; align-items:center; gap:9px; padding:6px 14px;
                 margin:2px 0; border-radius:6px; }
    .ph-lbl    { font-size:.76rem; font-weight:500; line-height:1.3; }
    .ph-ico    { font-size:.7rem; width:14px; text-align:center; flex-shrink:0; }
    .ph-active { background:var(--green-glow); border:1px solid var(--green-dim); }
    .ph-active .ph-lbl,.ph-active .ph-ico { color:var(--green); }
    .ph-done .ph-lbl   { color:var(--txt2); }
    .ph-done .ph-ico   { color:var(--green); }
    .ph-pend .ph-lbl,.ph-pend .ph-ico { color:var(--txt3); }

    /* main */
    .main .block-container { padding:2rem 2.5rem; max-width:1080px; }

    /* hero */
    .hero-eye { font-size:.68rem; font-weight:600; text-transform:uppercase;
                letter-spacing:.12em; color:var(--green); margin-bottom:.4rem; }
    .hero h1  { font-size:2rem; font-weight:700; letter-spacing:-.03em;
                color:var(--txt); margin:0 0 .4rem; line-height:1.15; }
    .hero p   { font-size:.93rem; color:var(--txt2); line-height:1.6; margin:0; }

    /* cards */
    .card  { background:var(--bg3); border:1px solid var(--border);
             border-radius:var(--r); padding:1.4rem; margin-bottom:.9rem; }
    .card-t{ font-size:.72rem; font-weight:600; text-transform:uppercase;
             letter-spacing:.09em; color:var(--txt2); margin-bottom:.6rem; }

    /* quickstart */
    .qs { background:rgba(0,118,168,.09); border:1px solid rgba(0,118,168,.35);
          border-radius:var(--r); padding:.85rem 1.1rem; margin-bottom:1.25rem;
          font-size:.85rem; color:var(--txt2); }
    .qs strong { color:#5BB3D8; }
    .qs code   { background:rgba(255,255,255,.07); padding:1px 5px; border-radius:3px;
                 font-family:var(--mono); font-size:.78rem; color:#A8D8EA; }

    /* HITL box */
    .hitl { background:var(--amber-bg); border:1.5px solid var(--amber);
            border-radius:var(--r); padding:1.1rem 1.3rem; margin:1rem 0; }
    .hitl h3 { color:var(--amber); font-size:.95rem; margin:0 0 .4rem;
               display:flex; align-items:center; gap:7px; }
    .hitl p  { color:var(--txt2); font-size:.84rem; margin:0; line-height:1.5; }

    /* agent log */
    .log { background:var(--bg2); border:1px solid var(--border);
           border-radius:var(--r); padding:.85rem 1rem; font-family:var(--mono);
           font-size:.75rem; line-height:1.85; max-height:260px; overflow-y:auto;
           color:var(--txt2); }
    .lg  { color:var(--green); }
    .la  { color:var(--amber); }
    .lb  { color:var(--bronze); }
    .ls  { color:var(--silver); }
    .lgo { color:var(--gold); }
    .lt  { color:var(--teal); }
    .lm  { color:var(--txt3); }

    /* pills */
    .pill { display:inline-block; padding:2px 9px; border-radius:20px;
            font-size:.68rem; font-weight:600; text-transform:uppercase; letter-spacing:.06em; }
    .pg { background:var(--green-glow); color:var(--green); border:1px solid var(--green-dim); }
    .pa { background:var(--amber-bg);   color:var(--amber); border:1px solid #b47800; }
    .pb { background:rgba(205,127,50,.14); color:var(--bronze); border:1px solid rgba(205,127,50,.4); }
    .ps { background:rgba(168,170,188,.12); color:var(--silver); border:1px solid rgba(168,170,188,.35); }
    .pgo{ background:rgba(201,168,76,.14); color:var(--gold);  border:1px solid rgba(201,168,76,.4); }

    /* metric row */
    .mrow { display:grid; grid-template-columns:repeat(auto-fit,minmax(130px,1fr));
            gap:.85rem; margin:.85rem 0; }
    .mc   { background:var(--bg3); border:1px solid var(--border);
            border-radius:var(--r); padding:.9rem; text-align:center; }
    .mv   { font-size:1.7rem; font-weight:700; letter-spacing:-.03em; line-height:1; margin-bottom:3px; }
    .ml   { font-size:.65rem; text-transform:uppercase; letter-spacing:.09em; color:var(--txt3); }
    .mg .mv{ color:var(--green); } .mt .mv{ color:var(--teal); }
    .mb .mv{ color:var(--bronze); } .ms .mv{ color:var(--silver); }
    .mgo .mv{ color:var(--gold); }

    /* step list */
    .sl li { display:flex; align-items:flex-start; gap:10px; padding:9px 0;
             border-bottom:1px solid var(--border); font-size:.84rem; color:var(--txt2); }
    .sl li:last-child { border-bottom:none; }
    .sn { width:20px; height:20px; border-radius:50%; background:var(--green-glow);
          border:1px solid var(--green-dim); color:var(--green); font-size:.68rem;
          font-weight:700; display:flex; align-items:center; justify-content:center;
          flex-shrink:0; margin-top:1px; }
    .st strong { color:var(--txt); display:block; margin-bottom:1px; }

    /* phase header strip */
    .ph-strip { display:flex; align-items:center; gap:10px; padding:.6rem 1rem;
                border-radius:var(--r); margin-bottom:1.25rem; }
    .ph-bronze { background:rgba(205,127,50,.1); border:1px solid rgba(205,127,50,.35); }
    .ph-silver { background:rgba(168,170,188,.1); border:1px solid rgba(168,170,188,.3); }
    .ph-gold   { background:rgba(201,168,76,.1);  border:1px solid rgba(201,168,76,.4); }
    .ph-strip .badge { font-size:.72rem; font-weight:700; text-transform:uppercase;
                       letter-spacing:.1em; padding:3px 10px; border-radius:4px; }
    .bronze-badge { background:rgba(205,127,50,.2); color:var(--bronze); }
    .silver-badge { background:rgba(168,170,188,.15); color:var(--silver); }
    .gold-badge   { background:rgba(201,168,76,.2); color:var(--gold); }

    /* buttons */
    .stButton > button {
        background:var(--green)!important; color:#0A0D08!important;
        font-weight:600!important; border:none!important; border-radius:6px!important;
        font-size:.84rem!important; padding:.45rem 1.1rem!important;
        transition:background .15s!important; font-family:'Inter',sans-serif!important;
    }
    .stButton > button:hover { background:var(--green-dim)!important; }

    /* file uploader */
    [data-testid="stFileUploader"] {
        background:var(--bg3)!important;
        border:1.5px dashed var(--border2)!important;
        border-radius:var(--r)!important;
    }

    /* text area */
    textarea {
        background:var(--bg3)!important; border:1px solid var(--border2)!important;
        color:var(--txt)!important; border-radius:6px!important;
        font-family:'Inter',sans-serif!important; font-size:.87rem!important;
    }
    textarea:focus { border-color:var(--green-dim)!important;
                     box-shadow:0 0 0 2px var(--green-glow)!important; }

    /* dataframe */
    [data-testid="stDataFrame"] th {
        background:var(--bg2)!important; color:var(--txt2)!important;
        font-size:.72rem!important; text-transform:uppercase!important; letter-spacing:.05em!important;
    }
    [data-testid="stDataFrame"] { border-radius:var(--r)!important; overflow:hidden!important; }

    /* expander */
    [data-testid="stExpander"] {
        background:var(--bg3)!important; border:1px solid var(--border)!important;
        border-radius:var(--r)!important;
    }

    /* checkbox */
    [data-testid="stCheckbox"] label { font-size:.85rem!important; color:var(--txt)!important; }

    /* scrollbar */
    ::-webkit-scrollbar { width:5px; height:5px; }
    ::-webkit-scrollbar-track { background:var(--bg); }
    ::-webkit-scrollbar-thumb { background:var(--border2); border-radius:3px; }
    </style>
    """, unsafe_allow_html=True)
