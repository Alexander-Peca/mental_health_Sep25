"""
mh package — reusable utilities for the Mental Health project.
Provides:
- paths   (PROJECT_ROOT, RAW_DIR, PROC_DIR, etc.)
- io      (read/write helpers)
- viz     (simple plotting)
- stats   (paired t-test + effect size)
"""
from .paths import (
    PROJECT_ROOT, DATA_DIR, RAW_DIR, PROC_DIR,
    EXT_DIR, INT_DIR, RESULTS_DIR, FIGURES_DIR, TABLES_DIR, REPORTS_DIR
)
from .io import (
    read_csv_from_raw, read_excel_from_raw,
    write_csv_to_processed, write_table
)

from .datastructure import data_overview

# viz and stats are typically imported by module name:
#   from mh import viz, stats
