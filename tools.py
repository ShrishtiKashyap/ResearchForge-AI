from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()

tavily = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


@tool
def web_search(query: str) -> str:
    """
    Search the web for recent and reliable information.
    Returns titles, URLs and snippets.
    """

    try:

        results = tavily.search(
            query=query,
            max_results=5
        )

        output = []

        for r in results["results"]:

            output.append(
                f"Title: {r['title']}\n"
                f"URL: {r['url']}\n"
                f"Snippet: {r['content'][:300]}\n"
            )

        return "\n-----\n".join(output)

    except Exception as e:

        return f"Web search failed: {e}"


@tool
def scrape_url(url: str) -> str:
    """
    Scrape and return clean text content from a URL.
    """

    try:

        response = requests.get(
            url,
            timeout=8,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        for tag in soup(
            ["script", "style", "nav", "footer"]
        ):
            tag.decompose()

        return soup.get_text(
            separator=" ",
            strip=True
        )[:1000]

    except Exception as e:

        return f"Could not scrape URL: {e}"