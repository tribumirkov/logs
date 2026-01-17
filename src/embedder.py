"""
Embedding generator module.

This module converts text logs into numerical embeddings using a
pre-trained model from Sentence Transformers.
"""

from sentence_transformers import SentenceTransformer


class Embedder:
    """
    Handles generation of text embeddings.
    """

    # pylint: disable=too-few-public-methods

    def __init__(self, model_name: str):

        """
        Initialize the embedder with a specific model.

        Args:
            model_name (str): The name or path of the model to load.
        """
        print(f"Loading embedding model: {model_name}...")
        self.model = SentenceTransformer(model_name, trust_remote_code=True)

    def generate_embeddings(self, texts: list) -> list:
        """
        Generate embeddings for a list of texts.

        Args:
            texts (list): A list of strings to embed.

        Returns:
            list: A list of embeddings (each embedding is a list of floats).
        """
        embeddings = self.model.encode(texts, show_progress_bar=True)
        # Convert numpy arrays to lists for JSON serialization
        return embeddings.tolist()
