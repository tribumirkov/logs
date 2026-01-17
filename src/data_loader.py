"""
BGL log parser module.

This module provides functions to parse the BGL log format and convert
it into a standardized format for training.
"""


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
    if len(parts) < 10:
        return None

    # Label is the first field.
    # '-' means non-alert, which we map to 'NORMAL'.
    # Otherwise, we use the label string as-is (e.g., 'APPREAD', 'FATAL').
    label_str = parts[0]
    label = "NORMAL" if label_str == "-" else label_str

    # Content starts from the 10th field (index 9)
    # We join back the remaining parts as they were split by whitespace
    content = " ".join(parts[9:])

    return {"text": content, "label": label}


def load_bgl_data(file_path: str, max_lines: int = 2000) -> list:
    """
    Load and parse BGL log data from a file.

    Args:
        file_path (str): Path to the BGL.log file.
        max_lines (int): Maximum number of lines to parse.

    Returns:
        list: A list of parsed log dictionaries.
    """
    dataset = []
    print(f"Parsing BGL data from {file_path} (max_lines={max_lines})...")

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            for i, line in enumerate(file):
                if i >= max_lines:
                    break
                parsed = parse_bgl_line(line.strip())
                if parsed:
                    dataset.append(parsed)
    except FileNotFoundError:
        print(f"Error: BGL log file not found at {file_path}")
        return []

    print(f"Successfully parsed {len(dataset)} samples.")
    return dataset