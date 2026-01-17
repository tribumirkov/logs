"""
Main entry point for the sysadmin log classifier POC.
"""

import json
import os
from src.config import load_config
from src.generator import LogGenerator


def run_data_generation(config: dict):
    """
    Generate synthetic log data based on the configuration.

    Args:
        config (dict): The configuration dictionary.
    """
    print("Starting data generation...")
    data_cfg = config['data']
    gen = LogGenerator(seed=data_cfg['random_seed'])
    dataset = gen.generate_dataset(data_cfg['num_samples'])

    output_path = data_cfg['output_path']
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=2)

    print(f"Generated {len(dataset)} samples and saved to {output_path}")


def main():
    """
    Main function to run the POC pipeline.
    """
    config_path = "config/config.yaml"
    if not os.path.exists(config_path):
        print(f"Error: Config file not found at {config_path}")
        return

    config = load_config(config_path)
    run_data_generation(config)


if __name__ == "__main__":
    main()
