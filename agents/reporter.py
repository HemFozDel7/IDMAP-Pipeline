"""Reporter Agent — queries Gold tables and generates HTML executive report."""
import pandas as pd
import json, time
from datetime import datetime

def run(gold_results: dict, intent: str, profile: dict) -> str:
    time.sleep(0.3)

    # Gather summary stats
    total_rows = sum(v["rows"] for v in gold_results.values())
    tables = list(gold_results.keys())
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    # Build table HTML for each gold table
    tables_html = ""
    charts_data = []
    for tname, tdata in gold_results.items():
        df = tdata["dataframe"]
        if df.empty:
            continue
        preview = df.head(10)
        thead = "".join(f"<th>{c}</th>" for c in preview.columns)
        tbody = ""
        for _, row in preview.iterrows():
            cells = "".join(f"<td>{v}</td>" for v in row.values)
            tbody += f"<tr>{cells}</tr>"

        tables_html += f"""
        <div class="section">
            <h2>📊 {tname}</h2>
            <p class="meta">{tdata['rows']:,} rows · {tdata['cols']} columns</p>
            <div class="table-wrap">
                <table>
                    <thead><tr>{thead}</tr></thead>
                    <tbody>{tbody}</tbody>
                </table>
            </div>
        </div>"""

        # Prepare chart data (first numeric col)
        num_cols = df.select_dtypes(include="number").columns.tolist()
        cat_cols = [c for c in df.columns if c not in num_cols and not c.startswith("_")]
        if num_cols and cat_cols:
            sample = df[[cat_cols[0], num_cols[0]]].head(10)
            charts_data.append({
                "id": tname.replace(".","_"),
                "label": cat_cols[0],
                "value": num_cols[0],
                "title": f"{num_cols[0]} by {cat_cols[0]}",
                "labels": [str(x) for x in sample[cat_cols[0]].tolist()],
                "values": [float(x) if pd.notna(x) else 0 for x in sample[num_cols[0]].tolist()],
            })

    # Build chart canvases
    charts_html = ""
    chart_js = ""
    for cd in charts_data[:3]:
        charts_html += f'<div class="chart-wrap"><canvas id="{cd["id"]}"></canvas></div>'
        labels_json = json.dumps(cd["labels"])
        values_json = json.dumps(cd["values"])
        chart_js += f"""
        new Chart(document.getElementById('{cd["id"]}'), {{
            type: 'bar',
            data: {{
                labels: {labels_json},
                datasets: [{{
                    label: '{cd["title"]}',
                    data: {values_json},
                    backgroundColor: 'rgba(134,188,37,0.7)',
                    borderColor: '#86BC25',
                    borderWidth: 1,
                    borderRadius: 4,
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{ labels: {{ color:'#E8EAF0', font:{{ family:'Inter' }} }} }},
                    title: {{ display:true, text:'{cd["title"]}', color:'#E8EAF0', font:{{ size:13 }} }}
                }},
                scales: {{
                    x: {{ ticks:{{ color:'#8B90A8' }}, grid:{{ color:'#2D3148' }} }},
                    y: {{ ticks:{{ color:'#8B90A8' }}, grid:{{ color:'#2D3148' }} }}
                }}
            }}
        }});"""

    # Source file summary
    src_rows = ""
    for fname, fp in profile.items():
        src_rows += f"<tr><td>{fname}</td><td>{fp['row_count']:,}</td><td>{fp['column_count']}</td><td>{fp['quality_score']}%</td></tr>"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>IDAMP Executive Report</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
  *{{ margin:0; padding:0; box-sizing:border-box; }}
  body{{ background:#0F1117; color:#E8EAF0; font-family:'Inter',sans-serif; padding:2rem; }}
  .header{{ border-bottom:1px solid #2D3148; padding-bottom:1.5rem; margin-bottom:2rem; }}
  .header h1{{ font-size:1.8rem; font-weight:700; letter-spacing:-.03em; }}
  .header .badge{{ display:inline-block; background:rgba(134,188,37,.15); color:#86BC25;
      border:1px solid #6A9420; padding:3px 12px; border-radius:20px; font-size:.72rem;
      font-weight:600; text-transform:uppercase; letter-spacing:.08em; margin-bottom:.75rem; }}
  .header p{{ color:#8B90A8; font-size:.9rem; line-height:1.6; margin-top:.5rem; }}
  .metrics{{ display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr));
      gap:1rem; margin:1.5rem 0; }}
  .mc{{ background:#1E2130; border:1px solid #2D3148; border-radius:8px; padding:1rem;
       text-align:center; }}
  .mv{{ font-size:1.6rem; font-weight:700; color:#86BC25; }}
  .ml{{ font-size:.65rem; text-transform:uppercase; letter-spacing:.09em; color:#545870; margin-top:3px; }}
  .section{{ background:#1A1D27; border:1px solid #2D3148; border-radius:8px;
      padding:1.25rem; margin-bottom:1.25rem; }}
  .section h2{{ font-size:1rem; font-weight:600; margin-bottom:.35rem; }}
  .meta{{ font-size:.78rem; color:#545870; margin-bottom:.85rem; }}
  .table-wrap{{ overflow-x:auto; }}
  table{{ width:100%; border-collapse:collapse; font-size:.78rem; }}
  th{{ background:#0F1117; color:#8B90A8; text-align:left; padding:8px 10px;
       font-size:.68rem; text-transform:uppercase; letter-spacing:.06em; border-bottom:1px solid #2D3148; }}
  td{{ padding:7px 10px; border-bottom:1px solid #1E2130; color:#C8CAD4; }}
  tr:last-child td{{ border-bottom:none; }}
  tr:hover td{{ background:#1E2130; }}
  .intent-box{{ background:rgba(0,118,168,.1); border:1px solid rgba(0,118,168,.35);
      border-radius:8px; padding:1rem 1.25rem; margin:1.5rem 0; }}
  .intent-box h3{{ color:#5BB3D8; font-size:.85rem; margin-bottom:.4rem; }}
  .intent-box p{{ font-size:.88rem; color:#A8AABC; line-height:1.5; }}
  .charts{{ display:grid; grid-template-columns:repeat(auto-fit,minmax(320px,1fr)); gap:1.25rem; margin:1.5rem 0; }}
  .chart-wrap{{ background:#1E2130; border:1px solid #2D3148; border-radius:8px; padding:1rem; }}
  .footer{{ margin-top:2rem; padding-top:1rem; border-top:1px solid #2D3148;
      font-size:.72rem; color:#545870; display:flex; justify-content:space-between; }}
</style>
</head>
<body>
<div class="header">
  <div class="badge">✅ Pipeline Complete</div>
  <h1>IDAMP Executive Report</h1>
  <p><strong>Business Intent:</strong> {intent}</p>
  <p style="color:#545870;font-size:.78rem;margin-top:.4rem;">Generated: {now}</p>
</div>

<div class="metrics">
  <div class="mc"><div class="mv">{len(tables)}</div><div class="ml">Gold Tables</div></div>
  <div class="mc"><div class="mv">{total_rows:,}</div><div class="ml">Total Rows</div></div>
  <div class="mc"><div class="mv">{len(profile)}</div><div class="ml">Source Files</div></div>
  <div class="mc"><div class="mv">4</div><div class="ml">Pipeline Phases</div></div>
</div>

<div class="intent-box">
  <h3>🎯 Business Question Answered</h3>
  <p>{intent}</p>
</div>

<div class="section">
  <h2>📁 Source Data Summary</h2>
  <div class="table-wrap"><table>
    <thead><tr><th>File</th><th>Rows</th><th>Columns</th><th>Quality</th></tr></thead>
    <tbody>{src_rows}</tbody>
  </table></div>
</div>

<div class="charts">{charts_html}</div>

{tables_html}

<div class="footer">
  <span>IDAMP Pipeline — Accelerate with AI Training Demo</span>
  <span>{now}</span>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {{
  {chart_js}
}});
</script>
</body></html>"""
    return html
