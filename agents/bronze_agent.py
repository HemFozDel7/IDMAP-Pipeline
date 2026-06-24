"""Bronze Agent — CSV → Parquet ingestion with metadata injection."""
import pandas as pd
import io, time, uuid
from datetime import datetime

def run(uploaded_files: list, sttm: pd.DataFrame) -> dict:
    time.sleep(0.4)
    results = {}
    run_id = str(uuid.uuid4())[:8]
    ts = datetime.utcnow().isoformat()

    for uf in uploaded_files:
        uf.seek(0)
        df = pd.read_csv(uf)
        # Apply renames from STTM
        rename_map = {}
        for _, row in sttm[sttm["source_file"] == uf.name].iterrows():
            if row["source_col"] != "(injected)" and row["source_col"] in df.columns:
                rename_map[row["source_col"]] = row["target_col"]
        df.rename(columns=rename_map, inplace=True)
        # Inject metadata columns
        df["_source_file"] = uf.name
        df["_run_id"]      = run_id
        df["_ingest_ts"]   = ts
        buf = io.BytesIO()
        df.to_parquet(buf, index=False)
        results[uf.name.replace(".csv", "_bronze.parquet")] = {
            "dataframe": df,
            "bytes":     buf.getvalue(),
            "rows":      len(df),
            "cols":      len(df.columns),
        }
    return results
