import torch
from sentence_transformers import SentenceTransformer
from settings import EMBEDDING_MODEL

print("Embedding modeli yükleniyor...")

device = "cuda" if torch.cuda.is_available() else "cpu"

print("Kullanılan cihaz:", device)

model = SentenceTransformer(
    EMBEDDING_MODEL,
    device=device
)

print("Embedding hazır")


def get_embedding(text):
    return model.encode(
        text,
        normalize_embeddings=True
    ).tolist()