"""
Main entry point for the sysadmin log classifier POC.
"""

import json
import os
from src.config import load_config
from src.embedder import Embedder
from src.trainer import Trainer
from src.data_loader import load_bgl_data


def run_embedding_generation(config: dict, dataset: list) -> str:
    """
    Convert logs to embeddings and save to JSON.

    Args:
        config (dict): The configuration dictionary.
        dataset (list): The list of parsed log dictionaries.

    Returns:
        str: The path to the JSON file with embeddings.
    """
    print("Starting embedding generation...")
    embedder = Embedder(config['embedding_model'])
    texts = [sample['text'] for sample in dataset]
    embeddings = embedder.generate_embeddings(texts)

    for i, sample in enumerate(dataset):
        sample['embedding'] = embeddings[i]

    output_path = config['data']['output_path'].replace(".json", "_with_embeddings.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

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

    # Dataset Retrieval (Skipped as requested)
    # from src.downloader import download_bgl
    # download_bgl(config['dataset_url'])

    # Data Parsing
    log_file = "data/BGL.log"
    dataset = load_bgl_data(log_file, max_lines=config['max_lines'])

    if not dataset:
        print("Error: No data loaded.")
        return

    # Pipeline: Embed -> Train
    embedded_data_path = run_embedding_generation(config, dataset)
    run_training(config, embedded_data_path)


if __name__ == "__main__":
    main()
