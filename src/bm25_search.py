from rank_bm25 import BM25Okapi
import re


class BM25Search:

    def __init__(self):

        self.documents = []
        self.tokenized_documents = []
        self.bm25 = None

    # ----------------------------------------------------

    def tokenize(self, text):

        text = text.lower()

        text = re.sub(r"[^\wçğıöşü\s]", " ", text)

        return text.split()

    # ----------------------------------------------------

    def build(self, documents):

        self.documents = documents

        corpus = []

        for doc in documents:

            title = str(doc.get("title", ""))

            text = title + " " + doc["text"]

            corpus.append(
                self.tokenize(text)
            )

        self.tokenized_documents = corpus

        self.bm25 = BM25Okapi(corpus)

    # ----------------------------------------------------

    def search(self, query, top_k=10):

        if self.bm25 is None:
            return []

        tokens = self.tokenize(query)

        scores = self.bm25.get_scores(tokens)

        ranked = sorted(
            zip(scores, self.documents),
            key=lambda x: x[0],
            reverse=True
        )

        results = []

        for score, doc in ranked[:top_k]:

            new_doc = doc.copy()

            new_doc["bm25_score"] = float(score)

            results.append(new_doc)

        return results