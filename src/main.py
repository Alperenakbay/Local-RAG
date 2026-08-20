import os

from ingest import read_all_pdfs
from embedding import get_embedding
from vectorstore import VectorStore
from reranker import rerank
from bm25_search import BM25Search
from chat import ask_llm

from settings import (
    DB_FOLDER,
    PDF_FOLDER,
    SEARCH_K,
    FINAL_K
)


# ==========================================================
# BAŞLANGIÇ
# ==========================================================

print("Local RAG başlatılıyor...")


# ==========================================================
# EMBEDDING
# ==========================================================

dimension = len(get_embedding("test"))

db = VectorStore(dimension)

bm25 = BM25Search()


# ==========================================================
# DATABASE
# ==========================================================

index_path = os.path.join(
    DB_FOLDER,
    "index.faiss"
)


if os.path.exists(index_path):

    print("Veritabanı yükleniyor...")

    db.load(DB_FOLDER)

    documents = db.documents

else:

    print("PDF'ler ilk kez işleniyor...")

    documents = read_all_pdfs(PDF_FOLDER)

    print(f"Toplam parça: {len(documents)}")

    embeddings = []

    for doc in documents:

        embeddings.append(
            get_embedding(doc["text"])
        )

    db.add(
        embeddings,
        documents
    )

    db.save(DB_FOLDER)

    print("Veritabanı hazır.")


# ==========================================================
# BM25
# ==========================================================

bm25.build(documents)


print("\nLocal RAG hazır.\n")


# ==========================================================
# SORU - CEVAP
# ==========================================================

while True:

    question = input("Soru : ").strip()

    if question.lower() in [
        "çık",
        "exit",
        "quit"
    ]:

        print("Program sonlandırıldı.")
        break

    if not question:
        continue


    # ======================================================
    # EMBEDDING SEARCH
    # ======================================================

    question_embedding = get_embedding(question)

    vector_results = db.search(
        question_embedding,
        k=SEARCH_K,
        threshold=0.40
    )


    # ======================================================
    # BM25 SEARCH
    # ======================================================

    bm25_results = bm25.search(
        question,
        top_k=SEARCH_K
    )


    # ======================================================
    # SONUÇLARI BİRLEŞTİR
    # ======================================================

    merged = []

    seen = set()

    for doc in vector_results + bm25_results:

        key = (
            doc["pdf"],
            doc["page"],
            doc["text"]
        )

        if key in seen:
            continue

        seen.add(key)

        merged.append(doc)


    # ======================================================
    # SONUÇ YOK
    # ======================================================

    if not merged:

        print("\nCevap bulunamadı.\n")
        continue


    # ======================================================
    # RERANK
    # ======================================================

    results = rerank(
        question,
        merged,
        top_k=FINAL_K
    )




    # ======================================================
    # CONTEXT
    # ======================================================

    context_parts = []

    seen_context = set()

    for doc in results:

        key = (
            doc["pdf"],
            doc["page"],
            doc["text"]
        )

        if key in seen_context:
            continue

        seen_context.add(key)

        context_parts.append(
            f"""
Başlık:
{doc.get("title", "")}

Kaynak:
{doc["pdf"]} - Sayfa {doc["page"]}

İçerik:
{doc["text"]}
"""
        )


    context = "\n".join(context_parts)


    # ======================================================
    # LLM
    # ======================================================

    answer = ask_llm(
        context,
        question
    )

    # ======================================================
    # EKRANA SADECE CEVAP
    # ======================================================

    print("\n" + "=" * 70)
    print("CEVAP")
    print("=" * 70)
    print(answer)

    # ======================================================
    # KAYNAKLAR (Akıllı Gösterim)
    # ======================================================
    
    # Eğer model cevabı metinlerde bulamadıysa, kaynak yazdırma!
    if "BİLGİ BULUNAMADI" not in answer.upper():
        print("\nKaynaklar:")

        shown = set()

        for doc in results:

            key = (
                doc["pdf"],
                doc["page"]
            )

            if key in shown:
                continue

            shown.add(key)

            print(
                f"• {doc['pdf']} | Sayfa {doc['page']}"
            )

    print("=" * 70)
    print()