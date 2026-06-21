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

GROUP_COL: Final[str] = "area"

# CUSTOM: Numeric columns to analyze (chose 4-5 numeric variables)

SELECTED_NUMERIC_COLS: Final[list[str]] = [
    "annual mean wage",
    "annual median wage",
    "employment",
    "location quotient",
]

# CUSTOM: Choose one numeric column for a manual statistics example.

EXAMPLE_NUMERIC_COL: Final[str] = "annual mean wage"

# === Section 1d. Pandas Configuration for Display ===

# Pandas display configuration (helps in notebooks)
pd.set_option("display.max_columns", 50)
pd.set_option("display.width", 120)


def correlation_matrix(df_clean: pd.DataFrame) -> pd.DataFrame:
    # Select only numeric columns
    df_clean_numeric_cols: pd.DataFrame = df_clean[SELECTED_NUMERIC_COLS]

    # calculate the correlation matrix using the df corr() method
    correlation_matrix = df_clean_numeric_cols.corr()

    LOG.info("\nCorrelation matrix:")
    LOG.debug(f"\n{correlation_matrix}")

    LOG.info("---------Visualize Correlation Matrix as a Heatmap---------------")

    # Open a fresh blank canvas before a new chart
    plt.figure()

    # Use a heatmap() to visualize correlation matrix
    heatmap: Axes = sns.heatmap(
        correlation_matrix,
        annot=True,  # Set annotations to True to show correlation values
        cmap="coolwarm",  # try viridis, plasma, or other colormaps
        center=0,
    )
    heatmap.set_title("Correlation Matrix Heatmap")

    plt.savefig(OUTPUT_PATH / "correlation_matrix_heatmap.png")
    return correlation_matrix


def bar_plot_example(
    df: pd.DataFrame, x_value: str, y_value: str, compare_by: str, title: str
) -> None:
    plt.figure()
    barplot: Axes = sns.barplot(df, x=x_value, y=y_value, hue=compare_by)
    barplot.set_title(title)
    barplot.set_xlabel(x_value)
    barplot.set_ylabel(y_value)
    plt.xticks(rotation=90, ha="right")
    plt.tight_layout()
    plt.savefig(OUTPUT_PATH / f"{title}.png")
    plt.figure()


def narrow_down_top_occupations(df_clean: pd.DataFrame) -> pd.DataFrame:
    # Let's narrow it down to the top 4 occupations by employment in the area with the highest annual mean wage,
    # then plot a bar chart comparing annual median wage and employment for those top 4 occupations.
    top_area: str = df_clean.groupby(GROUP_COL)[EXAMPLE_NUMERIC_COL].mean().idxmax()
    LOG.info(f"\nArea with highest {EXAMPLE_NUMERIC_COL}: {top_area}")
    df_top_area: pd.DataFrame = df_clean[df_clean[GROUP_COL] == top_area]
    top_occupations: pd.Series = (
        df_top_area.groupby("occupation")["employment"].sum().nlargest(4)
    )
    df_top_occupations: pd.DataFrame = df_top_area[
        df_top_area["occupation"].isin(top_occupations.index)
    ]
    return df_top_occupations


def occupation_focused(df: pd.DataFrame) -> pd.DataFrame:
    # Pick 3 preferred jobs then compare feasibility by area
    LOG.info("Narrowing down to 3 occupations")
    preferred_occupation: list[str] = [
        "Data Scientists (15-2051)",
        "Operations Research Analysts (15-2031)",
        "Computer Occupations, All Other (15-1299)",
    ]
    limited_occupation_df = df.loc[df['occupation'].isin(preferred_occupation)]
    LOG.info(limited_occupation_df)
    return limited_occupation_df


def main() -> None:
    """Main function to run the EDA workflow."""
    log_header(LOG, "EDA")
    df: pd.DataFrame = custom_eda.load_data(DATASET_NAME, DATASET_PATH)
    df_clean = custom_eda.clean_data(df)
    custom_eda.build_data_dictionary(df_clean)
    custom_eda.inspect_basic(df_clean)
    custom_eda.descriptive_stats(
        df_clean, EXAMPLE_NUMERIC_COL, SELECTED_NUMERIC_COLS, GROUP_COL
    )
    correlation_matrix(df_clean)

    # I need to clean the occupation names before plotting
    bar_plot_example(
        df_clean, "occupation", "annual median wage", "area", "Wage_Per_Occupation"
    )
    bar_plot_example(
        df_clean, "occupation", "employment", "area", "Employment_Rates_Per_Occupation"
    )
    df_top_occupations = narrow_down_top_occupations(df_clean)
    bar_plot_example(
        df_top_occupations,
        "employment",
        "annual median wage",
        "occupation",
        "Job_Type_Compared_To_Wage",
    )
    df_pref_occupations = occupation_focused(df_clean)
    bar_plot_example(
        df_pref_occupations,
        "occupation",
        "annual median wage",
        "area",
        "Wage_Per_Preferred_Jobs",
    )
    bar_plot_example(
        df_pref_occupations,
        "occupation",
        "employment",
        "area",
        "Employment_Rates_Preferred_Jobs",
    )
    df_pref_occupations.describe()
    # bar_plot_example(df, "area")
    # plt.show()


if __name__ == "__main__":
    main()
