"""Profiler Agent — inspects uploaded CSVs and returns a profile JSON."""
import pandas as pd
import json
import time

SEMANTIC_MAP = {
    "price": "monetary_value", "cost": "monetary_value", "revenue": "monetary_value",
    "amount": "monetary_value", "sale": "monetary_value",
    "date": "temporal", "time": "temporal", "year": "temporal", "month": "temporal",
    "id": "identifier", "key": "identifier", "code": "identifier", "sk": "identifier",
    "name": "descriptor", "description": "descriptor", "label": "descriptor",
    "zip": "geographic", "city": "geographic", "state": "geographic",
    "lat": "geographic", "lon": "geographic", "address": "geographic",
    "qty": "quantity", "count": "quantity", "units": "quantity", "sqft": "quantity",
    "rate": "metric", "ratio": "metric", "pct": "metric", "percent": "metric",
    "score": "metric", "index": "metric",
}

def infer_semantic(col_name: str) -> str:
    col_lower = col_name.lower()
    for kw, sem in SEMANTIC_MAP.items():
        if kw in col_lower:
            return sem
    return "attribute"

def profile_dataframe(name: str, df: pd.DataFrame) -> dict:
    cols = {}
    for col in df.columns:
        series = df[col]
        null_count = int(series.isnull().sum())
        unique_count = int(series.nunique())
        dtype = str(series.dtype)
        top_vals = series.dropna().value_counts().head(3).index.tolist()
        col_info = {
            "dtype": dtype,
            "null_count": null_count,
            "null_pct": round(null_count / len(df) * 100, 1) if len(df) > 0 else 0,
            "unique_count": unique_count,
            "cardinality": "high" if unique_count > len(df) * 0.5 else ("medium" if unique_count > 10 else "low"),
            "top_values": [str(v) for v in top_vals],
            "semantic": infer_semantic(col),
        }
        if pd.api.types.is_numeric_dtype(series):
            col_info["min"] = float(series.min()) if not series.empty else None
            col_info["max"] = float(series.max()) if not series.empty else None
            col_info["mean"] = round(float(series.mean()), 2) if not series.empty else None
        cols[col] = col_info

    return {
        "source_file": name,
        "row_count": len(df),
        "column_count": len(df.columns),
        "columns": cols,
        "quality_score": round(
            100 - (sum(c["null_pct"] for c in cols.values()) / max(len(cols), 1)), 1
        ),
    }

def run(uploaded_files: list) -> dict:
    """Profile all uploaded files and return combined profile JSON."""
    import streamlit as st
    time.sleep(0.3)
    profiles = {}
    for uf in uploaded_files:
        uf.seek(0)
        df = pd.read_csv(uf)
        profiles[uf.name] = profile_dataframe(uf.name, df)
    return profiles
