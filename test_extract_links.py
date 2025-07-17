import unittest
from extract_links import extract_links

class TestExtractLinks(unittest.TestCase):
    def test_tech_crunch(self):
        links = extract_links("https://techcrunch.com/2025/07/15/")
        self.assertIsInstance(links, list)
        self.assertTrue(all(isinstance(link, str) for link in links))
        self.assertGreater(len(links), 0)  # На сайте python.org точно есть ссылки
        print(links)


if __name__ == "__main__":
    unittest.main() 