import os
import faiss
import pickle
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader

model = SentenceTransformer("all-MiniLM-L6-v2")

texts = []
sources = []

knowledge_path = "knowledge"

for file in os.listdir(knowledge_path):
    file_path = os.path.join(knowledge_path, file)

    if file.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            texts.append(f.read())
            sources.append(file)

    elif file.endswith(".pdf"):
        reader = PdfReader(file_path)
        pdf_text = ""
        for page in reader.pages:
            pdf_text += page.extract_text() + "\n"
        texts.append(pdf_text)
        sources.append(file)

embeddings = model.encode(texts)

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

faiss.write_index(index, "memory.index")

with open("memory.pkl", "wb") as f:
    pickle.dump((texts, sources), f)

print("✅ Memory rebuilt with TXT and PDF files!")
