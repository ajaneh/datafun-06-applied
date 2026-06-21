import logging  # for type hinting only
from typing import Any  # for type hinting

from datafun_toolkit.logger import get_logger, log_header
import numpy as np
import pandas as pd

# === Section 1b. CONFIGURE LOGGER ONCE PER MODULE ===
LOG: logging.Logger = get_logger("P06", level="DEBUG")
log_header(LOG, "P06")


# Data Loader
def load_data(dataset_name: str, dataset_path: str) -> pd.DataFrame:

    LOG.info(f"Loading dataset: {dataset_name}")
    df: pd.DataFrame = pd.read_excel(f"data/raw/{dataset_path}")
    df.columns = df.columns.str.strip()
    count_of_rows: int = df.shape[0]
    count_of_columns: int = df.shape[1]
    LOG.info(f"Loaded: {count_of_rows} rows, {count_of_columns} columns")

    return df


# === Section 3. Inspect Data Shape and Structure ===


def inspect_basic(df: pd.DataFrame) -> None:

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
    # df['Employment'] = df['Employment'].str.replace(r'[()\-]', '', regex=True).astype(int)
    # df = df.dropna(how='any', inplace=True)

    cleaned_shape: tuple[int, int] = df.shape
    LOG.info(
        f"After dropping NA values: {cleaned_shape[0]} rows, {cleaned_shape[1]} columns"
    )


# === Section 4. Create Data Dictionary and Check Data Quality ===


def build_data_dictionary(df: pd.DataFrame) -> pd.DataFrame:

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


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the dataset by handling missing values and converting data types.

    This function performs basic data cleaning steps such as:
    - Dropping rows with missing values (if any)
    - Converting numeric columns to appropriate data types

    Arguments:
        df: The DataFrame to clean.

    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    initial_shape: tuple[int, int] = df.shape
    LOG.info(
        f"Initial dataset shape: {initial_shape[0]} rows, {initial_shape[1]} columns"
    )
    LOG.info("Cleaning data by dropping rows with missing values")
    # Log the initial column names before cleaning
    LOG.info("Initial column names:")
    for col in df.columns:
        LOG.info(f"  - {col}")
    # First let's clean the headers so there's no leading/trailing whitespace
    df.columns = df.columns.str.strip().str.lower()
    LOG.info("Stripped whitespace from column names, new column names:")
    for col in df.columns:
        LOG.info(f"  - {col}")
    # "(8) -" means no estimate so drop that row
    # The '~' inverts the boolean mask to keep rows that do NOT match
    df_clean = df[
        ~df.apply(lambda row: row.astype(str).str.contains(r'\(8\) -', regex=True)).any(
            axis=1
        )
    ]
    df_cleaned = df_clean.dropna(how="any")  # Drop rows with any missing values
    cleaned_shape: tuple[int, int] = df_cleaned.shape
    # Cast employment, and location quotient to numeric, removing any non-numeric characters
    df_cleaned['employment'] = df_cleaned['employment'].astype(int)
    df_cleaned['location quotient'] = df_cleaned['location quotient'].astype(float)
    LOG.info(f"After cleaning: {cleaned_shape[0]} rows, {cleaned_shape[1]} columns")
    # Log the difference
    dropped_rows: int = initial_shape[0] - cleaned_shape[0]
    LOG.info(f"Dropped {dropped_rows} rows due to missing values or '(8) -' entries")
    # Example of converting a column to numeric if it's not already
    # This is just a placeholder; you would replace 'NumericColumn' with your actual column name
    # LOG.info("Converting 'NumericColumn' to numeric type")
    # df_cleaned['NumericColumn'] = pd.to_numeric(df_cleaned['NumericColumn'], errors='coerce')

    return df_cleaned


def descriptive_stats(
    df_clean: pd.DataFrame,
    example_numeric_col: str,
    selected_numeric_cols: list[str],
    group_col: str,
) -> tuple[pd.DataFrame, pd.DataFrame]:

    LOG.info("--------------- Manual statistics ---------------")

    # Example: Calculate statistics for a specific column with numpy

    example_values = df_clean[example_numeric_col]

    # Use general variable names so the function can be reused.

    mean_value = np.mean(example_values)
    std_value = np.std(example_values)
    min_value = np.min(example_values)
    max_value = np.max(example_values)
    range_value = np.ptp(
        example_values
    )  # ptp is "peak to peak" = max - min, a measure of spread

    # Log the example results with formatting
    LOG.debug(f"{example_numeric_col} Statistics (using numpy):")
    LOG.debug(f"  Mean: {mean_value:.2f}")
    LOG.debug(f"  Std Dev: {std_value:.2f}")
    LOG.debug(f"  Min: {min_value:.2f}")
    LOG.debug(f"  Max: {max_value:.2f}")
    LOG.debug(f"  Range: {range_value:.2f}")

    LOG.info("--------------- Using pandas describe() method ---------------")

    LOG.info("Computing overall descriptive statistics")

    # Use describe() to get count, mean, std, min, 25%, 50%, 75%, max for numeric columns
    # OPTION: Use .T to transpose the result so that columns become rows for easier reading in logs
    stats_overall = df_clean[selected_numeric_cols].describe().T
    LOG.debug(f"\n{stats_overall}")

    LOG.info("--------------- Using pandas groupby() and agg() ---------------")

    LOG.info("Computing descriptive statistics by group")

    # Step 1: Select only the numeric columns we want to summarize
    df_numeric_subset: pd.DataFrame = df_clean[selected_numeric_cols]

    # Step 2: Split the numeric subset into groups based on the grouping column
    # groupby() returns a GroupBy object - not a DataFrame yet, just a plan to group
    grouped = df_numeric_subset.groupby(df_clean[group_col])

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


# empty main
def main() -> None:
    """Main function to run the EDA workflow."""
    log_header(LOG, "EDA")


if __name__ == "__main__":
    main()
