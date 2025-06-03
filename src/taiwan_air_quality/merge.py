import argparse
from pathlib import Path

import pandas as pd
from tqdm import tqdm


def merge_data(data_dir: str = "data", stations_file: str = "monitoring_stations.csv"):
    """
    Merge air quality data files by year.

    Args:
        data_dir: Directory containing yearly data folders
        stations_file: Path to monitoring stations CSV file
    """
    # Load the monitoring stations data
    monitoring_station = pd.read_csv(stations_file)

    # Base directory where the folders for each year are located
    base_dir = Path(data_dir)

    # Process each year's directory and combine all CSV files within it into a single CSV    # Process each year's directory and combine all CSV files within it into a single CSV
    for year_dir in base_dir.iterdir():
        if year_dir.is_dir():  # Check if it is a directory
            # Create a DataFrame to store the combined data for the current year
            combined_data = pd.DataFrame()
            year = year_dir.name

            # Iterate over each CSV file in the directory and append it to the combined DataFrame
            year_data_iter = tqdm(year_dir.glob("*.csv"), desc=f"Processing {year}")
            for csv_file in year_data_iter:
                # Read the CSV file, skip the second row (header=0 is default)
                data = pd.read_csv(csv_file, encoding="big5", skiprows=[1])

                # Strip trailing whitespace from columns names
                data.columns = data.columns.str.strip()

                # Strip trailing whitespace from string data in the DataFrame
                data = data.applymap(lambda x: x.strip() if isinstance(x, str) else x)

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

            # Save the combined data to a CSV file named after the year
            combined_csv_path = f"{data_dir}/{year}.csv"
            combined_data.to_csv(combined_csv_path, index=False, encoding="utf-8-sig")

    # Return the list of created files
    return list(base_dir.glob("*.csv"))


def main():
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
        "--stations-file",
        default="monitoring_stations.csv",
        help="Path to monitoring stations CSV file (default: monitoring_stations.csv)",
    )

    args = parser.parse_args()

    print(f"Merging data from {args.data_dir} using stations file {args.stations_file}")
    created_files = merge_data(args.data_dir, args.stations_file)
    print(f"Created {len(created_files)} merged files:")
    for file in created_files:
        print(f"  - {file}")


if __name__ == "__main__":
    main()
