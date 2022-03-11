import glob
import os

import requests
from bs4 import BeautifulSoup
from PIL import Image

URL = "https://readmanganato.com/manga-iw985579"
page = requests.get(URL)

links_manga = []
name_chapter = []
file_path = []


def main():
    chaptername = 0
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="ResultsContainer")
    results_class = soup.find_all("a", class_="chapter-name text-nowrap")

    for result_class in reversed(results_class):
        link = result_class["href"]
        name = result_class.text.strip()
        # print(name + ":\n")
        # print(link, end="\n" * 2)
        links_manga.append(link)
        name_chapter.append(name)
        # print(links_manga)

    # for link in links_manga:
    # print(link + "\n")

    for link in links_manga:
        chapter = requests.get(link)
        chapter_soup = BeautifulSoup(chapter.content, "html.parser")
        chapter_results = chapter_soup.find_all("img")

        for chapter in chapter_results:
            chapter_picture = chapter["src"]
            print(chapter_picture)
            s = requests.Session()
            s.headers.update({"referer": "https://readmanganato.com/"})
            picture = s.get(chapter_picture, verify=False)

            if chapter.has_key("alt"):
                filename = chapter["alt"]
            else:
                filename = "BackButton"

            file = open(f"{filename}.png", "wb")
            print(filename)
            file.write(picture.content)
            file.close()

        file_path.clear()
        for file in glob.glob("*.png"):
            file_path.append(file)

        images = [
            Image.open(f)
            for f in file_path
        ]
        chaptername += 1

        for i in range(0, len(images)):
            if images[i].mode == 'RGBA':
                images[i] = images[i].convert('RGB')

        pdf_path = f"/Users/benne/Pictures/Manga_PDF/Chapter_{chaptername}.pdf"

        images[0].save(
            pdf_path, "PDF", resolution=100.0, save_all=True, append_images=images[1:]
        )


if __name__ == '__main__':
    main()
