import json
from txtai import Embeddings

# Load the JSON data that was used for indexing.
with open("transcriptions-no-cut.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Prepare the documents for indexing.
# Each document is a tuple: (id, combined text, metadata)
# We store metadata as a JSON string to avoid SQLite binding issues.
documents = []
for key, value in data.items():
    file_title = value.get("file_title", "")
    transcription = value.get("transcription", "")
    combined_text = f"File Title: {file_title}\nTranscription: {transcription}"
    metadata = json.dumps({"file_title": file_title, "transcription": transcription})
    documents.append((key, combined_text, metadata))

# Create an embeddings instance using hybrid search.
# (Use the same model as for indexing; here, we use BGE-M3.)
embeddings = Embeddings(hybrid=True, path="BAAI/bge-m3")

# Create an index for the documents.
embeddings.index(documents)

# Ask the user for hybrid search parameters.
alpha = float(input("Enter alpha parameter for hybrid search (e.g., 0.5): "))
limit = int(input("Enter the number of relative documents to retrieve: "))

print("\n%-20s %-50s" % ("Query", "Results"))
print("-" * 70)

# Interactive query loop.
while True:
    query = input("\nEnter your search query (or type 'exit' to quit): ")
    if query.lower() == "exit":
        break

    # Run a hybrid search using the user-specified alpha and limit.
    # The search returns a list of tuples: (uid, score)
    results = embeddings.search(query, limit, weights=alpha)

    print(f"\nQuery: {query}\n")
    for uid, score in results:
        # Retrieve original file metadata from the data dictionary.
        item = data.get(uid, {})
        file_title = item.get("file_title", "N/A")
        transcription = item.get("transcription", "N/A")
        print(f"File Title   : {file_title}")
        print(f"Transcription: {transcription}")
        print(f"Score        : {score:.4f}")
        print("-" * 70)
