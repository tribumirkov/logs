"""
Main entry point for the sysadmin log classifier POC.
"""

import json
import os
from src.config import load_config
from src.downloader import download_bgl
from src.embedder import Embedder
from src.trainer import Trainer
from src.data_loader import load_bgl_data
from src.reporter import Reporter


def get_embeddings_path(config: dict) -> str:
    """
    Get the path to the embeddings file.

    Args:
        config (dict): The configuration dictionary.

    Returns:
        str: The path to the JSON file with embeddings.
    """
    return config['data']['output_path'].replace(".json", "_with_embeddings.json")


def run_embedding_generation(config: dict, dataset: list) -> str:
    """
    Convert logs to embeddings and save to JSON.

    Args:
        config (dict): The configuration dictionary.
        dataset (list): The list of parsed log dictionaries.

    Returns:
        str: The path to the JSON file with embeddings.
    """
    output_path = get_embeddings_path(config)

    if os.path.exists(output_path):
        print(f"Embeddings already exist at {output_path}, skipping generation.")
        return output_path

    print("Starting embedding generation...")
    embedder = Embedder(config['embedding_model'])
    texts = [sample['text'] for sample in dataset]
    embeddings = embedder.generate_embeddings(texts)

    for i, sample in enumerate(dataset):
        sample['embedding'] = embeddings[i]

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
        print(f"  Macro Precision: {metrics['macro_precision']:.4f}")
        print(f"  Macro Recall:    {metrics['macro_recall']:.4f}")
        print(f"  Macro F1-Score:  {metrics['macro_f1_score']:.4f}")

    return results

def run_reporting(config: dict, results: dict):
    """
    Generate the PDF report.

    Args:
        config (dict): The configuration dictionary.
        results (dict): The evaluation results.
    """
    print("Generating report...")
    reporter = Reporter(config['report']['output_path'])
    reporter.generate_report(results)

def main():
    """
    Main function to run the POC pipeline.
    """
    config_path = "config/config.yaml"
    if not os.path.exists(config_path):
        print(f"Error: Config file not found at {config_path}")
        return

    config = load_config(config_path)

    # Step 1: Download dataset if not present
    log_file = config['data']['log_path']
    data_dir = os.path.dirname(log_file)
    download_bgl(config['dataset_url'], data_dir)

    # Step 2: Parse log data
    dataset = load_bgl_data(
        log_file,
        total_samples=config['sampling']['total_samples'],
        normal_ratio=config['sampling']['normal_ratio'],
        seed=config['sampling']['seed']
    )

    if not dataset:
        print("Error: No data loaded.")
        return

    # Step 3: Generate embeddings
    embedded_data_path = run_embedding_generation(config, dataset)

    # Step 4: Train classifiers
    results = run_training(config, embedded_data_path)

    # Step 5: Generate report
    run_reporting(config, results)


if __name__ == "__main__":
    main()
