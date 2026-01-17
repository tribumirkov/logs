"""
PDF reporter module.

This module generates a PDF report containing classification metrics
and visualizations for the multi-class log classifier.
"""

import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
from fpdf import FPDF


class PDFReport(FPDF):
    """
    Custom PDF class for the report.
    """

    # pylint: disable=too-few-public-methods

    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Sysadmin Log Classifier Report', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')


class Reporter:
    """
    Generates the PDF report.
    """

    # pylint: disable=too-few-public-methods

    def __init__(self, output_path: str):

        self.output_path = output_path
        self.pdf = PDFReport()
        self.pdf.add_page()

    def _add_plot(self, title: str, plot_func, *args, **kwargs):
        """Helper to add a matplotlib plot to the PDF."""
        plt.figure(figsize=(10, 6))
        plot_func(*args, **kwargs)
        plt.title(title)

        # Save plot to temporary file
        temp_img = "temp_plot.png"
        plt.savefig(temp_img, bbox_inches='tight')
        plt.close()

        # Add to PDF
        self.pdf.set_font('Arial', 'B', 12)
        self.pdf.cell(0, 10, title, 0, 1)
        self.pdf.image(temp_img, w=170)
        self.pdf.ln(5)

        if os.path.exists(temp_img):
            os.remove(temp_img)

    def _plot_confusion_matrix(self, y_true, y_pred, classes):
        """Plots the confusion matrix."""
        cm = confusion_matrix(y_true, y_pred)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                    xticklabels=classes, yticklabels=classes)
        plt.xlabel('Predicted')
        plt.ylabel('True')

    def generate_report(self, results: dict):
        """
        Generate the PDF report from evaluation results.

        Args:
            results (dict): The dictionary returned by Trainer.evaluate().
        """
        for model_name, metrics in results.items():
            self.pdf.set_font('Arial', 'B', 14)
            self.pdf.cell(0, 10, f"Model: {model_name.replace('_', ' ').title()}", 0, 1)
            self.pdf.ln(2)

            # Summary Metrics
            self.pdf.set_font('Arial', '', 11)
            self.pdf.cell(0, 8, f"Overall Accuracy: {metrics['accuracy']:.4f}", 0, 1)
            self.pdf.cell(0, 8, f"Macro Precision: {metrics['macro_precision']:.4f}", 0, 1)
            self.pdf.cell(0, 8, f"Macro Recall:    {metrics['macro_recall']:.4f}", 0, 1)
            self.pdf.cell(0, 8, f"Macro F1-Score:  {metrics['macro_f1_score']:.4f}", 0, 1)
            self.pdf.ln(5)

            # Per-Class Metrics Table
            self.pdf.set_font('Arial', 'B', 12)
            self.pdf.cell(0, 10, "Per-Class Metrics:", 0, 1)

            self.pdf.set_font('Arial', 'B', 10)
            col_width = 45
            self.pdf.cell(col_width, 8, "Class", 1)
            self.pdf.cell(col_width, 8, "Precision", 1)
            self.pdf.cell(col_width, 8, "Recall", 1)
            self.pdf.cell(col_width, 8, "F1-Score", 1)
            self.pdf.ln()

            self.pdf.set_font('Arial', '', 10)
            for cls, scores in metrics['per_class_metrics'].items():
                self.pdf.cell(col_width, 8, str(cls), 1)
                self.pdf.cell(col_width, 8, f"{scores['precision']:.4f}", 1)
                self.pdf.cell(col_width, 8, f"{scores['recall']:.4f}", 1)
                self.pdf.cell(col_width, 8, f"{scores['f1_score']:.4f}", 1)
                self.pdf.ln()
            self.pdf.ln(10)

            # Confusion Matrix
            y_test = metrics['y_test']
            y_pred = metrics['y_pred']
            classes = metrics['classes']

            # Map indices back to class names for plotting if needed,
            # but confusion_matrix takes y_true/y_pred as is.
            # We just need labels for the axis.

            self._add_plot(
                f"Confusion Matrix ({model_name})",
                self._plot_confusion_matrix,
                y_test, y_pred, classes
            )

            self.pdf.add_page()


        # Save PDF
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        self.pdf.output(self.output_path)
        print(f"Report saved to {self.output_path}")
