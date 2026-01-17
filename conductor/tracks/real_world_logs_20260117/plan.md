# Implementation Plan - Track: real_world_logs_20260117

## Phase 1: Cleanup & Configuration

- [x] Task: Remove Synthetic Data Generator c458820
    - [ ] Delete `src/generator.py`.
    - [ ] Remove `generator.py` imports and calls from `main.py`.
    - [ ] run pylint.

- [ ] Task: Update Configuration for External Data
    - [ ] Update `config/config.yaml` to include `dataset_url` and `max_lines`.
    - [ ] Remove synthetic generation parameters from `config/config.yaml`.
    - [ ] Update `src/config.py` to validate new fields if necessary.
    - [ ] run pylint.

- [ ] Task: Conductor - User Manual Verification 'Cleanup & Configuration' (Protocol in workflow.md)

## Phase 2: Data Retrieval & Parsing

- [ ] Task: Implement Dataset Downloader
    - [ ] Create `src/downloader.py`.
    - [ ] Implement logic to download BGL dataset if `data/BGL.log` is missing.
    - [ ] run pylint.

- [ ] Task: Implement BGL Log Parser
    - [ ] Create `src/data_loader.py`.
    - [ ] Implement parsing for BGL format.
    - [ ] Implement label mapping ( '-' to 0, others to 1).
    - [ ] Implement truncation logic to read only `max_lines`.
    - [ ] run pylint.

- [ ] Task: Conductor - User Manual Verification 'Data Retrieval & Parsing' (Protocol in workflow.md)

## Phase 3: Pipeline Integration & Verification

- [ ] Task: Integrate BGL Loader into Main Pipeline
    - [ ] Update `main.py` to orchestrate: Download -> Parse -> Embed -> Train -> Report.
    - [ ] Ensure the parsed BGL data flows correctly into the existing `Embedder` and `Trainer`.
    - [ ] run pylint.

- [ ] Task: Final Pipeline Verification
    - [ ] Run the full pipeline with `uv run python main.py`.
    - [ ] Verify that embeddings are generated for real logs and models are trained.
    - [ ] Verify the PDF report is generated with new metrics.
    - [ ] run pylint.

- [ ] Task: Conductor - User Manual Verification 'Pipeline Integration & Verification' (Protocol in workflow.md)
