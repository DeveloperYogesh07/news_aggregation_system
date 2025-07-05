import httpx
from typing import List, Dict
from app.external.base_news_client import BaseNewsClient
from app.core.config import settings
import json

class NewsAPIClient(BaseNewsClient):
    BASE_URL = "https://newsapi.org/v2/top-headlines"
    API_KEY = "08999c2c0fb44ff29c4352f27d402246" 

    def fetch_top_headlines(self, category: str = None) -> List[Dict]:
        params = {
            "apiKey": self.API_KEY,
            "country": "us",
            "pageSize": 10,
            "category": category
        }

        response = httpx.get(self.BASE_URL, params=params)
        response.raise_for_status()

        # with open("newsapi_raw_response.json", "w") as f:
        #     json.dump(response.json(), f, indent=2)

        articles = response.json().get("articles", [])
        results = []
        for article in articles:
            results.append({
                "title": article.get("title"),
                "content": article.get("description"),
                "url": article.get("url"),
                "category": category
            })
        return results
