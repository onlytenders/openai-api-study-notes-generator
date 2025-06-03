# scripts/00_bootstrap.py
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def create_assistant():
    # Create the assistant
    assistant = client.beta.assistants.create(
        name="Study QnA Assistant",
        instructions=(
            "You are a helpful assistant that can answer questions and help with tasks. "
            "You are given a question and a context. You need to answer the question based on the context. "
            "If you don't know the answer, you should say so. "
            "You should use the tools provided to you to answer the question."
        ),
        tools=[{"type": "file_search"}],
        model="gpt-4-turbo-preview",
    )
    print(f"Assistant created with ID: {assistant.id}")

    # Create vector store
    vector_store = client.vector_stores.create(name="Study QnA Vector Store")
    print(f"Vector store created with ID: {vector_store.id}")

    # Upload file
    file_batch = client.files.create(
        file=open("data/bitcoin.pdf", "rb"),
        purpose="assistants"
    )

    # Update assistant with file
    client.beta.assistants.update(
        assistant_id=assistant.id,
        tool_resources={
            "file_search": {
                "vector_store_ids": [vector_store.id]
            }
        }
    )

    # Save assistant ID to .env file
    with open(".env", "a") as f:
        f.write(f"\nASSISTANT_ID={assistant.id}")
    print("\n✅ Assistant ID saved to .env file")

    return assistant.id, vector_store.id

if __name__ == "__main__":
    assistant_id, vector_store_id = create_assistant()
    # Save IDs for reuse (e.g., in a file or environment variable)
    with open("assistant_config.txt", "w") as f:
        f.write(f"ASSISTANT_ID={assistant_id}\nVECTOR_STORE_ID={vector_store_id}")