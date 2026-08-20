from sentence_transformers import CrossEncoder
import torch

print("Reranker yükleniyor...")

device = "cuda" if torch.cuda.is_available() else "cpu"

model = CrossEncoder(
    "BAAI/bge-reranker-base",
    device=device
)

print("Reranker hazır.")


def rerank(question, documents, top_k=4):

    if not documents:
        return []

    question_lower = question.lower()

    pairs = []

    for doc in documents:

        title = str(doc.get("title", ""))

        text = f"{title}\n\n{doc['text']}"

        pairs.append((question, text))

    scores = model.predict(pairs)

    ranked = []

    for score, doc in zip(scores, documents):

        title = str(doc.get("title", "")).lower()

        bonus = 0.0

        if question_lower in title:
            bonus += 0.40
        else:
            for word in question_lower.split():

                if len(word) < 3:
                    continue

                if word in title:
                    bonus += 0.12

        final_score = float(score) + bonus

        new_doc = doc.copy()
        new_doc["rerank_score"] = final_score

        ranked.append((final_score, new_doc))

    ranked.sort(
        key=lambda x: x[0],
        reverse=True
    )

    return [doc for _, doc in ranked[:top_k]]