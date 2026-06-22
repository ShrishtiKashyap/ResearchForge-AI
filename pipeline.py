from agents import (
    build_reader_agent,
    build_search_agent,
    writer_agent,
    critic_agent
)

from rich import print

import re


def run_research_pipeline(topic):

    state = {}

    # STEP 1

    print("\n" + "="*50)

    print("STEP 1 - Searching...")

    print("="*50)

    state["search_results"] = build_search_agent(topic)

    print(state["search_results"])

    # STEP 2

    print("\n" + "="*50)

    print("STEP 2 - Scraping...")

    print("="*50)

    urls = re.findall(

        r"https?://[^\s]+",

        state["search_results"]

    )

    if urls:

        url = urls[0]

        scraped = build_reader_agent(url)

        if "403" in scraped:

            scraped = "Website blocked scraping."

        state["scraped_content"] = scraped

    else:

        state["scraped_content"] = "No URL found."

    state["search_results"] = state["search_results"][:700]

    state["scraped_content"] = state["scraped_content"][:900]

    print(state["scraped_content"])

    # STEP 3

    print("\n" + "="*50)

    print("STEP 3 - Writing report...")

    print("="*50)

    research = f"""

SEARCH RESULTS

{state['search_results']}

SCRAPED CONTENT

{state['scraped_content']}

"""

    state["report"] = writer_agent(

        topic,

        research

    )

    print("\nREPORT\n")

    print(state["report"])

    # STEP 4

    print("\n" + "="*50)

    print("STEP 4 - Critiquing...")

    print("="*50)

    state["feedback"] = critic_agent(

        state["report"]

    )

    print("\nFEEDBACK\n")

    print(state["feedback"])

    return state


if __name__ == "__main__":

    topic = input(

        "Enter a research topic: "

    )

    run_research_pipeline(topic)