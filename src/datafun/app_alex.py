import logging  # for type hinting only
from pathlib import Path
from typing import Final  # for type hinting

from datafun_toolkit.logger import get_logger, log_header
from matplotlib.axes import Axes
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from datafun import custom_eda  # for load_dataset() function

# Since you are in root, this creates 'artifacts' directly in the root
OUTPUT_PATH: Path = Path("artifacts")
OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

# Type hint for Axes object (basic plot type returned by Seaborn)
# A seaborn plot is a set of axes. Set title, labels, etc. on the axes.
# A figure can contain multiple axes (plots)
# from matplotlib.figure import Figure

# === Section 1b. CONFIGURE LOGGER ONCE PER MODULE ===

LOG: logging.Logger = get_logger("P06", level="DEBUG")
log_header(LOG, "P06")

# === Section 1c. Global Constants and Configuration ===

# CUSTOM: These are dataset-specific constants
# used in multiple places in the code.
# Inspect or explore the dataset to determine columns needed for analysis.

# CUSTOM: Data set name
DATASET_NAME: Final[str] = "alex_OES_Report"
DATASET_PATH: Final[str] = "alex_OES_Report.xlsx"

# ==========================================================
# ANALYST CHOICE:
# Open the dataset in a spreadsheet or notebook and
# decide which columns to use for grouping and numeric analysis.
# ==========================================================

# CUSTOM: Grouping column (chose one categorical/non-numeric variable)

GROUP_COL: Final[str] = "Area"

# CUSTOM: Numeric columns to analyze (chose 4-5 numeric variables)

SELECTED_NUMERIC_COLS: Final[list[str]] = [
    "Annual mean wage",
    "Annual median wage",
    "Employment",
]

# CUSTOM: Choose one numeric column for a manual statistics example.

EXAMPLE_NUMERIC_COL: Final[str] = "Annual mean wage"

# === Section 1d. Pandas Configuration for Display ===

# Pandas display configuration (helps in notebooks)
pd.set_option("display.max_columns", 50)
pd.set_option("display.width", 120)


def bar_plot_example(df: pd.DataFrame) -> None:
    plt.figure()
    barplot: Axes = sns.barplot(df, x="Occupation", y="Annual median wage", hue="Area")
    barplot.set_title("Median Wage by Occupation and Area")
    barplot.set_xlabel("Occupation")
    barplot.set_ylabel("Annual Median Wage ($)")
    plt.xticks(rotation=90, ha="right")
    plt.tight_layout()
    plt.savefig(OUTPUT_PATH / "bar_plot_example.png")
    plt.figure()
    barplot: Axes = sns.barplot(df, x="Occupation", y="Employment", hue="Area")
    barplot.set_title("Employment by Occupation and Area")
    barplot.set_xlabel("Occupation")
    barplot.set_ylabel("Employment")
    plt.xticks(rotation=90, ha="right")
    plt.tight_layout()
    plt.savefig(OUTPUT_PATH / "bar_plot_jobs_available.png")


def main() -> None:
    """Main function to run the EDA workflow."""
    log_header(LOG, "EDA")
    df: pd.DataFrame = custom_eda.load_data(DATASET_NAME, DATASET_PATH)
    df = custom_eda.clean_data(df)
    custom_eda.inspect_basic(df)

    custom_eda.build_data_dictionary(df)
    bar_plot_example(df)
    plt.show()


if __name__ == "__main__":
    main()
