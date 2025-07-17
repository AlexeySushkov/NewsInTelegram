import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup


def get_html(url: str) -> str:
    """
    Загружает HTML-текст страницы по указанному адресу URL и возвращает только текстовое содержимое без тегов, CSS и JS.
    """
    response = requests.get(url, verify=False)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    # Удаляем все теги <script> и <style>
    for tag in soup(['script', 'style']):
        tag.decompose()
    text = soup.get_text(separator=' ', strip=True)
    return text 