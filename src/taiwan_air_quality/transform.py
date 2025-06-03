import argparse
from pathlib import Path

import pandas as pd
from tqdm import tqdm


# Function to pivot the table and combine date and time into datetime
def transform_data(data_file_path):
    """
    Transform the data in the CSV file to a long format and combine date and time into a datetime column
    Args:
        data_file_path: Path to the CSV file containing the data
    Returns:
        A DataFrame containing the transformed data
    """
    # Read the data
    data = pd.read_csv(data_file_path, encoding="utf-8-sig")

    # Convert date to datetime and combine with hour to create a datetime column
    data["日期"] = pd.to_datetime(data["日期"])

    # Melting the dataframe to make it long format
    data_long = pd.melt(
        data,
        id_vars=["測站", "縣市", "空管區", "日期", "測項"],
        var_name="小時",
        value_name="測量值",
    )

    # Convert hours to time deltas and add to date
    data_long["小時"] = pd.to_timedelta(data_long["小時"] + ":00:00")
    data_long["日期"] = data_long["日期"] + data_long["小時"]

    # Drop the hour column and pivot table
    data_long.drop("小時", axis=1, inplace=True)
    data_pivot = data_long.pivot_table(
        index=["測站", "縣市", "空管區", "日期"],
        columns="測項",
        values="測量值",
        aggfunc="first",
    )

    # Reset index to make sure '測站', '縣市', '空管區', '日期' are columns and not index
    data_pivot.reset_index(inplace=True)

    return data_pivot


def process_all_files(data_dir: str = "data"):
    """
    Transform all CSV files in the specified directory.

    Args:
        data_dir: Directory containing CSV files to transform
    """
    # Directory containing the yearly CSV files
    base_dir = Path(data_dir)

    # Find all the CSV files for the years 2018-2022
    csv_files = base_dir.glob("*.csv")

    iter_files = tqdm(csv_files, desc="Processing files")

    # Process and transform all CSV files
    for file_path in iter_files:
        transformed_data = transform_data(file_path)

        # Save the transformed data back to CSV
        transformed_data.to_csv(file_path, index=False, encoding="utf-8-sig")

    print(f"Transformation completed for all files in {data_dir}")


def main():
    """CLI entry point for transforming data."""
    parser = argparse.ArgumentParser(
        description="Transform Taiwan air quality data to long format"
    )
    parser.add_argument(
        "--data-dir",
        default="output",
        help="Directory containing CSV files to transform (default: output)",
    )
    parser.add_argument(
        "--file",
        type=str,
        help="Transform a specific file instead of all files in directory",
    )

    args = parser.parse_args()

    if args.file:
        print(f"Transforming single file: {args.file}")
        transformed_data = transform_data(args.file)
        transformed_data.to_csv(args.file, index=False, encoding="utf-8-sig")
        print(f"Transformation completed for {args.file}")
    else:
        print(f"Transforming all files in {args.data_dir}")
        process_all_files(args.data_dir)


if __name__ == "__main__":
    main()
