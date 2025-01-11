import faiss
import os

class VectorStore:
    def __init__(self, dimension, index_file):
        self.index = faiss.IndexFlatL2(dimension)
        self.sentences = []  # Store sentences here
        self.index_file = index_file

    def add_embeddings(self, embeddings, sentences):
        self.index.add(embeddings)
        self.sentences.extend(sentences)

    def search(self, query_embedding, top_k):
        distances, indices = self.index.search(query_embedding, top_k)
        return distances, indices
