def chunk_text(text, chunk_size=500, overlap=100):
    """
    Metni belirli boyutlarda parçalara ayırır.
    overlap sayesinde parçalar arasında ortak alan bırakılır.
    """

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks