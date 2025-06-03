# Taiwan Air Quality Observation Data

A Python package for processing and analyzing Taiwan air quality observation data. This package provides tools to merge, transform, and analyze air quality data from Taiwan's monitoring stations.

## Features

- **Data Merging**: Combine air quality data files by year from multiple monitoring stations
- **Data Transformation**: Convert wide-format data to long-format for analysis
- **CLI Tools**: Command-line interfaces for batch processing
- **Type Hints**: Full type hint support for better development experience
- **Modern Python**: Built with modern Python practices using `uv` for dependency management

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for dependency management. First, install uv if you haven't already:

```bash
# On Windows (PowerShell)
Invoke-WebRequest -Uri https://install.uv.io/install.ps1 -OutFile install.ps1; ./install.ps1

# On macOS/Linux
curl -LsSf https://install.uv.io/install.sh | sh
```

Then clone and install the project:

```bash
git clone https://github.com/whats2000/TaiwanAirQualityObservationData.git
cd TaiwanAirQualityObservationData
uv sync
```

## Usage

### Command Line Interface

The package provides two main CLI commands:

#### Merge Data
Merge air quality data files by year:

```bash
# Merge all data in the 'data' directory and output to 'output' directory
uv run merge-data

# Specify custom data directory and stations file
uv run merge-data --data-dir /path/to/data --output-dir /path/to/output --stations-file custom_stations.csv
```

#### Transform Data
Transform data from wide format to long format:

```bash
# Transform all CSV files in the 'data' directory
uv run transform-data

# Transform a specific file
uv run transform-data --file data/2023.csv

# Specify custom data directory
uv run transform-data --data-dir /path/to/data
```

### Python API

You can also use the package programmatically:

```python
from taiwan_air_quality import merge_data, transform_data, process_all_files

# Merge data
merge_data(data_dir='data', stations_file='monitoring_stations.csv')

# Transform a specific file
transformed_df = transform_data('data/2023.csv')

# Transform all files in a directory
process_all_files('data')
```

## Data Structure

### Input Data Format
The package expects air quality data in the following structure:
- Raw data organized in yearly directories under `data/`
- Each year directory contains CSV files from monitoring stations
- Monitoring stations metadata in `monitoring_stations.csv`

### Output Data Format
- **Merged Data**: Combined yearly CSV files with standardized columns
- **Transformed Data**: Long-format data with datetime columns for time-series analysis

## Development

### Setting up the Development Environment

```bash
# Clone the repository
git clone https://github.com/whats2000/TaiwanAirQualityObservationData.git
cd TaiwanAirQualityObservationData

# Install with development dependencies
uv sync --extra dev

# Install additional data science tools
uv sync --extra data
```

### Running Tests

```bash
uv run pytest
```

### Code Formatting

The project uses several tools for code quality:

```bash
# Format code with Black
uv run black src/ tests/

# Sort imports with isort
uv run isort src/ tests/

# Lint with flake8
uv run flake8 src/ tests/

# Type checking with mypy
uv run mypy src/
```

## Project Structure

```
TaiwanAirQualityObservationData/
├── src/
│   └── taiwan_air_quality/
│       ├── __init__.py          # Package initialization
│       ├── merge.py             # Data merging functionality
│       ├── transform.py         # Data transformation functionality
│       └── py.typed             # Type hint marker
├── tests/
│   ├── __init__.py
│   └── test_taiwan_air_quality.py
├── data/                        # Data directory (not in repo)
├── monitoring_stations.csv      # Station metadata
├── pyproject.toml              # Project configuration
├── uv.lock                     # Dependency lock file
├── README.md                   # This file
└── .gitignore                  # Git ignore rules
```

## Dependencies

### Core Dependencies
- **pandas**: Data manipulation and analysis
- **tqdm**: Progress bars for long-running operations

### Development Dependencies
- **pytest**: Testing framework
- **black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking

### Optional Dependencies (data)
- **matplotlib**: Plotting and visualization
- **seaborn**: Statistical data visualization
- **jupyter**: Interactive notebooks
- **plotly**: Interactive plots
- **numpy**: Numerical computing

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and ensure code quality (`uv run pytest && uv run black . && uv run flake8`)
5. Commit your changes (`git commit -m 'Add some amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Taiwan Environmental Protection Administration for providing air quality data
- The Python community for excellent tools and libraries
- Contributors to this project
