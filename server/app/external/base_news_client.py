from abc import ABC, abstractmethod
from typing import List, Dict

class BaseNewsClient(ABC):

    @abstractmethod
    def fetch_top_headlines(self, category: str = None) -> List[Dict]:
        pass
