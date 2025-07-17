import re
from typing import List
import requests
import logging
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def extract_links(url: str) -> List[str]:
    """
    Загружает HTML по указанному URL, извлекает все значения href из тегов <a> и возвращает их списком строк.
    При ошибках возвращает пустой список и пишет предупреждение в лог.
    """
    try:
        if not isinstance(url, str):
            logging.warning(f"URL должен быть строкой, получено: {type(url)}")
            return []
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        response.raise_for_status()
        html = response.text
        # print(html[:500])
        links = re.findall(r'<a\s[^>]*href="([^"]+)"', html)
        return links
    except Exception as e:
        logging.warning(f"Ошибка при обработке URL '{url}': {e}")
        return [] 