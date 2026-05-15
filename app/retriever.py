import json
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer


# -----------------------------
# Load Embedding Model
# -----------------------------

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


# -----------------------------
# Load SHL Catalog
# -----------------------------

with open(
    "app/data/assessments.json",
    "r",
    encoding="utf-8"
) as f:

    raw_assessments = json.load(f)


# -----------------------------
# Remove Job Solutions
# -----------------------------

assessments = []

for item in raw_assessments:

    name = item.get("name", "")

    if "Solution" in name:
        continue

    assessments.append(item)


print(f"Loaded {len(assessments)} individual assessments")


# -----------------------------
# Prepare Documents
# -----------------------------

documents = []

for item in assessments:

    text = f"""
    Name: {item.get('name', '')}

    Description:
    {item.get('description', '')}

    Job Levels:
    {' '.join(item.get('job_levels', []))}

    Categories:
    {' '.join(item.get('keys', []))}
    """

    documents.append(text)


# -----------------------------
# Generate Embeddings
# -----------------------------

print("Generating embeddings...")

embeddings = model.encode(
    documents,
    show_progress_bar=True
)


embeddings = np.array(
    embeddings
).astype("float32")


# -----------------------------
# Create FAISS Index
# -----------------------------

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

print(f"\nIndexed {len(documents)} assessments")


# -----------------------------
# Search Function
# -----------------------------

def search_assessments(query, top_k=5):

    query_embedding = model.encode([query])

    query_embedding = np.array(
        query_embedding
    ).astype("float32")


    distances, indices = index.search(
        query_embedding,
        top_k
    )


    results = []

    for idx in indices[0]:

        results.append(assessments[idx])


    return results


# -----------------------------
# Test Retrieval
# -----------------------------

if __name__ == "__main__":

    query = "Java backend developer with communication skills"

    results = search_assessments(query)

    print("\nTop Matches:\n")


    for item in results:

        print("=" * 50)

        print("Name:", item.get("name"))

        print("URL:", item.get("url"))

        print("Description:", item.get("description"))

        print()