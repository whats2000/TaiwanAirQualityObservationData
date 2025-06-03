import argparse
from pathlib import Path
from typing import List

import pandas as pd
from tqdm import tqdm


def merge_data(
    data_dir: str = "data",
    output_dir: str = "output",
    stations_file: str = "mapping_data/monitoring_stations.csv"
) -> List[str]:
    """
    Merge air quality data files by year.

    Args:
        data_dir: Directory containing yearly data folders
        output_dir: Directory to write merged data to
        stations_file: Path to monitoring stations CSV file
        
    Returns:
        List of created output file paths
    """
    # Load the monitoring stations data
    monitoring_station = pd.read_csv(stations_file)

    # Base directory where the folders for each year are located
    base_dir = Path(data_dir)

    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    created_files = []

    # Process each year's directory and combine all CSV files within it into a single DataFrame
    for year_dir in base_dir.iterdir():
        if not year_dir.is_dir():
            continue

        year = year_dir.name
        combined_data = pd.DataFrame()

        # 1. Collect all CSV paths into a list so tqdm can determine total length
        csv_files = list(year_dir.glob("*.csv"))

        # 2. Wrap the list in tqdm to display a proper progress bar
        for csv_file in tqdm(csv_files, desc=f"Processing {year}", unit="file"):
            try:
                # Read the CSV file, skip the second row (header=0 is default)
                data = pd.read_csv(csv_file, encoding="utf-8", skiprows=[1])

                # Strip trailing whitespace from column names
                data.columns = data.columns.str.strip()

                # Strip trailing whitespace from string data in the DataFrame
                data = data.map(lambda x: x.strip() if isinstance(x, str) else x)

                # Map the '測站' column to '空管區' using the monitoring_station DataFrame
                data = data.merge(
                    monitoring_station,
                    how="left",
                    left_on="測站",
                    right_on="監測站名稱",
                    validate="many_to_one",
                )

                # Drop the '監測站名稱' column as it is a duplicate of '測站'
                data.drop("監測站名稱", axis=1, inplace=True)

                # Adjust the order of columns as specified
                columns_order = ["測站", "縣市", "空管區", "日期", "測項"] + [
                    str(i).zfill(2) for i in range(24)
                ]
                data = data[columns_order]

                # Append the data to the combined DataFrame
                combined_data = pd.concat([combined_data, data], ignore_index=True)

            except Exception as e:
                # Use tqdm.write so the progress bar formatting isn’t disrupted
                tqdm.write(f"Error processing file {csv_file}: {e}")
                continue

        # Save the combined data to a CSV file named after the year
        if not combined_data.empty:
            combined_csv_path = output_path / f"{year}.csv"
            combined_data.to_csv(combined_csv_path, index=False, encoding="utf-8-sig")
            created_files.append(str(combined_csv_path))
            print(f"Created {combined_csv_path} with {len(combined_data)} rows")

    # Return the list of created files
    return created_files


def main() -> None:
    """CLI entry point for merging data."""
    parser = argparse.ArgumentParser(
        description="Merge Taiwan air quality data by year"
    )
    parser.add_argument(
        "--data-dir",
        default="data",
        help="Directory containing yearly data folders (default: data)",
    )
    parser.add_argument(
        "--output-dir",
        default="output",
        help="Directory to output merged data (default: output)",
    )
    parser.add_argument(
        "--stations-file",
        default="mapping_data/monitoring_stations.csv",
        help="Path to monitoring stations CSV file (default: monitoring_stations.csv)",
    )

    args = parser.parse_args()

    print(f"Merging data from {args.data_dir} using stations file {args.stations_file}")
    created_files = merge_data(args.data_dir, args.output_dir, args.stations_file)
    print(f"Created {len(created_files)} merged files:")
    for file in created_files:
        print(f"  - {file}")


if __name__ == "__main__":
    main()
