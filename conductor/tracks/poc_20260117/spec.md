# Specification: Core Sysadmin Log Classifier POC

## 1. Overview
This track focuses on building a functional Proof of Concept (POC) for classifying sysadmin logs. The system will generate synthetic log data, convert logs into embeddings using a specified model, and train two types of classifiers (Logistic Regression and SVM). The final output will be a comprehensive PDF report containing performance metrics and visualizations, driven by a central configuration file.

## 2. Core Components

### 2.1 Configuration
- **File:** `config.yaml`
- **Parameters:**
  - `embedding_model`: String (default: `Qwen/Qwen3-Embedding-0.6B`)
  - `data`:
    - `num_samples`: Integer (e.g., 1000)
    - `output_path`: String (path to save JSON)
    - `random_seed`: Integer (for reproducibility)
  - `classifiers`: List of strings (`['logistic_regression', 'svm']`)
  - `report`:
    - `output_path`: String (e.g., `report.pdf`)

### 2.2 Synthetic Data Generator
- **Input:** Configuration (num_samples, seed).
- **Functionality:**
  - Generates realistic sysadmin logs (Authentication, System Service, Network/Firewall).
  - Assigns labels:
    - `1` (Important): Critical errors, security alerts, failed logins.
    - `0` (Not Important): Info messages, debug logs, successful routine operations.
- **Output:** JSON file containing a list of objects: `{"text": "...", "label": 0/1}`.

### 2.3 Embedding Pipeline
- **Input:** JSON data from generator, Model name from config.
- **Functionality:**
  - Loads the specified model using `sentence-transformers` (or compatible library).
  - Batches log texts and generates embeddings.
- **Output:** Augmented JSON data: `{"text": "...", "label": 0/1, "embedding": [...]}`.

### 2.4 Classifier Training
- **Input:** Augmented JSON data with embeddings.
- **Functionality:**
  - Splits data into training and testing sets.
  - Trains `LogisticRegression` and `SVC` (SVM) from `scikit-learn`.
  - Evaluates models on the test set.
- **Output:** Dictionary of metrics (Accuracy, Precision, Recall, F1) and model objects (in memory or saved if needed).

### 2.5 Reporting
- **Input:** Evaluation metrics and test results.
- **Functionality:**
  - Generates confusion matrices and ROC curves.
  - Compiles metrics and plots into a PDF report.
- **Output:** PDF file (e.g., `classifier_report.pdf`).

## 3. Data Flow
1. **User** runs CLI command with config path.
2. **System** reads `config.yaml`.
3. **Generator** creates logs -> `data.json`.
4. **Embedder** adds embeddings -> `data_with_embeddings.json`.
5. **Trainer** trains models and calculates metrics.
6. **Reporter** visualizes results and saves `report.pdf`.

## 4. Technology Stack Alignment
- **Language:** Python
- **Libraries:** `uv`, `pylint`, `PyYAML`, `pandas`, `scikit-learn`, `sentence-transformers` (for Qwen model compatibility), `matplotlib`/`seaborn` (for plots), `fpdf` or `reportlab` (for PDF generation).
- **Style:** PEP 8 strict, no unit tests.
