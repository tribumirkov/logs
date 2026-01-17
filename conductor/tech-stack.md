# Technology Stack

## 1. Programming Language
- **Python:** Chosen for its dominance in the Machine Learning ecosystem, providing mature libraries for data manipulation, embedding generation, and classification.

## 2. Machine Learning Frameworks
- **PyTorch/TensorFlow:** Used for building and training the classification models. This allows for potential expansion from simple linear models (implemented as neural layers) to more complex architectures if the POC evolves.
- **Sentence-Transformers:** Integrated to provide a wide range of pre-trained models for generating high-quality log embeddings.
- **scikit-learn:** Utilized for data preprocessing and evaluation metrics.

## 3. Data Handling & Utilities
- **PyYAML:** For parsing the `config.yaml` file that governs the system's settings.
- **NumPy & Pandas:** For efficient numerical operations and structured data handling during the training and inference phases.
- **JSON:** Standard format for the intermediate and final datasets (logs + labels + embeddings).

## 4. Development & Testing
- **Pytest:** For unit testing the data generator, embedding pipeline, and classifier logic.
