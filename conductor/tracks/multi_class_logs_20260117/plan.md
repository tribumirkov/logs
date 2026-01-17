# Implementation Plan - Track: multi_class_logs_20260117

## Phase 1: Data Loader & Configuration Updates

- [x] Task: Update BGL Parser for Multi-Class Labels 81a74cd
    - [ ] Modify `src/data_loader.py` to return the original label string (or map `-` to `NORMAL`).
    - [ ] run pylint.

- [ ] Task: Update Configuration
    - [ ] Verify `config/config.yaml` is still appropriate for the new multi-class task (e.g., check `max_lines` to ensure all categories are represented).
    - [ ] run pylint.

- [ ] Task: Conductor - User Manual Verification 'Data Loader & Configuration Updates' (Protocol in workflow.md)

## Phase 2: Multi-Class Trainer Implementation

- [ ] Task: Implement Label Encoding
    - [ ] Update `src/trainer.py` to use `scikit-learn.preprocessing.LabelEncoder`.
    - [ ] Store the encoder to allow mapping indices back to category names for reporting.

- [ ] Task: Update Classifiers for Multi-Class
    - [ ] Ensure `LogisticRegression` and `SVC` are configured for multi-class (default behavior in sklearn usually handles this, but verify `multi_class='multinomial'` or similar).
    - [ ] Update evaluation logic to calculate Macro-Averaged and Per-Class metrics.
    - [ ] run pylint.

- [ ] Task: Conductor - User Manual Verification 'Multi-Class Trainer Implementation' (Protocol in workflow.md)

## Phase 3: Reporting & Final Integration

- [ ] Task: Update PDF Reporter for Multi-Class
    - [ ] Modify `src/reporter.py` to handle N categories in confusion matrices.
    - [ ] Implement the detailed metrics table in the PDF output.

- [ ] Task: Update Main Pipeline
    - [ ] Update `main.py` to handle the transition of string labels through the pipeline.
    - [ ] run pylint.

- [ ] Task: Conductor - User Manual Verification 'Reporting & Final Integration' (Protocol in workflow.md)
