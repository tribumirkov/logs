# Specification: Multi-Class Log Classification (BGL Categories)

## 1. Overview
This track migrates the classification pipeline from a binary model (Important/Not Important) to a multi-class model based on the original categories found in the Loghub BGL dataset. This involves updating the parser, trainer, and reporting modules.

## 2. Core Components

### 2.1 BGL Category Parsing
- **Categories:** The system will now extract and use the full set of labels from the BGL dataset.
- **Mapping:**
    - `-` -> `NORMAL`
    - `APPREAD`, `APPFATAL`, `KERNELEXIT`, etc. -> Use the actual labels provided in the first column of the BGL logs.
- **Module:** Update `src/data_loader.py` to return the raw label string instead of a 0/1 integer.

### 2.2 Multi-Class Classifier Training
- **Label Encoding:** Implement `LabelEncoder` from `scikit-learn` to convert string categories into numerical indices for training.
- **Classifiers:** Update `LogisticRegression` and `SVM` to handle multi-class classification (e.g., using `ovr` or `multinomial` strategies).
- **Module:** Update `src/trainer.py`.

### 2.3 Comprehensive Reporting
- **Metrics Strategy:** Implement both Macro-Averaging and a detailed Per-Class breakdown.
- **Visualizations:**
    - **Confusion Matrix:** Updated to a larger N x N matrix representing all categories.
    - **PDF Report:** Must include a detailed table with Precision, Recall, and F1-score for *each* category.
- **Module:** Update `src/reporter.py`.

## 3. Acceptance Criteria
- The system correctly parses and encodes at least 5 different categories from the BGL dataset.
- The training pipeline successfully converges on a multi-class classification task.
- The generated PDF report contains a full breakdown of metrics per category and macro-averages.
- `pylint` passes with no errors.
