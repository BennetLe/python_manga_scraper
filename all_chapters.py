import glob
import os

import requests
from bs4 import BeautifulSoup
from PIL import Image
import urllib3
import os.path

from tkinter.messagebox import showinfo

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

links_manga = []
name_chapter = []
file_path = []


def get(URL, path):
    chapter_name = 0
    counter_name = 0

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    results_class = soup.find_all("a", class_="chapter-name text-nowrap")
    manga_name = str(soup.find("h1").text)
    manga_name = manga_name.replace("’", "").replace(":", "").replace("(", "").replace(")", "")

    # create a list of all the chapters
    for result_class in reversed(results_class):
        link = result_class["href"]
        links_manga.append(link)

    # get all the pictures from every chapter
    for link in links_manga:
        # get all image links from link
        chapter = requests.get(link)
        chapter_soup = BeautifulSoup(chapter.content, "html.parser")
        chapter_results = chapter_soup.find_all("img")

        # get all the pictures from chapter
        for chapter in chapter_results:
            chapter_picture = chapter["src"]
            # print the link of the img to log the progress
            print(chapter_picture)
            # get the pictures with the referer https://readmanganato.com/
            s = requests.Session()
            s.headers.update({"referer": "https://readmanganato.com/"})
            picture = s.get(chapter_picture, verify=False)

            # inc the counter for the img name
            counter_name += 1
            if chapter.has_attr("alt"):
                filename = ""+str(counter_name)
            else:
                filename = "BackButton"

            # save the picture
            file = open(f"{filename}.png", "wb")
            # print the filename to log the progress
            print(filename)
            file.write(picture.content)
            file.close()

        # clear the list file_path
        file_path.clear()
        # add every picture path to file_path
        for file in glob.glob("*.png"):
            file_path.append(file)

        # add content of file_path to images
        images = [
            Image.open(f)
            for f in file_path
        ]
        # inc the chapter name by one
        chapter_name += 1

        # convert every image type to RGB to prevent errors
        for i in range(0, len(images)):
            if images[i].mode != 'RGB':
                images[i] = images[i].convert('RGB')

        # set a save location and a filename for the PDF
        pdf_path = os.path.join(path, manga_name + "_"+str(chapter_name)+".pdf")

        # convert all the images to a PDF
        images[0].save(
            pdf_path, "PDF", resolution=100.0, save_all=True, append_images=images[1:]
        )
        # remove the old images
        for file in glob.glob("*.png"):
            os.remove(file)

        # console output to log the progress
        print(f"[*] Chapter {chapter_name} is converted to PDF")
        # input("Press Enter to continue...")
        images.clear()

    showinfo(message="Manga download complete!")