# Implementation Plan - Track: poc_20260117

## Phase 1: Project Setup & Configuration [checkpoint: 0130843]

- [x] Task: Initialize project structure and environment 279f495
    - [ ] Create project directories (`src`, `config`, `data`, `output`).
    - [ ] Initialize `uv` project and add dependencies: `pyyaml`, `pandas`, `numpy`, `scikit-learn`, `sentence-transformers`, `torch`, `matplotlib`, `seaborn`, `fpdf`, `pylint`.
    - [ ] Create initial `config.yaml` with default settings (Model: `Qwen/Qwen3-Embedding-0.6B`).

- [x] Task: Implement Configuration Loader a723997
    - [ ] Create `src/config.py` to load and validate `config.yaml`.
    - [ ] Implement strict PEP 8 linting check.

- [ ] Task: Conductor - User Manual Verification 'Project Setup & Configuration' (Protocol in workflow.md)

## Phase 2: Synthetic Data Generation [checkpoint: ede402b]

- [x] Task: Implement Log Generators e33b1e5
    - [ ] Create `src/generator.py`.
    - [ ] Implement functions to generate Authentication, System, and Network logs.
    - [ ] Implement logic to assign labels (1/0) based on severity rules.

- [x] Task: Implement Data Generation CLI 1951697
    - [ ] Add main execution logic to generate `num_samples` and save to JSON.
    - [ ] Ensure deterministic output using random seed.
    - [ ] run pylint.

- [ ] Task: Conductor - User Manual Verification 'Synthetic Data Generation' (Protocol in workflow.md)

## Phase 3: Embedding Pipeline [checkpoint: f2f9c79]

- [x] Task: Implement Embedding Generator 9a2fc4c
    - [ ] Create `src/embedder.py`.
    - [ ] Implement model loading using `sentence-transformers` (compatible with Qwen).
    - [ ] Implement batch processing to convert log text to embeddings.

- [x] Task: Integrate Embedding with Data Pipeline 81c37ae
    - [ ] Update pipeline to read generated JSON, add embeddings, and save to new JSON file.
    - [ ] run pylint.

- [ ] Task: Conductor - User Manual Verification 'Embedding Pipeline' (Protocol in workflow.md)

## Phase 4: Classifier Training & Evaluation

- [x] Task: Implement Model Trainer d5cad1d
    - [ ] Create `src/trainer.py`.
    - [ ] Implement data loading and train/test split.
    - [ ] Implement `train_logistic_regression` and `train_svm`.

- [x] Task: Implement Evaluation Metrics 59e8a70
    - [ ] Add metric calculation (Accuracy, Precision, Recall, F1).
    - [ ] Generate confusion matrices and ROC curve data.
    - [ ] run pylint.

- [ ] Task: Conductor - User Manual Verification 'Classifier Training & Evaluation' (Protocol in workflow.md)

## Phase 5: Reporting & CLI Integration

- [ ] Task: Implement PDF Reporter
    - [ ] Create `src/reporter.py`.
    - [ ] Implement plotting functions (Confusion Matrix, ROC) using matplotlib.
    - [ ] Implement PDF generation to compile text metrics and plots.

- [ ] Task: Create Main CLI Entrypoint
    - [ ] Create `main.py` to orchestrate the full pipeline: Config -> Gen -> Embed -> Train -> Report.
    - [ ] run pylint.

- [ ] Task: Conductor - User Manual Verification 'Reporting & CLI Integration' (Protocol in workflow.md)
