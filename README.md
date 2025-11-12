# News Summarizer

An agentic pipeline that fetches the latest articles for a query and returns a concise, source-cited summary—plus a structured JSON output that your apps can consume.

## Prerequisites

- Python 3.12 or higher
- uv
- API keys for:
  - OpenAI


## Installation

1. Clone the repository:
```bash
git clone https://github.com/Pranavisriya/news-summarizer.git
cd news-summarizer
```

2. Install `uv` in the environment if it is not present
```bash
pip install uv
```

3. Create a virtual python environment in this repo
```bash
uv init
uv venv -p 3.12
```

Any other method can also be used to create python environment.

4. Activate python environment
```bash
source .venv/bin/activate
```


5. Install dependencies using uv:
```bash
uv add -r requirements.txt
```

6. Create a `.env` file in the project root with your API keys:
```
OPEN_API_KEY=your_openaiapi_key
NEWSAPI_KEY=your_newsapi_key
TAVILY_API_KEY=your_tavilyapi_key
```

## Usage

Run the fastapi and frontend:
```bash
uvicorn main:app --reload --port 8000
streamlit run frontend.py
```


## Features

- Latest-aware search (NewsAPI/Tavily)
- Factual, compact summaries with explicit dates when available
- Structured JSON output for easy integration
- Source citations (domains + links)
- Session memory (optional) via LangGraph’s in-memory checkpointing
- FastAPI + Streamlit for quick local testing and demos
  
## License

This project is licensed under the terms included in the LICENSE file.

## Author

Pranavi Sriya (pranavisriyavajha9@gmail.com)



