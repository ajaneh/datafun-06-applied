"""app_case.py - Project script (example).

Author: Denise Case
Date: 2026-06

Purpose:
    - exploratory data analysis (EDA)
    - loading a CSV dataset
    - inspecting a DataFrame with pandas
    - checking for missing values
    - computing descriptive statistics
    - grouping and aggregating
    - computing a correlation matrix
    - creating charts with seaborn and matplotlib

Data Source:
- data/raw/owid-co2-data-subset.csv (from Our World in Data)

Assumptions:
- The data contains columns like:
  country, year, co2, co2_per_capita, population, gdp

Terminal command to run this file from the root project folder:

uv run python -m datafun.app_case

OBS:
  Don't edit this file - it should remain a working example.
  Copy it, rename it, and modify your copy.
"""


# === Section 1a. DECLARE IMPORTS (BRING IN FREE CODE) ===

import logging  # for type hinting only
from typing import Any, Final  # for type hinting

from datafun_toolkit.logger import get_logger, log_header
from matplotlib.axes import Axes
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

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
DATASET_NAME: Final[str] = "owid-co2-data-subset"

# ==========================================================
# ANALYST CHOICE:
# Open the dataset in a spreadsheet or notebook and
# decide which columns to use for grouping and numeric analysis.
# ==========================================================

# CUSTOM: Grouping column (chose one categorical/non-numeric variable)

GROUP_COL: Final[str] = "country"

# CUSTOM: Numeric columns to analyze (chose 4-5 numeric variables)

SELECTED_NUMERIC_COLS: Final[list[str]] = [
    "year",
    "co2",
    "co2_per_capita",
    "population",
    "gdp",
]

# CUSTOM: Choose one numeric column for a manual statistics example.

EXAMPLE_NUMERIC_COL: Final[str] = "co2_per_capita"

# CUSTOM: Choose a few numeric columns to check for correlations and plot.
# Look for strong correlations in the descriptive stats section to guide this choice.
# For example, if co2_per_capita and gdp show strong correlation, plot those

SCATTER_X_COL: Final[str] = "gdp"
SCATTER_Y_COL: Final[str] = "co2"

BOX_Y_COL: Final[str] = "co2_per_capita"

# CUSTOM: Assign readable labels for the charted variables.

SCATTER_X_LABEL: Final[str] = "GDP"
SCATTER_Y_LABEL: Final[str] = "CO2 emissions"

BOX_Y_LABEL: Final[str] = "CO2 per capita"

# === Section 1d. Pandas Configuration for Display ===

# Pandas display configuration (helps in notebooks)
pd.set_option("display.max_columns", 50)
pd.set_option("display.width", 120)


# === Section 2. Load the Data ===


def load_data() -> pd.DataFrame:
    """Load a dataset into a DataFrame.

    This function loads a dataset from a CSV file located in the
    `data/raw` directory. The dataset name is specified by the
    `DATASET_NAME` constant.

    Arguments: None

    Returns:
        pd.DataFrame: The loaded dataset.
    """
    LOG.info(f"Loading dataset: {DATASET_NAME}")
    df: pd.DataFrame = pd.read_csv(f"data/raw/{DATASET_NAME}.csv")
    count_of_rows: int = df.shape[0]
    count_of_columns: int = df.shape[1]
    LOG.info(f"Loaded: {count_of_rows} rows, {count_of_columns} columns")

    return df


# === Section 3. Inspect Data Shape and Structure ===


def inspect_basic(df: pd.DataFrame) -> None:
    """Inspect the basic structure of the dataset.

    WHY: Always start by understanding what columns exist,
    what types they are, and how large the dataset is.

    - How many rows and columns are there?
    - What types of data are present?
    - Are there obvious missing values?

    This step determines challenges we might have downstream (later).

    Arguments:
        df: The DataFrame to inspect.

    Returns:
        None
    """
    # Preview the first few rows
    LOG.info("Previewing first few rows of the dataset")
    LOG.debug(f"\n{df.head()}")

    LOG.info("Column names")
    column_names: list[str] = list(df.columns)
    LOG.debug(f"{column_names}")

    LOG.info("DataFrame info (types and non-null counts)")
    df.info()

    # Get shape - number of rows and columns
    # It has two parts so the return value is a tuple of (num_rows, num_columns)
    shape: tuple[int, int] = df.shape

    # To get each value, we can unpack the tuple into two variables
    # This is a common Python idiom for working with tuples.
    # Or we could just use shape[0] and shape[1] directly without unpacking.

    num_rows, num_cols = shape

    LOG.info(f"Dataset shape: {num_rows} rows, {num_cols} columns")


# === Section 4. Create Data Dictionary and Check Data Quality ===


def build_data_dictionary(df: pd.DataFrame) -> pd.DataFrame:
    """Build a starter data dictionary.

    Includes:
    - column name
    - data type
    - missing value count
    - percent missing

    WHY: A data dictionary helps with understanding the structure and quality of the data.

    Arguments:
    - df: The DataFrame to analyze.

    Returns:
    - pd.DataFrame: A data dictionary summarizing the columns.
    """
    LOG.info("Building starter data dictionary")

    data_dictionary = pd.DataFrame(
        {
            "column": df.columns,
            "dtype": [str(t) for t in df.dtypes],
            "missing_count": df.isna().sum().values,
            "missing_pct": (df.isna().mean() * 100).round(2).values,
        }
    )

    LOG.debug(f"\n{data_dictionary}")
    return data_dictionary


def check_quality(df: pd.DataFrame) -> None:
    """Perform basic data quality checks.

    Checks include:
    - Missing values
    - Duplicate rows
    - Basic numeric sanity checks

    WHY: Data quality issues can affect analysis results.
    It's important to identify them early in the EDA process.
    Arguments:
    - df: The DataFrame to check.
    Returns:
    - None (logs results)
    """
    LOG.info("Missing values per column:")
    LOG.info(f"\n{df.isnull().sum()}")

    LOG.info("Checking missing values per column")
    LOG.debug(f"\n{df.isna().sum().sort_values(ascending=False)}")

    dup_count = int(df.duplicated().sum())
    LOG.info(f"Duplicate rows detected: {dup_count}")

    LOG.info("Call describe() for numeric columns")
    LOG.debug(f"\n{df[SELECTED_NUMERIC_COLS].describe()}\n")


# === Section 5. Create Clean View for EDA ===


def make_clean_view(df: pd.DataFrame) -> pd.DataFrame:
    """Create a cleaned view for EDA.

    Strategy:
    - Keep the original DataFrame unchanged
    - Drop rows missing key numeric fields and grouping field

    WHY: EDA often focuses on a "clean" subset of the data.
    This allows exploring patterns without being distracted by missing values.

    Arguments:
    - df: The original DataFrame.

    Returns:
    - pd.DataFrame: A cleaned view of the data for EDA.
    """
    LOG.info("Creating cleaned view for EDA (dropping rows with key missing values)")

    # Build the list of columns we require to be non-missing
    # This includes all the selected numeric columns plus the grouping column.
    # SELECTED_NUMERIC_COLS is a list of strings,
    # GROUP_COL is a single string
    # Wrap GROUP_COL in a list - two lists can be combined with +
    cols_required: list[str] = SELECTED_NUMERIC_COLS + [GROUP_COL]
    LOG.debug(f"Columns required to be non-missing: {cols_required}")

    # Drop a row if it is missing a value in ANY of the required columns
    # Use the dropna() method with subset= to specify which columns to check for missing values.
    # Dropna means "drop rows if not available (na) that is, they have missing values". By default, it checks all columns, but we only want to check the key columns.
    # dropna(subset=...) only looks at the specified columns, not the whole row
    # .copy() creates a new DataFrame so we don't accidentally modify the original
    df_clean: pd.DataFrame = df.dropna(subset=cols_required).copy()

    # Report what was kept and what was dropped
    count_original: int = df.shape[0]
    count_clean: int = df_clean.shape[0]
    count_dropped: int = count_original - count_clean

    LOG.info(f"Original rows: {count_original}")
    LOG.info(f"Clean rows:    {count_clean}")
    LOG.info(f"Rows dropped:  {count_dropped}")

    return df_clean


# === Section 6. Descriptive Statistics for Numeric Columns ===


def descriptive_stats(df_clean: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Compute descriptive statistics overall and by group.

    WHY: Summary statistics offer a quick overview of numeric data:

    - Central tendency (mean)
    - Spread (std, min, max)
    - Distribution shape (quartiles)

    Grouping by a categorical variable (i.e., non-numeric column)
    enables comparing statistics across categories

    Args:
        df_clean (pd.DataFrame): Cleaned DataFrame for analysis.

    Returns:
        tuple[pd.DataFrame, pd.DataFrame]: Overall stats, stats by group.

    Notes:
    - Descriptive statistics summarize key aspects of numeric data.
    - Grouped stats help compare across categories.
    """

    LOG.info("--------------- Manual statistics ---------------")

    # Example: Calculate statistics for a specific column with numpy

    example_values = df_clean[EXAMPLE_NUMERIC_COL]

    # Use general variable names so the function can be reused.

    mean_value = np.mean(example_values)
    std_value = np.std(example_values)
    min_value = np.min(example_values)
    max_value = np.max(example_values)
    range_value = np.ptp(
        example_values
    )  # ptp is "peak to peak" = max - min, a measure of spread

    # Log the example results with formatting
    LOG.debug(f"{EXAMPLE_NUMERIC_COL} Statistics (using numpy):")
    LOG.debug(f"  Mean: {mean_value:.2f}")
    LOG.debug(f"  Std Dev: {std_value:.2f}")
    LOG.debug(f"  Min: {min_value:.2f}")
    LOG.debug(f"  Max: {max_value:.2f}")
    LOG.debug(f"  Range: {range_value:.2f}")

    LOG.info("--------------- Using pandas describe() method ---------------")

    LOG.info("Computing overall descriptive statistics")

    # Use describe() to get count, mean, std, min, 25%, 50%, 75%, max for numeric columns
    # OPTION: Use .T to transpose the result so that columns become rows for easier reading in logs
    stats_overall = df_clean[SELECTED_NUMERIC_COLS].describe().T
    LOG.debug(f"\n{stats_overall}")

    LOG.info("--------------- Using pandas groupby() and agg() ---------------")

    LOG.info("Computing descriptive statistics by group")

    # Step 1: Select only the numeric columns we want to summarize
    df_numeric_subset: pd.DataFrame = df_clean[SELECTED_NUMERIC_COLS]

    # Step 2: Split the numeric subset into groups based on the grouping column
    # groupby() returns a GroupBy object - not a DataFrame yet, just a plan to group
    grouped = df_numeric_subset.groupby(df_clean[GROUP_COL])

    # Step 3: For each group, compute multiple summary statistics at once
    # agg() applies each function in the list to each numeric column
    # The result has a multi-level column index: (numeric_column, statistic)
    df_stats_by_group: pd.DataFrame = grouped.agg(
        ["count", "mean", "std", "min", "max"]
    )

    LOG.debug(f"\n{df_stats_by_group}")

    LOG.info("\nStacked view - easier to read in logs:")

    # Yuck: That's the multi-level column index in action.
    # pandas lays out the result as (numeric_column, statistic) pairs
    # side by side, wrapping when the terminal width runs out.
    # With 4 numeric columns × 5 statistics = 20 columns total,
    # it can only fit 2 numeric columns per line at 120 characters wide.
    # Let's stack it so each numeric column's stats are grouped together
    # vertically instead of horizontally.

    stats_by_group_stacked: pd.DataFrame | pd.Series[Any] = df_stats_by_group.stack(
        level=0
    )
    LOG.debug(f"\n{stats_by_group_stacked}")

    return stats_overall, df_stats_by_group


# === Section 7. Simple Correlations (Numeric Only) ===


def correlation_matrix(df_clean: pd.DataFrame) -> pd.DataFrame:
    """Compute a simple numeric correlations to understand
    relationships between numeric variables.

    A correlation matrix is symmetric.
    There are as many columns as numeric variables.
    There are as many rows as numeric variables.
    The diagonal values are always exactly 1.0.
    since each variable perfectly correlates with itself.

    WHY: Correlation tells us how numeric variables relate to each other.

    - Values near 1 or -1 indicate strong relationships
    - Values near 0 indicate weak or no linear relationship

    Args:
        df_clean (pd.DataFrame): Cleaned DataFrame for analysis.

    Returns:
        pd.DataFrame: Correlation matrix of numeric columns.
    """
    LOG.info("Computing correlation matrix for numeric columns")

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
    # IN NOTEBOOK: SHOW AS YOU GO
    #      plt.show() displays the current chart and closes it
    #      Call this before starting a new chart
    #      or next chart will be drawn on top of this one
    # IN SCRIPT: WAIT TO SHOW TILL THE END
    #      Do not call plt.show() here - let figures accumulate
    #      so all charts display together with sequential Figure numbers.
    #      plt.show() is called once at the end of make_plots()
    # plt.show()

    LOG.info("""
CUSTOM: Update these notes and use Markdown cells to narrate and tell the story as you explore. For example:

Interpretation:

 - Values close to 1 (dark red) = strong positive correlation (both increase together)
 - Values close to -1 (dark blue) = strong negative correlation (one increases, other decreases)
 - Values close to 0 (white) = little or no linear relationship
 - The diagonal is always 1 (each variable correlates perfectly with itself)

From this heatmap, we can see that flipper_length_mm and body_mass_g show strong positive correlation (~0.87).
""")

    return correlation_matrix


# === Section 8. Create Visualizations ===


def make_plots(df_clean: pd.DataFrame) -> None:
    """Create simple, notebook-friendly plots.

    Arguments:
        df_clean: Cleaned DataFrame for analysis.

    Returns:
        None

    WHY: Visualizations reveal patterns not obvious in tables.
    CUSTOM: Charts will vary depending on the dataset
            and questions of interest.

    Common charts include:
    1. A scatter plot to see relationships between two variables
    2. A box plot to compare distributions across groups

    A scatter plot shows the relationship between two numeric variables.
    In this example:
    - Each dot is one data record shown as x vs y.
    - Color (hue) provides a third dimension.

    A box plot shows the distribution of one numeric variable across groups.
    - The box shows the middle 50% of values.
    - The line inside the box is the median.
    - The whiskers show the range. Dots beyond the whiskers are outliers.

    """
    LOG.info("---- Creating Scatter Plot to see Relationships ------")
    LOG.info("----   Use clean dataframe ---------------------------")
    LOG.info(f"----   Set x to {SCATTER_X_LABEL} -----------------------")
    LOG.info(f"----   Set y to {SCATTER_Y_LABEL} --------------------------")
    LOG.info("----   Set the hue (color mapping) to the group column --")

    # Open a fresh blank canvas before a new chart
    plt.figure()

    # Use a scatterplot() to visualize relationships between two variables (x vs y)

    # Use the prior analysis to choose which numeric variables to plot.
    # Look for strong correlations or interesting patterns.

    scatter_plt: Axes = sns.scatterplot(
        data=df_clean,
        x=SCATTER_X_COL,
        y=SCATTER_Y_COL,
        hue=GROUP_COL,
    )
    # Set axis labels using the Matplotlib Axes methods set_xlabel() and set_ylabel()
    scatter_plt.set_xlabel(SCATTER_X_LABEL)
    scatter_plt.set_ylabel(SCATTER_Y_LABEL)

    # Set the title using the Matplotlib Axes set_title() method
    scatter_plt.set_title(f"{SCATTER_X_LABEL} vs {SCATTER_Y_LABEL} (by {GROUP_COL})")

    # IN NOTEBOOK: SHOW AS YOU GO
    #      plt.show() displays the current chart and closes it
    #      Call this before starting a new chart
    #      or next chart will be drawn on top of this one
    # IN SCRIPT: WAIT TO SHOW TILL THE END
    #      Do not call plt.show() here - let figures accumulate
    #      so all charts display together with sequential Figure numbers.
    #      plt.show() is called once at the end of make_plots()
    # plt.show()

    LOG.info("------ Creating Box Plot to see Distribution: ---------")
    LOG.info("------   Use clean dataframe --------------------------")
    LOG.info("------   Set x to the group column --------------------")
    LOG.info(f"------   Set y to {BOX_Y_LABEL} ----------------------")

    # Open a fresh blank canvas before a new chart
    plt.figure()

    # Use a boxplot() to visualize the distribution of a numeric variable across groups
    box_plt: Axes = sns.boxplot(
        data=df_clean,
        x=GROUP_COL,
        y=BOX_Y_COL,
    )
    # Set readable labels and title for the box plot
    box_plt.set_xlabel(GROUP_COL)
    box_plt.set_ylabel(BOX_Y_LABEL)
    box_plt.set_title(f"{BOX_Y_LABEL} by {GROUP_COL}")

    # Rotate the x-axis labels if there are many groups or long names
    box_plt.tick_params(axis="x", labelrotation=45)

    # IN NOTEBOOK: SHOW AS YOU GO
    #      plt.show() displays the current chart and closes it
    #      Call this before starting a new chart
    #      or next chart will be drawn on top of this one
    # IN SCRIPT: WAIT TO SHOW TILL THE END
    #      Do not call plt.show() here - let figures accumulate
    #      so all charts display together with sequential Figure numbers.
    #      plt.show() is called once at the end of make_plots()
    # plt.show()


# === Section 9. Summary and Next Steps ===


def summarize(df: pd.DataFrame, df_clean: pd.DataFrame) -> None:
    """Log a brief summary of findings and suggested next steps.

    WHY: EDA is not the final report.
    A summary captures what was found and what to investigate next.

    Arguments:
        df: The original DataFrame.
        df_clean: The cleaned DataFrame.

    Returns:
        None
    """
    LOG.info("========================")
    LOG.info("SUMMARY")
    LOG.info("========================")
    LOG.info(f"Dataset: {DATASET_NAME}")

    LOG.info(f"Original rows: {df.shape[0]}")
    LOG.info(f"Clean rows:    {df_clean.shape[0]}")

    # Get the unique values in the grouping column (e.g. species names)
    unique_groups_array: np.ndarray = df_clean[GROUP_COL].unique()

    # Sort them alphabetically so the output is consistent and readable
    sorted_groups: list[str] = sorted(unique_groups_array)

    LOG.info(f"Groups found in {GROUP_COL}: {sorted_groups}")

    LOG.info("======================")
    LOG.info("Review the results. ")
    LOG.info("Determine the strongest correlations. ")
    LOG.info("======================")
    LOG.info("Look for interesting patterns in the charts. ")
    LOG.info("Repeat the process, exploring additional angles.")
    LOG.info("After finding interesting insights, conclude your analysis.")
    LOG.info("======================")
    LOG.info("Include instructions and specifics in your README.md file.")
    LOG.info("Write up your narrative on your docs/index.md file.")
    LOG.info("Include your next step suggestions for further analysis or modeling.")
    LOG.info("======================")


# === DEFINE THE MAIN FUNCTION THAT CALLS OTHER FUNCTIONS ===


def main() -> None:
    """Main function to run the EDA workflow."""
    log_header(LOG, "EDA")

    LOG.info("========================")
    LOG.info("START main()")
    LOG.info("========================")

    LOG.info(f"--- Section 2: Load dataset: {DATASET_NAME} ---")
    df = load_data()

    LOG.info("--- Section 3: Inspect shape and basic structure ---")
    inspect_basic(df)

    LOG.info("--- Section 4: Create Data Dictionary and Check Data Quality ---")
    build_data_dictionary(df)
    check_quality(df)

    LOG.info("--- Section 5: Create a cleaned view for EDA ---")
    df_clean = make_clean_view(df)

    LOG.info("--- Section 6: Descriptive statistics for numeric columns ---")
    descriptive_stats(df_clean)

    LOG.info("--- Section 7: Correlation matrix for numeric columns ---")
    correlation_matrix(df_clean)

    LOG.info("--- Section 8: Charts ---")
    make_plots(df_clean)

    LOG.info("--- Section 9: Summary and next steps ---")
    summarize(df, df_clean)

    LOG.info(
        "----- in a script, call plt.show() once at the end to display all charts -----"
    )
    LOG.info(
        "----- in a script, close the chart windows (with the close button) to continue  -----"
    )
    plt.show()

    LOG.info("EDA workflow complete")
    LOG.info("IMPORTANT: This script creates chart windows.")
    LOG.info(
        "Close any chart windows and terminate this process with CTRL+c as needed."
    )
    LOG.info("========================")
    LOG.info("Executed successfully!")
    LOG.info("========================")


# === CONDITIONAL EXECUTION GUARD ===

# WHY: Only call main() when running this file directly as a script.
# This is standard Python boilerplate.

if __name__ == "__main__":
    main()
