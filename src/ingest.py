import os
import re

from pypdf import PdfReader

from settings import CHUNK_SIZE, CHUNK_OVERLAP


def read_all_pdfs(folder):

    documents = []

    for file in os.listdir(folder):

        if not file.lower().endswith(".pdf"):
            continue

        print(f"Okunuyor: {file}")

        pdf_path = os.path.join(folder, file)

        reader = PdfReader(pdf_path)

        for page_number, page in enumerate(reader.pages, start=1):

            text = page.extract_text()

            if not text:
                continue

            text = clean_text(text)

            chunks = chunk_text(text)

            for chunk in chunks:

                lines = chunk.split("\n")

                title = lines[0].strip()

                documents.append(
                    {
                        "title": title,
                        "text": chunk,
                        "pdf": file,
                        "page": page_number
                    }
                )

    return documents


# -------------------------------------------------------


def clean_text(text):

    text = text.replace("\r", "\n")

    text = re.sub(r"\n{2,}", "\n", text)

    text = re.sub(r"[ \t]+", " ", text)

    text = re.sub(r"-\n", "", text)

    text = re.sub(r"\n(?=[a-zçğıöşü])", " ", text, flags=re.IGNORECASE)

    return text.strip()


# -------------------------------------------------------


def chunk_text(text):

    paragraphs = [
        p.strip()
        for p in text.split("\n")
        if p.strip()
    ]

    if not paragraphs:
        return []

    title = paragraphs[0]

    chunks = []

    current = title + "\n"

    for paragraph in paragraphs[1:]:

        if len(current) + len(paragraph) <= CHUNK_SIZE:

            current += paragraph + "\n"

        else:

            if len(current.strip()) > 150:
                chunks.append(current.strip())

            overlap = current[-CHUNK_OVERLAP:]

            current = (
                title
                + "\n"
                + overlap
                + "\n"
                + paragraph
                + "\n"
            )

    if len(current.strip()) > 150:
        chunks.append(current.strip())

    return chunks