"""Taiwan Air Quality Observation Data Processing Package."""

from .merge import merge_data
from .transform import process_all_files, transform_data

__version__ = "0.1.0"
__all__ = ["merge_data", "transform_data", "process_all_files"]


def hello() -> str:
    return "Hello from taiwan-air-quality!"
