import faiss
import os
import pickle  # For saving and loading sentences

class VectorStore:
    def __init__(self, dimension, index_file):
        self.index = faiss.IndexFlatL2(dimension)
        self.sentences = []  # Store sentences here
        self.index_file = index_file  # File to store FAISS index
        self.sentences_file = f"{index_file}_sentences.pkl"  # File to store sentences

    def add_embeddings(self, embeddings, sentences):
        """Add embeddings and corresponding sentences to the vector store."""
        self.index.add(embeddings)
        self.sentences.extend(sentences)

    def search(self, query_embedding, top_k):
        """Search the vector store for the top K similar embeddings."""
        distances, indices = self.index.search(query_embedding, top_k)
        print(f"Distances: {distances}")
        print(f"Indices: {indices}")
        return distances, indices

    def save(self):
        """Save the FAISS index and sentences to disk."""
        # Save FAISS index
        faiss.write_index(self.index, self.index_file)
        # Save sentences using pickle
        with open(self.sentences_file, 'wb') as f:
            pickle.dump(self.sentences, f)
        print(f"Vector store saved to {self.index_file} and {self.sentences_file}.")

    def load(self):
        """Load the FAISS index and sentences from disk."""
        if os.path.exists(self.index_file) and os.path.exists(self.sentences_file):
            # Load FAISS index
            self.index = faiss.read_index(self.index_file)
            # Load sentences using pickle
            with open(self.sentences_file, 'rb') as f:
                self.sentences = pickle.load(f)
            print(f"Vector store loaded from {self.index_file} and {self.sentences_file}.")
        else:
            raise FileNotFoundError("Vector store files not found.")
