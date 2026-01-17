"""
Configuration loader module.

This module is responsible for loading and validating the configuration
from the YAML file.
"""

import yaml


def load_config(config_path: str) -> dict:
    """
    Load the configuration from the specified YAML file.

    Args:
        config_path (str): The path to the configuration file.

    Returns:
        dict: The configuration dictionary.

    Raises:
        FileNotFoundError: If the config file does not exist.
        yaml.YAMLError: If the config file is not valid YAML.
    """
    with open(config_path, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
    return config
