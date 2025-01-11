from sentence_transformers import SentenceTransformer

class EmbeddingService:
    def __init__(self, model_name):
        self.model = SentenceTransformer(model_name)

    def generate_embeddings(self, text):
        sentences = text.split('\n')
        embeddings = self.model.encode(sentences)
        return embeddings, sentences
