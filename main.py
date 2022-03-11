import requests
from bs4 import BeautifulSoup

URL = "https://readmanganato.com/manga-iw985579"
page = requests.get(URL)

links_manga = []
name_chapter = []

def main():
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="ResultsContainer")
    results_class = soup.find_all("a", class_="chapter-name text-nowrap")

    for result_class in reversed(results_class):
        link = result_class["href"]
        name = result_class.text.strip()
        print(name + ":\n")
        print(link, end="\n" * 2)
        links_manga.append(link)
        name_chapter.append(name)

    for link in links_manga:
        print(link + "\n")


if __name__ == '__main__':
    main()