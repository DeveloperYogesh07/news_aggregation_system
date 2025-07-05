from typing import Optional


class CategoryClassifier:
    """
    A basic keyword-based news category classifier.
    Extendable to ML model later.
    """
    keyword_map = {
        "business": ["market", "stock", "economy", "trade", "invest", "revenue"],
        "sports": ["soccer", "tennis", "cricket", "NBA", "FIFA", "goal", "match"],
        "technology": ["AI", "artificial intelligence", "machine learning", "software", "hardware", "tech"],
        "entertainment": ["celebrity", "movie", "TV", "drama", "actor", "actress", "film", "music"],
        "politics": ["election", "president", "vote", "government", "campaign", "parliament"],
        "health": ["covid", "vaccine", "hospital", "healthcare", "mental health", "disease"],
        "science": ["space", "nasa", "astronomy", "research", "quantum", "physics", "scientist"],
        "general": []
    }

    def classify(self, text: str) -> str:
        text = text.lower()

        for category, keywords in self.keyword_map.items():
            for kw in keywords:
                if kw.lower() in text:
                    return category

        return "general"  # default fallback
