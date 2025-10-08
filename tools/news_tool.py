# tools/news_tool.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("NEWS_API_KEY")

def get_latest_news(topic: str) -> str:
    """
    Fetches the top 5 latest news headlines from India using the GNews API.
    """
    if not API_KEY:
        return "Error: News API key is not configured."

    # This is the new URL for the GNews API
    url = f"https://gnews.io/api/v4/top-headlines?country=in&lang=en&max=5&apikey={API_KEY}"

    # For GNews, we can add the topic as a keyword if it's not generic
    generic_terms = ["news", "latest news", "latest", "headlines", "top news", "india", "bharat"]
    if topic.lower().strip() not in generic_terms:
        url += f"&q={topic}"

    print(f"DEBUG: Calling GNews API with URL: {url}")

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if data.get("totalArticles") > 0 and data.get("articles"):
            headlines = []
            for article in data["articles"]:
                # GNews has a different structure for the source name
                source_name = article['source']['name']
                headlines.append(f"- {article['title']} ({source_name})")
            
            return "Here are the top headlines from India:\n" + "\n".join(headlines)
        else:
            return f"Sorry, I couldn't find any recent news on '{topic}' from India."
            
    except Exception as e:
        return f"Sorry, an error occurred while fetching the news: {e}"