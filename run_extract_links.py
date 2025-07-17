from extract_links import extract_links
from filter_links import filter_links_by_substring
from get_html import get_html

if __name__ == "__main__":
    # url = input("Введите URL: ")
    url = "https://techcrunch.com/2025/07/15/"
    links = extract_links(url)
    print(f"Найдено {len(links)} ссылок:")
    for link in links:
        print(link)

    substring = "2025/07/15/"
    filtered_links = filter_links_by_substring(links, substring)
    print(f"\nСсылки, содержащие подстроку '{substring}': {len(filtered_links)}")
    for link in filtered_links:
        print(link)

    print("\nОбработка последних 5 ссылок:")
    for link in filtered_links[-5:]:
        print(link)
        try:
            html = get_html(link)
            print(f"  HTML (первые 200 символов): {html[:200]}")
        except Exception as e:
            print(f"  Ошибка при получении HTML: {e}")
