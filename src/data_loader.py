"""
BGL log parser module.

This module provides functions to parse the BGL log format and convert
it into a standardized format for training.
"""

import random
from collections import defaultdict

# Constants
LABEL_NORMAL = 0
LABEL_ANOMALY = 1
MIN_BGL_TOKENS = 10
CONTENT_START_INDEX = 9


def parse_bgl_line(line: str) -> dict:
    """
    Parse a single line of BGL log.

    BGL format: <Label> <Timestamp> <Date> <Node> <Time> <NodeRepeat>
                <Type> <Component> <Level> <Content>

    Args:
        line (str): A single line from the BGL log file.

    Returns:
        dict: A dictionary with 'text' and 'label', or None if parsing fails.
    """
    parts = line.split()
    if len(parts) < MIN_BGL_TOKENS:
        return None

    # Label is the first field.
    # '-' means non-alert (NORMAL), everything else is an anomaly.
    label_str = parts[0]
    label = LABEL_NORMAL if label_str == "-" else LABEL_ANOMALY

    # Content starts from the 10th field (index 9)
    # We join back the remaining parts as they were split by whitespace
    content = " ".join(parts[CONTENT_START_INDEX:])

    return {"text": content, "label": label}


def load_bgl_data(
    file_path: str,
    total_samples: int,
    normal_ratio: float,
    seed: int
) -> list:
    """
    Load and parse BGL log data, then create stratified random subsamples.

    Parses the entire file, groups by label, then samples to create a dataset
    where NORMAL is ~70% (configurable) and anomaly classes share the rest.
    Deduplicates samples by text content to prevent data leakage between
    train and dev sets.

    Args:
        file_path (str): Path to the BGL.log file.
        total_samples (int): Target total number of samples in output.
        normal_ratio (float): Ratio of NORMAL samples.
        seed (int): Random seed for reproducibility.

    Returns:
        list: A list of parsed log dictionaries.
    """
    random.seed(seed)

    print(f"Parsing entire BGL data from {file_path}...")

    samples_by_label = defaultdict(list)
    seen_texts = set()
    duplicates_removed = 0

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            for line in file:
                parsed = parse_bgl_line(line.strip())
                if parsed:
                    text = parsed['text']
                    if text not in seen_texts:
                        seen_texts.add(text)
                        samples_by_label[parsed['label']].append(parsed)
                    else:
                        duplicates_removed += 1
    except FileNotFoundError:
        print(f"Error: BGL log file not found at {file_path}")
        return []

    print(f"Parsed {sum(len(v) for v in samples_by_label.values())} unique samples "
          f"({duplicates_removed} duplicates removed)")
    print(f"  NORMAL ({LABEL_NORMAL}): {len(samples_by_label.get(LABEL_NORMAL, []))} samples")
    print(f"  ANOMALY ({LABEL_ANOMALY}): {len(samples_by_label.get(LABEL_ANOMALY, []))} samples")

    # Calculate target counts
    normal_count = int(total_samples * normal_ratio)
    anomaly_count = total_samples - normal_count

    # Sample from each class
    dataset = []

    # Sample NORMAL
    normal_samples = samples_by_label.get(LABEL_NORMAL, [])
    if len(normal_samples) >= normal_count:
        dataset.extend(random.sample(normal_samples, normal_count))
    else:
        dataset.extend(normal_samples)
        print(f"Warning: Only {len(normal_samples)} NORMAL samples available")

    # Sample ANOMALY
    anomaly_samples = samples_by_label.get(LABEL_ANOMALY, [])
    if len(anomaly_samples) >= anomaly_count:
        dataset.extend(random.sample(anomaly_samples, anomaly_count))
    else:
        dataset.extend(anomaly_samples)
        print(f"Warning: Only {len(anomaly_samples)} ANOMALY samples available")

    # Shuffle the final dataset
    random.shuffle(dataset)

    print(f"\nFinal dataset: {len(dataset)} samples")
    normal_final = sum(1 for s in dataset if s['label'] == LABEL_NORMAL)
    anomaly_final = sum(1 for s in dataset if s['label'] == LABEL_ANOMALY)
    print(f"  NORMAL ({LABEL_NORMAL}): {normal_final} "
          f"({normal_final / len(dataset) * 100:.1f}%)")
    print(f"  ANOMALY ({LABEL_ANOMALY}): {anomaly_final} "
          f"({anomaly_final / len(dataset) * 100:.1f}%)")

    return dataset
