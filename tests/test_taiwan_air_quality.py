"""Tests for taiwan_air_quality package."""

import pandas as pd

from taiwan_air_quality import hello, transform_data


def test_hello():
    """Test the hello function."""
    result = hello()
    assert result == "Hello from taiwan-air-quality!"


def test_transform_data_function_exists():
    """Test that transform_data function can be imported."""
    # Just test that the function exists and is callable
    assert callable(transform_data)


def test_transform_data_with_sample_data(tmp_path):
    """Test transform_data with a sample CSV file."""
    # Create a sample CSV file
    sample_data = pd.DataFrame(
        {
            "測站": ["測站1", "測站1"],
            "縣市": ["台北市", "台北市"],
            "空管區": ["北部空品區", "北部空品區"],
            "日期": ["2023-01-01", "2023-01-01"],
            "測項": ["PM2.5", "PM10"],
            "00": [25.0, 45.0],
            "01": [23.0, 43.0],
            "02": [22.0, 42.0],
        }
    )

    # Save to temporary CSV file
    csv_file = tmp_path / "test_data.csv"
    sample_data.to_csv(csv_file, index=False, encoding="utf-8-sig")

    # Test the transform_data function
    result = transform_data(csv_file)

    # Check that result is a DataFrame
    assert isinstance(result, pd.DataFrame)

    # Check that the DataFrame has the expected structure
    assert "測站" in result.columns
    assert "縣市" in result.columns
    assert "空管區" in result.columns
    assert "日期" in result.columns

    # Check that the data has been pivoted correctly
    assert len(result) > 0
