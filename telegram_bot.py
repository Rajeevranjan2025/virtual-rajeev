import faiss
import pickle
import ollama
from sentence_transformers import SentenceTransformer
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# ===============================
# LOAD MEMORY
# ===============================
index = faiss.read_index("memory.index")

with open("memory.pkl", "rb") as f:
    texts, sources = pickle.load(f)

embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# ===============================
# BOT HANDLER
# ===============================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_query = update.message.text
    original_query = user_query.lower()

    # 🔒 PRIVACY PROTECTION
    SENSITIVE = ["mobile", "phone", "number", "email", "contact", "address"]
    if any(word in original_query for word in SENSITIVE):
        await update.message.reply_text(
            "I cannot share personal contact details for privacy reasons."
        )
        return

    # 🎯 QUERY-AWARE ROUTING
    ROUTING_HINTS = {
        "skill": "technical skills",
        "experience": "work experience",
        "project": "projects",
        "education": "education",
        "resume": "resume summary",
        "language": "programming languages",
    }

    search_query = user_query
    for key, hint in ROUTING_HINTS.items():
        if key in original_query:
            search_query = hint
            break

    # 🔍 EMBEDDING + SEARCH
    query_embedding = embed_model.encode([search_query])
    distances, indices = index.search(query_embedding, k=5)

    context_text = "\n\n".join([texts[i] for i in indices[0]])

    # 🧠 STRICT CONTEXT ANSWERING
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
                "content": f"Context:\n{context_text}"
            },
            {
                "role": "user",
                "content": user_query
            }
        ]
    )

    await update.message.reply_text(response["message"]["content"])

# ===============================
# MAIN
# ===============================
def main():
    BOT_TOKEN = "8351870703:AAFOzLMa6avZKDGGJxfguRr9CHhtX1AQ4SM"

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Virtual Rajeev Telegram Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
