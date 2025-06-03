# scripts/01_qna_assistant.py
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables and assistant config
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load assistant ID from config
with open("assistant_config.txt", "r") as f:
    config = dict(line.strip().split("=") for line in f)
    assistant_id = config["ASSISTANT_ID"]

def ask_question(question):
    # Create a thread
    thread = client.beta.threads.create()
    
    # Add user message
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=question
    )
    
    # Stream the assistant's response
    with client.beta.threads.runs.stream(
        thread_id=thread.id,
        assistant_id=assistant_id
    ) as stream:
        print(f"Question: {question}")
        print("Answer:")
        for event in stream:
            if event.event == "thread.message.delta":
                for delta in event.data.delta.content:
                    if delta.type == "text":
                        print(delta.text.value, end="", flush=True)
        print("\nCitations:")
        # Retrieve final messages to check citations
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        for message in messages:
            if message.role == "assistant":
                for content_block in message.content:
                    if hasattr(content_block, "citations"):
                        for citation in content_block.citations:
                            print(f"- {citation.text} (File ID: {citation.file_id})")

# Test questions
questions = [
    "Explain, what is bitcoin?",
    "What is the price of bitcoin today?"
]

if __name__ == "__main__":
    for question in questions:
        ask_question(question)
        print("\n" + "="*50 + "\n")