# split text into chunks of max_tokens
# helper function to split text into chunks of max_tokens
def split_text(text, max_tokens=200):
    sentences = text.split(". ")
    chunks = []
    chunk = ""

    for sentence in sentences:
        if len(chunk + sentence) > max_tokens:
            chunks.append(chunk.strip())
            chunk = sentence + ". "
        else:
            chunk += sentence + ". "

    if chunk:
        chunks.append(chunk.strip())

    return chunks
