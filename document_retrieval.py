import re


STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "how",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "this",
    "to",
    "what",
    "when",
    "where",
    "which",
    "with",
}


CHUNK_WORDS = 180
CHUNK_OVERLAP = 30
TOP_CHUNKS = 4


def normalise_terms(text):

    words = re.findall(
        r"[A-Za-z0-9_]+",
        text.lower()
    )

    return {
        word
        for word in words
        if len(word) > 2
        and word not in STOP_WORDS
    }


def chunk_document(document):

    words = document["text"].split()

    chunks = []

    start = 0
    chunk_number = 1

    while start < len(words):

        end = start + CHUNK_WORDS

        chunk_words = words[start:end]

        if chunk_words:

            chunks.append(
                {
                    "source": document["name"],
                    "chunk_number": chunk_number,
                    "text": " ".join(
                        chunk_words
                    ),
                }
            )

        if end >= len(words):
            break

        start = end - CHUNK_OVERLAP
        chunk_number += 1

    return chunks


def build_chunks(documents):

    all_chunks = []

    for document in documents:
        all_chunks.extend(
            chunk_document(document)
        )

    return all_chunks


def score_chunk(question, chunk_text):

    question_terms = normalise_terms(
        question
    )

    chunk_terms = normalise_terms(
        chunk_text
    )

    return len(
        question_terms.intersection(
            chunk_terms
        )
    )


def retrieve_relevant_chunks(
    question,
    documents
):

    scored_chunks = []

    for chunk in build_chunks(documents):

        score = score_chunk(
            question,
            chunk["text"]
        )

        if score > 0:

            chunk_with_score = (
                chunk.copy()
            )

            chunk_with_score[
                "score"
            ] = score

            scored_chunks.append(
                chunk_with_score
            )

    scored_chunks.sort(
        key=lambda item: (
            -item["score"],
            item["source"],
            item["chunk_number"],
        )
    )

    return scored_chunks[
        :TOP_CHUNKS
    ]


def build_context(chunks):

    context_parts = []

    for chunk in chunks:

        context_parts.append(
            (
                f"SOURCE: {chunk['source']}\n"
                f"CHUNK: {chunk['chunk_number']}\n"
                f"{chunk['text']}"
            )
        )

    return "\n\n---\n\n".join(
        context_parts
    )


def build_grounded_prompt(
    question,
    chunks
):

    if chunks:

        context = build_context(
            chunks
        )

    else:

        context = (
            "No relevant passage was retrieved "
            "from the supplied documents."
        )

    return f"""
You are answering an engineering question for an academic research experiment.

Use only the supplied document context below.

Do not use outside knowledge to add technical facts that are not supported by the supplied context.

If the answer cannot be found in the supplied context, state clearly:
"The information is not available in the provided documentation."

Keep the answer focused on the question.

DOCUMENT CONTEXT:

{context}

QUESTION:

{question}
""".strip()


def source_names(chunks):

    names = []

    for chunk in chunks:

        if chunk["source"] not in names:
            names.append(
                chunk["source"]
            )

    return names
