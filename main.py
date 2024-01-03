import nltk
from pathlib import Path
from tkinter import *
from tkinter import filedialog, messagebox
import tkinter.ttk as ttk
from nltk.corpus import stopwords
from string import punctuation
from wordfreq import top_n_list
import webbrowser
from langdetect import detect_langs
from NeuralNetwork import predict
from datetime import datetime
import os
from customtkinter import CTkButton


docs = []
langs = []

nltk.download("stopwords")
nltk.download("punkt")

stopwords_german = set(stopwords.words('german'))
stopwords_french = set(stopwords.words('french'))

root = Tk()
button_background = "black"
hover_button_color = "gray"
root['background'] = "white"
resultTree = ttk.Treeview(root,
                          columns=("Filename", "Freq Words", "Alphabet", "Neural Network", 'Distance'),
                          selectmode='browse', height=11)
resultTree.heading('Filename', text="Filename", anchor=W)
resultTree.heading('Freq Words', text="Freq Words", anchor=W)
resultTree.heading('Alphabet', text="Alphabet", anchor=W)
resultTree.heading('Neural Network', text="Neural Network", anchor=W)
resultTree.heading('Distance', text="Distance", anchor=W)
resultTree.column('#0', stretch=NO, minwidth=0, width=0)
resultTree.column('#1', stretch=NO, minwidth=277, width=277)
resultTree.column('#2', stretch=NO, minwidth=277, width=277)
resultTree.column('#3', stretch=NO, minwidth=277, width=277)
resultTree.column('#4', stretch=NO, minwidth=277, width=277)
aboutButton = CTkButton(root, text='How To', width=400, height=20, fg_color=button_background,
                        hover_color=hover_button_color, font=("Arial", 20))
chooseDocsButton = CTkButton(root, text='Browse HTML', width=400, height=20, fg_color=button_background,
                             hover_color=hover_button_color, font=("Arial", 20))
detectButton = CTkButton(root, text='Build Information', width=400, height=20, fg_color=button_background,
                         hover_color=hover_button_color, font=("Arial", 20))
saveButton = CTkButton(root, text='Save Result With Timestamp', width=400, height=20, fg_color=button_background,
                       hover_color=hover_button_color, font=("Arial", 20))
openButton = CTkButton(root, text='Open In Browser', width=400, height=20, fg_color=button_background,
                       hover_color=hover_button_color, font=("Arial", 20))
space = Label(root, text='\n')
application_documentation = """1. To browse file in system storage tap 'Browse HTML' button;
2. To build info about languages on documents from previous step tap 'Build Information' button;
3. To save results of previous file language detection with current timestamp tab 'Save Result With Timestamp' button;
4. To open document in browser choose its table row and tap 'Open Document' button.
"""


def nameOf(path):
    return Path(path).stem


def chooseDocsClicked():
    global docs, langs
    docs = []
    langs = []
    resultTree.delete(*resultTree.get_children())
    files = filedialog.askopenfilename(multiple=True)
    splitlist = root.tk.splitlist(files)
    for doc in splitlist:
        docs.append(
            (nameOf(doc), Path(doc, encoding="UTF-8", errors='ignore').read_text(encoding="UTF-8", errors='ignore')))
        resultTree.insert('', 'end', values=(nameOf(doc), '', '', '', ''))


def detect_freqwords_method(text):
    words = set()
    for sentence in nltk.sent_tokenize(text):
        for word in nltk.word_tokenize(sentence):
            if word not in punctuation:
                words.add(word)
    if len(words.intersection(top_n_list('de', 30))) > len(words.intersection(top_n_list('fr', 30))):
        return f"German - {round(len(words.intersection(top_n_list('de', 30))) / 30 * 100, 1)}%"
    else:
        return f"French - {round(len(words.intersection(top_n_list('fr', 30))) / 30 * 100, 1)}%"


def detect_alphabet_method(text):
    german_alphabet = set("ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜß".lower())
    french_alphabet = set("ABCDEFGHIJKLMNOPQRSTUVWXYZé’ç".lower())
    chars = set()
    for sentence in nltk.sent_tokenize(text):
        for word in nltk.word_tokenize(sentence):
            if word not in punctuation:
                chars.update(set(word.lower()))
    if len(german_alphabet.intersection(chars)) > len(french_alphabet.intersection(chars)):
        return f"German - {round(len(german_alphabet.intersection(chars)) / len(german_alphabet) * 100, 1)}%"
    else:
        return f"French - {round(len(french_alphabet.intersection(chars)) / len(french_alphabet) * 100, 1)}%"


def detect_nn_method(text):
    return predict(text)


def detectButtonClicked():
    resultTree.delete(*resultTree.get_children())
    for doc in docs:
        freqwords_method = detect_freqwords_method(doc[1])
        alphabet_method = detect_alphabet_method(doc[1])
        nn_method = detect_nn_method(doc[1])
        distance = detect_langs(doc[1])
        lang = "German" if str(distance[0]).split(":")[0] == 'de' else "French"
        dist = round(float(str(distance[0]).split(":")[1]), 1)
        resultTree.insert('', 'end', values=(doc[0], freqwords_method, alphabet_method, nn_method, f"{lang} - {dist}"))


def save():
    filename = f"Results/result-${datetime.now()}$.txt".replace(" ", "!").replace(":", "-").replace(".", "-")
    with open(filename, "w") as file:
        for k in resultTree.get_children(""):
            for i in resultTree.item(k)['values']:
                file.write(i)
                file.write(" - ")
            file.write("\n")


def open_web():
    if resultTree.item(resultTree.focus())['values'] != '':
        name = resultTree.item(resultTree.focus())['values'][0]
        webbrowser.open(f'{os.getcwd()}/Documents/{name}.html')


def aboutButtonClicked():
    messagebox.showinfo("How To Use", application_documentation)


if __name__ == '__main__':
    aboutButton.configure(command=aboutButtonClicked)
    chooseDocsButton.configure(command=chooseDocsClicked)
    detectButton.configure(command=detectButtonClicked)
    saveButton.configure(command=save)
    openButton.configure(command=open_web)

    aboutButton.pack()
    chooseDocsButton.pack()
    detectButton.pack()
    saveButton.pack()
    openButton.pack()
    space.pack()
    resultTree.pack()
    root.mainloop()
