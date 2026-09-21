"""
Stage 2 of the pipeline: splitting documents into chunks.

⚠️ THIS IS THE FILE YOU CHANGE IN MILESTONE 3.

`split_documents` below is deliberately plain. It cuts every document into
fixed-size pieces with a fixed overlap and pays no attention to where sentences
or paragraphs end. It works, and it is not good.

On a corpus of short posts it may not cut anything at all: `campus_life` comes
out as 88 documents and 88 chunks, because almost nothing in it reaches 800
characters. That is the baseline, not a bug — Milestone 3 is where you decide
whether one post should stay one chunk.

Your job in Milestone 3 is to replace the *body* of `split_documents` with a
strategy that fits the documents you actually read in Milestone 1. Keep the
name and the shape of what it returns — the rest of the pipeline calls it, and
your README has to name the function that produced your chunks.

If you get stuck for 30 minutes, `fallback_split` is the original. Switch back
to it, write down what you saw, and move on. That's a real observation about
your pipeline, not giving up.
"""

from dataclasses import dataclass

import config
from ingest import Document


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


# Keep adding paragraphs to a chunk until its body reaches this many
# characters. Stops one-line paragraphs like "The good: closest building to the
# science quad" from becoming chunks on their own.
#
# I started at 200 and it was too high: a whole housing post came back as one
# chunk again, which is what I was trying to get away from. At 100 the laundry
# line gets its own chunk with the building name on it.
MIN_BODY = 100


def split_documents(documents: list[Document]) -> list[Chunk]:
    """
    Split on paragraphs, and repeat the title line in every chunk.

    Every post in campus_life is a title line, a blank line, then one to four
    short paragraphs. The title is the only place the name appears: the body of
    housing_morrow_house.txt says "$1.50 wash, $1.25 dry" but never says
    "Morrow House". A chunk without the title can't answer "how much is the
    dryer in Morrow House", so the title goes on the front of each chunk.

    Paragraphs shorter than MIN_BODY get joined with the next one, so I don't
    end up with a chunk that is only "The bad: the elevator is out roughly one
    week per semester."
    """
    chunks: list[Chunk] = []

    for doc in documents:
        paragraphs = [p.strip() for p in doc.text.split("\n\n") if p.strip()]
        if not paragraphs:
            continue

        title = paragraphs[0]
        bodies = paragraphs[1:]

        # A document with no body paragraphs is just its title — keep it whole.
        if not bodies:
            bodies = [title]

        grouped: list[str] = []
        current = ""
        for paragraph in bodies:
            current = f"{current}\n\n{paragraph}" if current else paragraph
            if len(current) >= MIN_BODY:
                grouped.append(current)
                current = ""

        # Whatever is left over is too short to stand alone, so it joins the
        # chunk before it rather than becoming a fragment.
        if current:
            if grouped:
                grouped[-1] = f"{grouped[-1]}\n\n{current}"
            else:
                grouped.append(current)

        for index, body in enumerate(grouped):
            text = body if body == title else f"{title}\n\n{body}"
            chunks.append(
                Chunk(
                    text=text,
                    source=doc.source,
                    index=index,
                    produced_by="chunker.py::split_documents",
                )
            )

    return chunks


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
