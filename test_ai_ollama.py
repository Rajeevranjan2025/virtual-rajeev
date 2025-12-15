import ollama

print("✅ Virtual Rajeev is ready (Ollama)!")
print("Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {"role": "system", "content": "You are Virtual Rajeev, a helpful personal AI assistant."},
            {"role": "user", "content": user_input}
        ]
    )

    print("Virtual Rajeev:", response["message"]["content"])
