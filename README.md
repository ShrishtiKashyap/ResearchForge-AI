# 🔬 ResearchForge-AI

An AI-powered multi-agent research assistant built using LangChain, Ollama, Tavily Search, BeautifulSoup, and Streamlit.

## Features

*  Searches the web for information
*  Scrapes relevant webpage content
*  Generates concise research reports
*  Reviews reports using a critic agent
*  Interactive Streamlit dashboard

## Tech Stack

* Python
* LangChain
* Ollama (Qwen3:4B)
* Tavily API
* BeautifulSoup
* Streamlit

## Project Architecture

User Topic

↓

Search Agent

↓

Reader Agent

↓

Writer Agent

↓

Critic Agent

↓

Final Report

## Project Structure

```text
ResearchForge-AI/
│
├── assets/
├── app.py
├── agents.py
├── pipeline.py
├── tools.py
├── requirements.txt
├── README.md
├── .gitignore
└── .env
```

## Setup

### Clone repository

```bash
git clone <your-repository-link>
```

### Create virtual environment

```bash
python -m venv .venv
```

### Activate virtual environment

Windows:

```bash
.\.venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run application

```bash
python -m streamlit run app.py
```

## Screenshots

Add screenshots inside `/assets`.

## Future Improvements

* Faster parallel execution
* Better source citations
* Export to PDF
* Agent memory support
* More advanced UI
