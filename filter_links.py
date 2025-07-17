from typing import List

def filter_links_by_substring(links: List[str], substring: str) -> List[str]:
    """
    Фильтрует список ссылок, возвращая только те, которые содержат указанную подстроку.
    """
    return [link for link in links if substring in link] 