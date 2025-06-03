# scripts/02_generate_notes.py
import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List
import time

# Define the schema for structured output
class Note(BaseModel):
    heading: str = Field(..., description="The heading of the note")
    summary: str = Field(..., description="A concise summary of the topic (max 150 chars)")
    page_reference: str | None = Field(None, description="The page reference where this information can be found")

class NotesResponse(BaseModel):
    notes: List[Note] = Field(..., description="List of 10 study notes")

def generate_notes():
    # Load environment variables
    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    try:
        # Create a thread with the initial message
        thread = client.beta.threads.create(
            messages=[{
                "role": "user",
                "content": (
                    "Generate exactly 10 unique revision notes from the provided document. "
                    "Each note should have a heading, summary (max 150 chars), and page_reference. "
                    "Format the response as a JSON object with a 'notes' array containing objects with "
                    "'heading', 'summary', and 'page_reference' fields."
                )
            }]
        )

        # Create a run with structured output
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=os.getenv("ASSISTANT_ID"),
            instructions="Generate exactly 10 study notes in JSON format with heading, summary, and page_reference fields.",
            tools=[],
            model="gpt-4-turbo-preview",
            response_format={"type": "json_object"}
        )

        # Wait for the run to complete
        while True:
            run_status = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            if run_status.status == 'completed':
                break
            elif run_status.status in ['failed', 'cancelled', 'expired']:
                print(f"Run failed with status: {run_status.status}")
                return None
            time.sleep(1)

        # Get the response
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        response_content = messages.data[0].content[0].text.value
        
        # Parse the JSON response
        try:
            notes_data = json.loads(response_content)
            notes_response = NotesResponse(**notes_data)
            return notes_response.notes
        except Exception as e:
            print(f"Error parsing response: {e}")
            print(f"Raw response: {response_content}")
            return None

    except Exception as e:
        print(f"Error in generate_notes: {e}")
        return None

def save_notes(notes):
    if not notes:
        return
        
    try:
        # Save to JSON file
        with open("exam_notes.json", "w") as f:
            json.dump([note.model_dump() for note in notes], f, indent=2)
        
        # Print notes in a readable format
        print("\n📚 Generated Study Notes:\n")
        for i, note in enumerate(notes, 1):
            print(f"📝 Note {i}: {note.heading}")
            print(f"📌 Summary: {note.summary}")
            print(f"📄 Page Ref: {note.page_reference or 'N/A'}")
            print("-" * 60)
            
    except Exception as e:
        print(f"Error saving notes: {e}")

if __name__ == "__main__":
    print("🤖 Generating study notes...")
    notes = generate_notes()
    if notes:
        save_notes(notes)
        print("\n✅ Notes have been saved to exam_notes.json")
    else:
        print("\n❌ Failed to generate notes")