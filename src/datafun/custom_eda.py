import logging  # for type hinting only

from datafun_toolkit.logger import get_logger, log_header
import pandas as pd

# === Section 1b. CONFIGURE LOGGER ONCE PER MODULE ===
LOG: logging.Logger = get_logger("P06", level="DEBUG")
log_header(LOG, "P06")


# Data Loader
def load_data(dataset_name: str, dataset_path: str) -> pd.DataFrame:
    """Load a dataset into a DataFrame.

    This function loads a dataset from a excel file located in the
    `data/raw` directory. The dataset name and path are provided as arguments.

    Arguments: None

    Returns:
        pd.DataFrame: The loaded dataset.
    """
    LOG.info(f"Loading dataset: {dataset_name}")
    df: pd.DataFrame = pd.read_excel(f"data/raw/{dataset_path}")
    df.columns = df.columns.str.strip()
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
    # df['Employment'] = df['Employment'].str.replace(r'[()\-]', '', regex=True).astype(int)
    # df = df.dropna(how='any', inplace=True)

    cleaned_shape: tuple[int, int] = df.shape
    LOG.info(
        f"After dropping NA values: {cleaned_shape[0]} rows, {cleaned_shape[1]} columns"
    )


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
    LOG.info("Cleaning data by dropping rows with missing values")

    # "(8) -" means no estimate so drop that row
    # The '~' inverts the boolean mask to keep rows that do NOT match
    df_clean = df[
        ~df.apply(lambda row: row.astype(str).str.contains(r'\(8\) -', regex=True)).any(
            axis=1
        )
    ]
    df_cleaned = df_clean.dropna(how="any")  # Drop rows with any missing values

    # Example of converting a column to numeric if it's not already
    # This is just a placeholder; you would replace 'NumericColumn' with your actual column name
    # LOG.info("Converting 'NumericColumn' to numeric type")
    # df_cleaned['NumericColumn'] = pd.to_numeric(df_cleaned['NumericColumn'], errors='coerce')

    return df_cleaned


# empty main
def main() -> None:
    """Main function to run the EDA workflow."""
    log_header(LOG, "EDA")


if __name__ == "__main__":
    main()
