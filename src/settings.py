# =========================
# EMBEDDING
# =========================

EMBEDDING_MODEL = "BAAI/bge-m3"

# =========================
# RERANKER
# =========================

RERANKER_MODEL = "BAAI/bge-reranker-v2-m3"

# =========================
# CHUNKING
# =========================

# Yaklaşık karakter sayısı
CHUNK_SIZE = 800

# Her chunk arasında ortak metin
CHUNK_OVERLAP = 150

# =========================
# RETRIEVAL
# =========================

# FAISS'ten ilk getirilecek belge sayısı
SEARCH_K = 15

# Reranker sonrası kullanılacak belge sayısı
FINAL_K = 5

# Cosine similarity eşiği
DISTANCE_THRESHOLD = 0.35

# =========================
# LLM
# =========================

TEMPERATURE = 0.0

MAX_TOKENS = 180

# =========================
# DATABASE
# =========================

DB_FOLDER = "db"

PDF_FOLDER = "data"