# Sysadmin Log Classifier POC

This project is a Proof of Concept (POC) for automatically classifying system logs (specifically from the BGL dataset) into NORMAL and ANOMALY categories using machine learning. It leverages pre-trained embeddings to represent log content and trains classifiers to identify potential issues.

## Features

- **Log Parsing**: Specialized parser for the BGL log format.
- **Stratified Subsampling**: Configurable sampling to balance NORMAL and ANOMALY classes.
- **Embedding Generation**: Uses `sentence-transformers` (specifically Qwen models) to convert log text into high-dimensional vectors.
- **Machine Learning Classifiers**: Supports Logistic Regression and SVM.
- **Automated Reporting**: Generates a PDF report with accuracy metrics and confusion matrices.
- **Config-Driven**: All parameters (dataset paths, sampling ratios, model choices) are managed via `config/config.yaml`.

## Project Structure

```text
├── main.py              # Application entry point
├── src/
│   ├── data_loader.py   # Log parsing and sampling logic
│   ├── embedder.py      # Embedding generation using SentenceTransformers
│   ├── trainer.py       # Model training and evaluation
│   ├── reporter.py      # PDF report generation
│   ├── config.py        # Config loader
│   └── downloader.py    # Dataset download utility
├── config/
│   └── config.yaml      # Project configuration
└── data/                # Directory for input logs and generated embeddings
```

## Installation

This project uses `uv` for dependency management.

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd logs
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

## Usage

### 1. Data Preparation
Ensure your BGL log file is placed in the location specified in `config/config.yaml` (default: `data/BGL.log`).

### 2. Configuration
Adjust parameters in `config/config.yaml` as needed:
- `sampling`: Control the number of samples and the class balance.
- `embedding_model`: Choose the SentenceTransformer model.
- `classifiers`: Select which models to train.

### 3. Run the Pipeline
Execute the main script to parse data, generate embeddings, train models, and create the report:
```bash
uv run main.py
```

### 4. View Results
The generated report will be saved to `output/report.pdf` (or as configured).

## Development

### Linting
To check code quality with Pylint:
```bash
uv run pylint src/*.py main.py
```
