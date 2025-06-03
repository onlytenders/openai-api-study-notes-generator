from openai import OpenAI
from dotenv import load_dotenv
import os

def cleanup():
    print("🧹 Starting cleanup process...")
    
    # Load environment variables
    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Get IDs from .env file
    assistant_id = os.getenv("ASSISTANT_ID")
    
    try:
        # Delete assistant if it exists
        if assistant_id:
            try:
                client.beta.assistants.delete(assistant_id=assistant_id)
                print(f"✅ Assistant {assistant_id} deleted successfully")
            except Exception as e:
                print(f"⚠️ Error deleting assistant: {e}")
        
        # List and delete all files
        try:
            files = client.files.list()
            for file in files.data:
                client.files.delete(file_id=file.id)
                print(f"✅ File {file.id} deleted successfully")
        except Exception as e:
            print(f"⚠️ Error deleting files: {e}")
        
        # List and delete all vector stores
        try:
            vector_stores = client.vector_stores.list()
            for store in vector_stores.data:
                client.vector_stores.delete(vector_store_id=store.id)
                print(f"✅ Vector store {store.id} deleted successfully")
        except Exception as e:
            print(f"⚠️ Error deleting vector stores: {e}")
        
        # Clean up local files
        local_files = ['exam_notes.json']
        for file in local_files:
            if os.path.exists(file):
                os.remove(file)
                print(f"✅ Local file {file} deleted successfully")
        
        # Clean up .env file - remove ASSISTANT_ID
        if os.path.exists(".env"):
            with open(".env", "r") as f:
                lines = f.readlines()
            with open(".env", "w") as f:
                for line in lines:
                    if not line.startswith("ASSISTANT_ID="):
                        f.write(line)
            print("✅ Removed ASSISTANT_ID from .env file")
            
        print("\n🎉 Cleanup completed successfully!")
        
    except Exception as e:
        print(f"\n❌ An error occurred during cleanup: {e}")

if __name__ == "__main__":
    cleanup()
