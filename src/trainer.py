"""
Model trainer module.

This module provides functions to train and evaluate classification models
(Logistic Regression and SVM) using log embeddings.
"""

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.preprocessing import LabelEncoder


class Trainer:
    """
    Handles model training and evaluation.
    """

    # pylint: disable=too-many-instance-attributes
    def __init__(self, data: list):
        """
        Initialize the trainer with augmented log data.

        Args:
            data (list): List of dictionaries with 'embedding' and 'label'.
        """
        self.embeddings = np.array([sample['embedding'] for sample in data])

        # Encode string labels into integers
        raw_labels = [sample['label'] for sample in data]
        self.label_encoder = LabelEncoder()
        self.labels = self.label_encoder.fit_transform(raw_labels)

        self.classes = self.label_encoder.classes_
        print(f"Detected {len(self.classes)} classes: {self.classes}")

        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(
            self.embeddings, self.labels, test_size=0.2, random_state=42
        )
        self.models = {}

    def train_logistic_regression(self):
        """
        Train a Logistic Regression classifier.
        """
        print("Training Logistic Regression...")
        # multi_class='multinomial' is auto-selected but good to be explicit or leave default
        model = LogisticRegression(max_iter=1000)
        model.fit(self.x_train, self.y_train)
        self.models['logistic_regression'] = model

    def train_svm(self):
        """
        Train a Support Vector Machine (SVM) classifier.
        """
        print("Training SVM...")
        model = SVC(probability=True)
        model.fit(self.x_train, self.y_train)
        self.models['svm'] = model

    def evaluate(self) -> dict:
        """
        Evaluate all trained models on the test set.

        Returns:
            dict: Evaluation metrics for each model.
        """
        results = {}
        for name, model in self.models.items():
            y_pred = model.predict(self.x_test)
            accuracy = accuracy_score(self.y_test, y_pred)

            # Calculate metrics for each class (Macro and Per-Class)
            precision, recall, f1, _ = precision_recall_fscore_support(
                self.y_test, y_pred, average=None, labels=range(len(self.classes))
            )

            # Macro averages
            macro_precision, macro_recall, macro_f1, _ = precision_recall_fscore_support(
                self.y_test, y_pred, average='macro'
            )

            results[name] = {
                'accuracy': accuracy,
                'macro_precision': macro_precision,
                'macro_recall': macro_recall,
                'macro_f1_score': macro_f1,
                'per_class_metrics': {
                    self.classes[i]: {
                        'precision': precision[i],
                        'recall': recall[i],
                        'f1_score': f1[i]
                    } for i in range(len(self.classes))
                },
                'y_test': self.y_test.tolist(),
                'y_pred': y_pred.tolist(),
                'classes': self.classes.tolist()
            }
        return results
