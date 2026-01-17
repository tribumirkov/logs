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


class Trainer:
    """
    Handles model training and evaluation.
    """

    def __init__(self, data: list):
        """
        Initialize the trainer with augmented log data.

        Args:
            data (list): List of dictionaries with 'embedding' and 'label'.
        """
        self.embeddings = np.array([sample['embedding'] for sample in data])
        self.labels = np.array([sample['label'] for sample in data])
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(
            self.embeddings, self.labels, test_size=0.2, random_state=42
        )
        self.models = {}

    def train_logistic_regression(self):
        """
        Train a Logistic Regression classifier.
        """
        print("Training Logistic Regression...")
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
            precision, recall, f1, _ = precision_recall_fscore_support(
                self.y_test, y_pred, average='binary'
            )
            results[name] = {
                'accuracy': accuracy,
                'precision': precision,
                'recall': recall,
                'f1_score': f1,
                'y_test': self.y_test.tolist(),
                'y_pred': y_pred.tolist(),
                # For ROC curve
                'y_score': model.predict_proba(self.x_test)[:, 1].tolist()
            }
        return results
