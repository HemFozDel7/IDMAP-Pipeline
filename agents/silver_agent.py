"""Silver Agent — cleansing, dedup, type cast, date normalisation, SK."""
import pandas as pd
import io, time, uuid

def _dedup_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Rename any duplicate column names by appending a suffix."""
    seen = {}
    new_cols = []
    for col in df.columns:
        if col in seen:
            seen[col] += 1
            new_cols.append(f"{col}_{seen[col]}")
        else:
            seen[col] = 0
            new_cols.append(col)
    df.columns = new_cols
    return df

def run(bronze_results: dict, sttm: pd.DataFrame) -> dict:
    time.sleep(0.4)
    results = {}

    for bname, bdata in bronze_results.items():
        df = bdata["dataframe"].copy()

        # Fix duplicate columns immediately on entry
        df = _dedup_columns(df)

        src = bname.replace("_bronze.parquet", ".csv")
        rules = sttm[sttm["source_file"] == src]

        for _, row in rules.iterrows():
            col = row["target_col"]
            if col not in df.columns:
                continue

            # Null strategy
            ns = row.get("null_strategy", "flag_unknown")
            if ns == "fill_median" and pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].fillna(df[col].median())
            elif ns == "fill_mode":
                mode = df[col].mode()
                df[col] = df[col].fillna(mode[0] if not mode.empty else "Unknown")
            elif ns == "fill_forward":
                df[col] = df[col].ffill()
            elif ns == "flag_unknown":
                df[col] = df[col].fillna("Unknown")

            # Type cast
            tc = row.get("type_cast", "VARCHAR")
            try:
                if tc == "INT64":
                    df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
                elif tc == "DECIMAL(15,2)":
                    df[col] = pd.to_numeric(df[col], errors="coerce").round(2)
                elif tc == "DATE":
                    df[col] = pd.to_datetime(df[col], errors="coerce").dt.strftime("%Y-%m-%d")
            except Exception:
                pass

            # Surrogate key
            sk_prefix = row.get("sk_prefix", "N/A")
            if row.get("dedup_key") == "Yes" and sk_prefix != "N/A":
                sk_col = "sk_" + col
                if sk_col not in df.columns:  # don't add twice
                    df[sk_col] = [sk_prefix + str(uuid.uuid4())[:8] for _ in range(len(df))]

        # Dedup on identifier columns
        id_cols = [
            r["target_col"] for _, r in rules.iterrows()
            if r.get("dedup_key") == "Yes" and r["target_col"] in df.columns
        ]
        if id_cols:
            df = df.drop_duplicates(subset=id_cols, keep="last")

        df = df.reset_index(drop=True)

        # Final dedup columns safety check before writing
        df = _dedup_columns(df)

        buf = io.BytesIO()
        df.to_parquet(buf, index=False)
        results[bname.replace("_bronze.parquet", "_silver.parquet")] = {
            "dataframe": df,
            "bytes":     buf.getvalue(),
            "rows":      len(df),
            "cols":      len(df.columns),
        }

    return results