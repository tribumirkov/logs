"""
Main entry point for the sysadmin log classifier POC.
"""

import json
import os
from src.config import load_config
from src.generator import LogGenerator
from src.embedder import Embedder
from src.trainer import Trainer


def run_data_generation(config: dict) -> str:
    """
    Generate synthetic log data based on the configuration.

    Args:
        config (dict): The configuration dictionary.

    Returns:
        str: The path to the generated JSON file.
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
    return output_path


def run_embedding_generation(config: dict, input_path: str) -> str:
    """
    Convert logs to embeddings and update the data file.

    Args:
        config (dict): The configuration dictionary.
        input_path (str): The path to the generated logs JSON.

    Returns:
        str: The path to the JSON file with embeddings.
    """
    print("Starting embedding generation...")
    with open(input_path, 'r', encoding='utf-8') as f:
        dataset = json.load(f)

    embedder = Embedder(config['embedding_model'])
    texts = [sample['text'] for sample in dataset]
    embeddings = embedder.generate_embeddings(texts)

    for i, sample in enumerate(dataset):
        sample['embedding'] = embeddings[i]

    output_path = input_path.replace(".json", "_with_embeddings.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=2)

    print(f"Added embeddings to {len(dataset)} samples and saved to {output_path}")
    return output_path

def run_training(config: dict, data_path: str) -> dict:
    """
    Train models and evaluate performance.

    Args:
        config (dict): The configuration dictionary.
        data_path (str): The path to the JSON file with embeddings.

    Returns:
        dict: Evaluation results.
    """
    print("Starting model training...")
    with open(data_path, 'r', encoding='utf-8') as f:
        dataset = json.load(f)

    trainer = Trainer(dataset)
    if 'logistic_regression' in config['classifiers']:
        trainer.train_logistic_regression()
    if 'svm' in config['classifiers']:
        trainer.train_svm()

    results = trainer.evaluate()
    for name, metrics in results.items():
        print(f"\nResults for {name}:")
        print(f"  Accuracy:  {metrics['accuracy']:.4f}")
        print(f"  Precision: {metrics['precision']:.4f}")
        print(f"  Recall:    {metrics['recall']:.4f}")
        print(f"  F1-Score:  {metrics['f1_score']:.4f}")

    return results

def main():
    """
    Main function to run the POC pipeline.
    """
    config_path = "config/config.yaml"
    if not os.path.exists(config_path):
        print(f"Error: Config file not found at {config_path}")
        return

    config = load_config(config_path)
    logs_path = run_data_generation(config)
    embedded_data_path = run_embedding_generation(config, logs_path)
    run_training(config, embedded_data_path)


if __name__ == "__main__":
    main()
