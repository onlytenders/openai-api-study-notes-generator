# 📚 AI Study Notes Generator

This project uses OpenAI's Assistant API to automatically generate structured study notes from PDF documents. Perfect for students and researchers who want to create quick, organized summaries of their study materials.

## 🌟 Features

- 🤖 Uses OpenAI's GPT-4 to analyze documents
- 📝 Generates 10 key study notes with headings and summaries
- 📍 Includes page references for easy lookup
- 🎯 Outputs clean, structured JSON format
- 🧹 Includes cleanup utilities for resource management

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- OpenAI API key
- PDF document(s) to analyze

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd ai_hw2
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:
```bash
OPENAI_API_KEY=your_api_key_here
```

### 📖 Usage

1. Place your PDF file in the `data/` directory

2. Run the bootstrap script to set up the assistant:
```bash
python scripts/00_bootstrap.py
```

3. Generate study notes:
```bash
python scripts/02_generate_notes.py
```

4. Find your generated notes in `exam_notes.json`

5. Clean up resources when done:
```bash
python scripts/99_cleanup.py
```

## 📁 Project Structure

```
.
├── data/               # Store your PDF files here
├── scripts/
│   ├── 00_bootstrap.py    # Sets up OpenAI assistant
│   ├── 02_generate_notes.py # Generates study notes
│   └── 99_cleanup.py      # Cleans up resources
├── requirements.txt    # Project dependencies
└── README.md          # This file
```

## 🛠️ Configuration

The project uses environment variables for configuration:
- `OPENAI_API_KEY`: Your OpenAI API key
- `ASSISTANT_ID`: Automatically set by bootstrap script

## 🧹 Cleanup

To remove all created resources and clean up your workspace:
```bash
python scripts/99_cleanup.py
```

This will:
- Delete the OpenAI assistant
- Remove uploaded files
- Delete vector stores
- Clean up local files
- Reset environment variables

## 📝 Note Format

Generated notes follow this structure:
```json
{
  "notes": [
    {
      "heading": "Topic Title",
      "summary": "Concise summary (max 150 chars)",
      "page_reference": "Page number"
    }
  ]
}
```

## ⚠️ Important Notes

- Keep your `.env` file secure and never commit it to version control
- Clean up resources when done to avoid unnecessary OpenAI API charges
- Make sure your PDF files are text-searchable for best results

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
