from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()


# ----------------------------
# SAFE TAVILY INIT
# ----------------------------

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if TAVILY_API_KEY:
    tavily = TavilyClient(api_key=TAVILY_API_KEY)
else:
    tavily = None


# ----------------------------
# WEB SEARCH TOOL
# ----------------------------

@tool
def web_search(query: str) -> str:
    """
    Search the web for recent and reliable information.
    Returns titles, URLs and snippets.
    """

    if not tavily:
        return "❌ Tavily API key missing. Add TAVILY_API_KEY in environment variables."

    try:
        results = tavily.search(
            query=query,
            max_results=5
        )

        output = []

        for r in results.get("results", []):
            output.append(
                f"Title: {r.get('title','')}\n"
                f"URL: {r.get('url','')}\n"
                f"Snippet: {r.get('content','')[:300]}\n"
            )

        return "\n-----\n".join(output)

    except Exception as e:
        return f"Web search failed: {e}"


# ----------------------------
# SCRAPER TOOL
# ----------------------------

@tool
def scrape_url(url: str) -> str:
    """
    Scrape and return clean text content from a URL.
    """

    try:
        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        soup = BeautifulSoup(response.text, "html.parser")

        # remove unwanted tags
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)

        return text[:1500]

    except Exception as e:
        return f"Could not scrape URL: {e}"