from pathlib import Path
import pandas as pd
from .paths import RAW_DIR, PROC_DIR, TABLES_DIR

def read_csv_from_raw(filename: str | Path, **kwargs) -> pd.DataFrame:
    """Read a CSV located in 01_data/raw."""
    return pd.read_csv(RAW_DIR / filename, **kwargs)

def read_excel_from_raw(filename: str | Path, **kwargs) -> pd.DataFrame:
    """Read an Excel file located in 01_data/raw."""
    return pd.read_excel(RAW_DIR / filename, **kwargs)

def write_csv_to_processed(df: pd.DataFrame, filename: str | Path, index: bool=False, **kwargs) -> Path:
    """Write a DataFrame to 01_data/processed and return the output path."""
    out_path = PROC_DIR / filename
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=index, **kwargs)
    return out_path

def write_table(df: pd.DataFrame, filename: str | Path, index: bool=False, **kwargs) -> Path:
    """Save a 'final' table into 05_results/tables."""
    out_path = TABLES_DIR / filename
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=index, **kwargs)
    return out_path

