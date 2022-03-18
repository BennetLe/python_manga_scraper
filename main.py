import all_chapters
import tkinter as tk
from tkinter.filedialog import askdirectory


def main():
    window = tk.Tk()

    def set_path():
        directory = askdirectory()
        lbl_path["text"] = f"{directory}"

    def get_manga():
        URL = input_URL.get()
        path = lbl_path["text"]
        if URL != "" and path != "":
            all_chapters.get(URL, path)

    window.rowconfigure([0, 1, 2, 3], minsize=25, weight=1)
    window.columnconfigure([0], minsize=300, weight=1)

    input_URL = tk.Entry(master=window)
    input_URL.grid(row=0, column=0, sticky="nsew")

    btn_path = tk.Button(master=window, text="Open path selector", command=set_path)
    btn_path.grid(row=1, column=0, sticky="nsew")

    lbl_path = tk.Label(master=window, text="")
    # lbl_path.grid(row=2, column=0, sticky="nsew")

    btn_submit = tk.Button(master=window, text="Get Manga", command=get_manga)
    btn_submit.grid(row=3, column=0, sticky="nsew")

    window.mainloop()


if __name__ == '__main__':
    main()