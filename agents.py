import os
import requests
from tools import web_search, scrape_url
from dotenv import load_dotenv
load_dotenv()


# ----------------------------
# SAFE LLM CALL (CLOUD READY)
# ----------------------------

def call_llm(prompt):
    import os
    import requests

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return "❌ Missing GROQ_API_KEY"

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama3-8b-8192",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0
            },
            timeout=30
        )

        data = response.json()

        # 🔥 SAFE CHECKS (THIS FIXES YOUR ERROR)
        if "choices" not in data:
            return f"❌ Groq API error: {data}"

        return data["choices"][0]["message"]["content"]

    except Exception as e:
        return f"❌ Groq API failed: {str(e)}"


# ----------------------------
# SEARCH AGENT
# ----------------------------

def build_search_agent(topic):
    return web_search.invoke(topic)


# ----------------------------
# SCRAPER AGENT
# ----------------------------

def build_reader_agent(url):
    return scrape_url.invoke(url)


# ----------------------------
# WRITER AGENT
# ----------------------------

def writer_agent(topic, research):

    prompt = f"""
You are an expert research writer.

Write a concise research report.

Topic:
{topic}

Research:
{research}

Structure:
- Introduction
- 3 Key Findings
- Conclusion
- Sources

Keep it under 400 words.
"""

    return call_llm(prompt)


# ----------------------------
# CRITIC AGENT
# ----------------------------

def critic_agent(report):

    prompt = f"""
You are a research reviewer.

Review this report:

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

    return call_llm(prompt)


