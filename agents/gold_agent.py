"""Gold Agent — joins, aggregations, KPI materialisation."""
import pandas as pd
import io
import time


def _safe_dedup(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicate columns — keeps first occurrence."""
    return df.loc[:, ~df.columns.duplicated(keep="first")]


def run(silver_results: dict, sttm: pd.DataFrame, intent: str) -> dict:
    time.sleep(0.4)
    results = {}

    # ── Sanitise every incoming silver frame immediately ──────────────────────
    silver_dfs = {}
    for k, v in silver_results.items():
        df = v["dataframe"].copy()
        df = _safe_dedup(df)
        silver_dfs[k] = df

    for _, row in sttm.iterrows():
        tname   = row["output_table"]
        src_key = row["source_silver"]

        # ── KPI summary table ─────────────────────────────────────────────────
        if src_key == "ALL":
            rows = []
            for src_name, df in silver_dfs.items():
                for col in df.select_dtypes(include="number").columns:
                    clean = df[col].dropna()
                    if clean.empty:
                        continue
                    rows.append({
                        "source_table": src_name,
                        "metric":       col,
                        "sum":          round(float(clean.sum()),  2),
                        "mean":         round(float(clean.mean()), 2),
                        "count":        int(clean.count()),
                        "min":          round(float(clean.min()),  2),
                        "max":          round(float(clean.max()),  2),
                    })
            if rows:
                out = pd.DataFrame(rows)
                buf = io.BytesIO()
                out.to_parquet(buf, index=False)
                results["kpi_summary.parquet"] = {
                    "dataframe": out,
                    "bytes":     buf.getvalue(),
                    "rows":      len(out),
                    "cols":      len(out.columns),
                }
            continue

        # ── Find matching silver dataframe ────────────────────────────────────
        silver_key = next(
            (k for k in silver_dfs if src_key.replace(".csv", "") in k),
            None,
        )
        if silver_key is None:
            continue

        df = silver_dfs[silver_key].copy()
        df = _safe_dedup(df)

        num_cols = df.select_dtypes(include="number").columns.tolist()
        cat_cols = [
            c for c in df.select_dtypes(include="object").columns
            if not c.startswith("_") and not c.startswith("sk_")
        ]

        # ── Dimension table ───────────────────────────────────────────────────
        if "dim_" in tname:
            out = df[cat_cols[:6]].drop_duplicates() if cat_cols else df.head(50)

        # ── Fact / aggregation table ──────────────────────────────────────────
        else:
            grp_cols = [c for c in cat_cols if df[c].nunique() < 30][:2]
            if grp_cols and num_cols:
                agg = (
                    df.groupby(grp_cols)[num_cols[:4]]
                    .agg(["sum", "mean"])
                    .round(2)
                    .reset_index()
                )
                # Flatten MultiIndex columns
                agg.columns = [
                    "_".join(filter(None, c)) if isinstance(c, tuple) else c
                    for c in agg.columns
                ]
                out = _safe_dedup(agg)
            else:
                out = df.copy()

        # ── Final safety dedup before writing parquet ─────────────────────────
        out = _safe_dedup(out)

        buf = io.BytesIO()
        out.to_parquet(buf, index=False)
        results[tname + ".parquet"] = {
            "dataframe": out,
            "bytes":     buf.getvalue(),
            "rows":      len(out),
            "cols":      len(out.columns),
        }

    return results