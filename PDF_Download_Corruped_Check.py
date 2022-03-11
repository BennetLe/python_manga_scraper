from PyPDF2 import PdfFileReader
import glob, os

files = []

os.chdir("/Users/benne/Pictures/Manga_PDF")
for file in glob.glob("*.pdf"):
    pdf = PdfFileReader(open(file, 'rb'))
    if pdf.getNumPages() <= 2:
        print(file)
        files.append(file)

for file in files:
    if "CORRUPTED" in file:
        os.rename(r"" + file, r"CORRUPTED_" + file)