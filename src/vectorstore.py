import os
import pickle

import faiss
import numpy as np


class VectorStore:

    def __init__(self, dimension):

        # Cosine Similarity
        self.index = faiss.IndexFlatIP(dimension)

        self.documents = []

    # --------------------------------------------------

    def add(self, embeddings, documents):

        vectors = np.asarray(
            embeddings,
            dtype=np.float32
        )

        faiss.normalize_L2(vectors)

        self.index.add(vectors)

        self.documents.extend(documents)

    # --------------------------------------------------

    def search(self, embedding, k=15, threshold=0.40):

        vector = np.asarray(
            [embedding],
            dtype=np.float32
        )

        faiss.normalize_L2(vector)

        scores, indices = self.index.search(vector, k)

        results = []

        seen = set()

        for score, idx in zip(scores[0], indices[0]):

            if idx == -1:
                continue

            if score < threshold:
                continue

            doc = self.documents[idx].copy()

            key = (
                doc["pdf"],
                doc["page"],
                doc["text"]
            )

            if key in seen:
                continue

            seen.add(key)

            if len(doc["text"]) < 60:
                continue

            doc["score"] = float(score)

            results.append(doc)

        results.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return results

    # --------------------------------------------------

    def save(self, folder="db"):

        os.makedirs(folder, exist_ok=True)

        faiss.write_index(
            self.index,
            os.path.join(folder, "index.faiss")
        )

        with open(
            os.path.join(folder, "texts.pkl"),
            "wb"
        ) as f:

            pickle.dump(
                self.documents,
                f
            )

    # --------------------------------------------------

    def load(self, folder="db"):

        self.index = faiss.read_index(
            os.path.join(folder, "index.faiss")
        )

        with open(
            os.path.join(folder, "texts.pkl"),
            "rb"
        ) as f:

            self.documents = pickle.load(f)