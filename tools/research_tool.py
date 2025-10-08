import os
from serpapi import GoogleSearch
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("SERPAPI_KEY")

def deep_research(topic: str) -> str:
    """
    Searches Google for a given topic and returns the top 5 search result snippets.
    Use this tool to find information about any real-world topic, event, or place.
    """
    if not API_KEY:
        return "Error: Search API key is not configured."

    params = { "engine": "google", "q": topic, "api_key": API_KEY, "num": 5 }

    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        
        search_snippets = []
        if "organic_results" in results:
            for result in results.get("organic_results", []):
                snippet = f"Title: {result.get('title')}\nSummary: {result.get('snippet')}\n---"
                search_snippets.append(snippet)
        
        if not search_snippets:
            return f"Sorry, I couldn't find any information on '{topic}'."
        
        return "\n".join(search_snippets)

    except Exception as e:
        return f"Sorry, an error occurred during the research: {e}"

