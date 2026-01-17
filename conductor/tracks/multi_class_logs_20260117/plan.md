# Implementation Plan - Track: multi_class_logs_20260117

## Phase 1: Data Loader & Configuration Updates [checkpoint: e8e27b6]

- [x] Task: Update BGL Parser for Multi-Class Labels 81a74cd
    - [ ] Modify `src/data_loader.py` to return the original label string (or map `-` to `NORMAL`).
    - [ ] run pylint.

- [x] Task: Update Configuration 99312bc
    - [ ] Verify `config/config.yaml` is still appropriate for the new multi-class task (e.g., check `max_lines` to ensure all categories are represented).
    - [ ] run pylint.

- [ ] Task: Conductor - User Manual Verification 'Data Loader & Configuration Updates' (Protocol in workflow.md)

## Phase 2: Multi-Class Trainer Implementation [checkpoint: 6011eb9]

- [x] Task: Implement Label Encoding 0da8184
    - [ ] Update `src/trainer.py` to use `scikit-learn.preprocessing.LabelEncoder`.
    - [ ] Store the encoder to allow mapping indices back to category names for reporting.

- [x] Task: Update Classifiers for Multi-Class e3eff73
    - [ ] Ensure `LogisticRegression` and `SVC` are configured for multi-class (default behavior in sklearn usually handles this, but verify `multi_class='multinomial'` or similar).
    - [ ] Update evaluation logic to calculate Macro-Averaged and Per-Class metrics.
    - [ ] run pylint.

- [ ] Task: Conductor - User Manual Verification 'Multi-Class Trainer Implementation' (Protocol in workflow.md)

## Phase 3: Reporting & Final Integration

- [x] Task: Update PDF Reporter for Multi-Class 5ef9834
    - [ ] Modify `src/reporter.py` to handle N categories in confusion matrices.
    - [ ] Implement the detailed metrics table in the PDF output.

- [x] Task: Update Main Pipeline 07b5a73
    - [ ] Update `main.py` to handle the transition of string labels through the pipeline.
    - [ ] run pylint.

- [ ] Task: Conductor - User Manual Verification 'Reporting & Final Integration' (Protocol in workflow.md)
