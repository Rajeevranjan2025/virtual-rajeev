import faiss
import pickle
import ollama
from sentence_transformers import SentenceTransformer

# ===============================
# LOAD MEMORY (FAISS + TEXT)
# ===============================
index = faiss.read_index("memory.index")

with open("memory.pkl", "rb") as f:
    texts, sources = pickle.load(f)

embed_model = SentenceTransformer("all-MiniLM-L6-v2")

print("🧠 Virtual Rajeev with RAG is ready!")
print("Type 'exit' to quit.\n")

# ===============================
# CHAT LOOP
# ===============================
while True:
    query = input("You: ")

    if query.lower() == "exit":
        break

    original_query = query.lower()

    # ===============================
    # 🔒 PRIVACY PROTECTION
    # ===============================
    SENSITIVE_KEYWORDS = [
        "mobile", "phone", "number", "email", "contact", "address"
    ]

    if any(word in original_query for word in SENSITIVE_KEYWORDS):
        print("Virtual Rajeev: I cannot share personal contact details for privacy reasons.")
        continue

    # ===============================
    # 🎯 QUERY-AWARE ROUTING (HELP RAG)
    # ===============================
    ROUTING_HINTS = {
        "skill": "technical skills",
        "experience": "work experience",
        "project": "projects",
        "education": "education",
        "resume": "resume summary",
        "language": "programming languages",
    }

    search_query = query
    for key, hint in ROUTING_HINTS.items():
        if key in original_query:
            search_query = hint
            break

    # ===============================
    # 🔍 EMBEDDING + SEARCH
    # ===============================
    query_embedding = embed_model.encode([search_query])
    distances, indices = index.search(query_embedding, k=3)

    # Combine retrieved contexts
    context = "\n\n".join([texts[i] for i in indices[0]])

    # ===============================
    # 🧠 STRICT CONTEXT ANSWERING
    # ===============================
    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are Virtual Rajeev, a personal AI assistant.\n"
                    "Answer ONLY using the information provided in the context below.\n"
                    "Do NOT add any information from your own knowledge.\n"
                    "If the answer is not explicitly present in the context, reply exactly with:\n"
                    "'This information is not mentioned in the provided data.'"
                )
            },
            {
                "role": "system",
                "content": f"Context:\n{context}"
            },
            {
                "role": "user",
                "content": query
            }
        ]
    )

    print("Virtual Rajeev:", response["message"]["content"])
