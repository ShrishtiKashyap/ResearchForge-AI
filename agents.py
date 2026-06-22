from langchain_ollama import ChatOllama

from tools import web_search, scrape_url

from dotenv import load_dotenv

load_dotenv()

llm = ChatOllama(
    model="qwen3:4b",
    temperature=0,
)


# SEARCH

def build_search_agent(topic):

    return web_search.invoke(topic)


# SCRAPER

def build_reader_agent(url):

    return scrape_url.invoke(url)


# WRITER

def writer_agent(topic, research):

    prompt = f"""
/no_think

You are an expert research writer.

Write a concise research report.

Topic:
{topic}

Research:
{research}

Structure:

Introduction

3 Key Findings

Conclusion

Sources

Keep it under 400 words.
"""

    response = llm.invoke(prompt)

    return response.content


# CRITIC

def critic_agent(report):

    prompt = f"""
/no_think

You are a research reviewer.

Review this report.

{report}

Respond exactly as:

Score: X/10

Strengths:
- ...

Areas to Improve:
- ...

Verdict:
...
"""

    response = llm.invoke(prompt)

    return response.content