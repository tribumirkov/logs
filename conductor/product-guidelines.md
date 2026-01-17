# Product Guidelines

## 1. Documentation Style: Technical & Explicit
- **Mathematical Clarity:** For modules involving embeddings and classification algorithms (Logistic Regression, SVM), the code should include comments explaining the underlying principles or references to the relevant methodologies.
- **Comprehensive Docstrings:** Every function and class must have a docstring that clearly defines inputs, outputs, and any side effects.
- **Example Usage:** Where appropriate, include short code examples within docstrings to demonstrate how to instantiate and use key components like the classifier or the data generator.

## 2. Configuration & Interaction: Configuration-Driven
- **Centralized Settings:** A primary configuration file (e.g., `config.json` or `config.yaml`) should be the source of truth for the system's behavior.
- **Configurable Parameters:**
    - **Embeddings:** Model name or path for the embedding generator.
    - **Classification:** Choice of algorithm (`logistic_regression`, `svm`) and their respective hyperparameters.
    - **Data:** Paths for synthetic data generation output and training data input.
- **Minimal CLI Overrides:** While the configuration file is the primary interface, the CLI may allow for simple overrides (e.g., specifying a different config file path).

## 3. Data Integrity
- **Reproducibility:** The synthetic data generation must be deterministic given a specific random seed, ensuring that results can be validated and compared across different runs.
- **Schema Validation:** The system should perform basic validation on the JSON data structures (log, importance, embedding) to ensure the training pipeline receives well-formatted input.
