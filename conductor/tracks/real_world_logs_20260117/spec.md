# Specification: Real-World Log Integration (Loghub BGL)

## 1. Overview
This track replaces the synthetic log generator with an external, real-world dataset (Loghub BGL). To maintain efficiency for this POC, the system will download the dataset and process only a truncated subset (first 2000 lines).

## 2. Core Components

### 2.1 Data Retrieval & Management
- **Dataset:** Loghub BGL (BlueGene/L Supercomputer logs).
- **Removal:** Delete `src/generator.py` and remove references in `main.py`.
- **Retrieval Logic:**
    - A new module `src/downloader.py` will check for `data/BGL.log`.
    - If missing, it will download the BGL dataset from a public URL (e.g., Logpai repository).
- **Truncation:** The system will implement a loader that reads only the first 2000 lines of the file to ensure the embedding and training phases remain fast.

### 2.2 Data Loading & Parsing
- **Format:** BGL logs use a specific format: `<Label> <Timestamp> <Date> <Node> <Time> <NodeRepeat> <Type> <Component> <Level> <Content>`.
- **Label Mapping:**
    - In BGL, `-` indicates non-alert (0) and everything else (e.g., `FATAL`, `ERROR`) indicates an alert/anomaly (1).
- **Output:** The loader will convert these parsed lines into the standard JSON schema: `{"text": "<Content>", "label": 0/1}`.

### 2.3 Configuration Updates
- **File:** `config.yaml`
- **New Fields:**
    - `dataset_url`: Public URL for the BGL dataset.
    - `max_lines`: 2000 (default).
- **Removed Fields:**
    - All fields under `data` that were specific to the synthetic generator.

## 3. Acceptance Criteria
- `src/generator.py` is deleted.
- The system successfully downloads `BGL.log` if it is missing.
- The system parses the first 2000 lines, correctly assigning binary labels (0/1).
- The existing embedding and training pipeline functions correctly using this real-world data.
- `pylint` passes with no errors.
