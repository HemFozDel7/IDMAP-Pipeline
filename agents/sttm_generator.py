"""STTM Generator Agent — produces Bronze / Silver / Gold mapping rules."""
import pandas as pd
import time

# ── Bronze STTM ───────────────────────────────────────────────────────────────
def generate_bronze_sttm(profile: dict) -> pd.DataFrame:
    time.sleep(0.2)
    rows = []
    for fname, fp in profile.items():
        for col, info in fp["columns"].items():
            target = col.lower().replace(" ", "_").replace("-", "_")
            rows.append({
                "source_file":   fname,
                "source_col":    col,
                "target_col":    target,
                "transformation":"rename + cast to string",
                "metadata_field":"No",
                "notes":         f"semantic={info['semantic']}, dtype={info['dtype']}",
                "approved":      True,
            })
        # Metadata injections
        for meta in ["_source_file", "_run_id", "_ingest_ts"]:
            rows.append({
                "source_file":   fname,
                "source_col":    "(injected)",
                "target_col":    meta,
                "transformation":"system_injection",
                "metadata_field":"Yes",
                "notes":         "Injected automatically at Bronze ingestion",
                "approved":      True,
            })
    return pd.DataFrame(rows)

# ── Silver STTM ───────────────────────────────────────────────────────────────
def generate_silver_sttm(profile: dict, intent: str) -> pd.DataFrame:
    time.sleep(0.2)
    rows = []
    for fname, fp in profile.items():
        for col, info in fp["columns"].items():
            target = col.lower().replace(" ", "_").replace("-", "_")
            # Null strategy
            if info["null_pct"] == 0:
                null_strat = "none_required"
            elif info["semantic"] in ("monetary_value", "quantity", "metric"):
                null_strat = "fill_median"
            elif info["semantic"] in ("geographic", "descriptor"):
                null_strat = "fill_mode"
            elif info["semantic"] == "temporal":
                null_strat = "fill_forward"
            else:
                null_strat = "flag_unknown"

            # Type cast
            dtype = info["dtype"]
            if "int" in dtype:      cast = "INT64"
            elif "float" in dtype:  cast = "DECIMAL(15,2)"
            elif "datetime" in dtype or "date" in info["semantic"]:
                cast = "DATE"
            else:                   cast = "VARCHAR"

            rows.append({
                "source_file":   fname,
                "source_col":    col,
                "target_col":    target,
                "null_strategy": null_strat,
                "type_cast":     cast,
                "dedup_key":     "Yes" if info["semantic"] == "identifier" else "No",
                "date_format":   "YYYY-MM-DD" if info["semantic"] == "temporal" else "N/A",
                "sk_prefix":     f"SK_{fname[:4].upper()}_" if info["semantic"] == "identifier" else "N/A",
                "approved":      True,
            })
    return pd.DataFrame(rows)

# ── Gold STTM ─────────────────────────────────────────────────────────────────
def generate_gold_sttm(profile: dict, intent: str) -> pd.DataFrame:
    time.sleep(0.2)
    files = list(profile.keys())
    rows = []

    # One output table per file + a KPI table
    for fname in files:
        fp = profile[fname]
        id_cols = [c for c, i in fp["columns"].items() if i["semantic"] == "identifier"]
        num_cols = [c for c, i in fp["columns"].items() if i["semantic"] in ("monetary_value","quantity","metric")]
        date_cols= [c for c, i in fp["columns"].items() if i["semantic"] == "temporal"]
        geo_cols = [c for c, i in fp["columns"].items() if i["semantic"] == "geographic"]

        tbl = fname.replace(".csv","").lower()

        rows.append({
            "output_table": f"dim_{tbl}",
            "source_silver": fname,
            "join_key":     ", ".join(id_cols[:2]) if id_cols else "N/A",
            "join_type":    "N/A",
            "aggregation":  "N/A",
            "kpi_formula":  "N/A",
            "group_by":     ", ".join(geo_cols[:2]) if geo_cols else "N/A",
            "intent_link":  "dimension lookup",
            "approved":     True,
        })

        if num_cols:
            rows.append({
                "output_table": f"fact_{tbl}",
                "source_silver": fname,
                "join_key":     ", ".join(id_cols[:1]) if id_cols else "N/A",
                "join_type":    "INNER" if len(files) > 1 else "N/A",
                "aggregation":  f"SUM({num_cols[0]}), AVG({num_cols[0]})" if num_cols else "COUNT(*)",
                "kpi_formula":  f"{num_cols[0]}_per_unit = {num_cols[0]} / NULLIF(units,0)" if len(num_cols)>1 else "N/A",
                "group_by":     ", ".join((geo_cols or date_cols or id_cols)[:2]),
                "intent_link":  "answers: " + intent[:60] + "...",
                "approved":     True,
            })

    # KPI summary table
    rows.append({
        "output_table": "kpi_summary",
        "source_silver": "ALL",
        "join_key":     "Derived",
        "join_type":    "CROSS",
        "aggregation":  "AVG, SUM, COUNT, PERCENTILE_50",
        "kpi_formula":  "intent_driven_kpi = aggregated_metric / baseline",
        "group_by":     "period, category",
        "intent_link":  "primary answer: " + intent[:50],
        "approved":     True,
    })

    return pd.DataFrame(rows)
