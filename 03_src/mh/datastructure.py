# 03_src/mh/datastructure.py

from __future__ import annotations
from typing import Dict, Any
import pandas as pd

try:
    from IPython.display import display
except Exception:  # pragma: no cover
    def display(x): print(x)

def data_overview(
    df: pd.DataFrame,
    top: int = 15,
    show_numeric_summary: bool = True,
    show_top_missing: bool = True,
    show_top_unique: bool = True,
    show_duplicates: bool = True,
    show_categoricals_preview: bool = True,
    max_cats: int = 8,
    head_rows: int = 3,
) -> Dict[str, Any]:
    """
    One-call early diagnostics for a DataFrame. Displays a compact overview
    and returns key objects (dtypes, numeric_summary, missing_rate, n_unique, …).
    """
    out: Dict[str, Any] = {}

    # 1) basic shape
    print(f"Shape: {df.shape[0]:,} rows × {df.shape[1]:,} columns")

    # 2) preview top rows
    print(f"\nTop {head_rows} rows (quick peek):")
    display(df.head(head_rows))

    # 3) dtypes
    dtypes = df.dtypes.sort_index()
    out["dtypes"] = dtypes
    print("\nDtypes (sorted by column name):")
    display(dtypes)

    # 4) numeric summary
    if show_numeric_summary:
        try:
            # pandas >= 2.0
            num_desc = df.describe(numeric_only=True).T
        except TypeError:
            # older pandas fallback
            num_desc = df.select_dtypes(include="number").describe().T
        out["numeric_summary"] = num_desc
        print("\nNumeric summary (describe):")
        display(num_desc)

    # 5) missingness
    if show_top_missing:
        miss = df.isna().mean().sort_values(ascending=False).rename("missing_rate")
        out["missing_rate"] = miss
        print(f"\nTop {top} missingness:")
        display(miss.head(top))

    # 6) unique counts
    if show_top_unique:
        nunq = df.nunique(dropna=False).sort_values(ascending=False).rename("n_unique")
        out["n_unique"] = nunq
        print(f"\nTop {top} unique counts:")
        display(nunq.head(top))

    # 7) duplicates
    if show_duplicates:
        dup = int(df.duplicated().sum())
        out["duplicate_rows"] = dup
        print(f"\nDuplicated rows: {dup}")

    # 8) categorical preview
    if show_categoricals_preview:
        cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
        out["categorical_columns"] = cat_cols
        if cat_cols:
            preview_cols = cat_cols[:max_cats]
            print(f"\nCategorical preview (top 10 levels) for up to {max_cats} columns:")
            for c in preview_cols:
                vc = df[c].value_counts(dropna=False).head(10)
                print(f"  • {c}")
                display(vc)

    return out
