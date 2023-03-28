import nltk
import re
import os
import glob
import tkinter as tk
from tkinter import END
from nltk.tokenize import word_tokenize

#Ahmed Mohamed 20190062
#Samaa Khalifa 20190247
#Noura Ashraf 20190592

# Change directory
os.chdir("/Users/ahmed Ibrahim/data")

# Read file start with format .txt
filesNames = glob.glob("*.txt")

data = []
for x in range(3000):
    textfile = open(filesNames[x], encoding="utf8")
    data.append(textfile.read())


def preprocessingData():
    for i in range(len(data)):
        formatedtxt = data[i].lower()
        formatedtxt = re.sub('[^A-Za-z0-9\s]+', '', formatedtxt)
        tokens = word_tokenize(formatedtxt)
        corpus.extend(tokens)


corpus = []
unigramCounts = dict()
bigramCounts = dict()
trigramCounts = dict()

def unigram():
    return nltk.FreqDist(corpus)


def trainingCorpus():
    for i in range(len(corpus) - 2):
        bigram = (corpus[i], corpus[i + 1])
        trigram = (corpus[i], corpus[i + 1], corpus[i + 2])
        if bigram in bigramCounts.keys():
            bigramCounts[bigram] += 1
        else:
            bigramCounts[bigram] = 1

        if trigram in trigramCounts.keys():
            trigramCounts[trigram] += 1
        else:
            trigramCounts[trigram] = 1

    unigramCounts = unigram()


def bigramSuggestion(tokenized_input):
    lastToken = tokenized_input[-1:][0]  # get last token from textInput

    probabilities = dict()
    for token in corpus:
        bigram = (lastToken, token)  # store last input token with each word in corpus
        unigram = (lastToken)

        bigram_count = bigramCounts.get(bigram, 0)  # get count of input token with corpus word
        unigram_count = unigramCounts.get(unigram, 0)  # get count of input token

        bigram_Probability = (bigram_count + 1) / (unigram_count + size)  # do smoothing
        probabilities[token] = bigram_Probability

    res_suggest = sorted(probabilities.items(), key=lambda x: x[1], reverse=True)[:10]
    return res_suggest


def trigramSuggestion(tokenized_input):
    last_twoToken = tokenized_input[-2:]  # get last two token from textInput

    probabilities = dict()
    for token in corpus:
        trigram = (last_twoToken[0], last_twoToken[1], token)  # store last two input token with each word in corpus
        bigram = (last_twoToken[0], last_twoToken[1])

        trigram_count = trigramCounts.get(trigram, 0)  # get count of two input token with corpus word
        bigram_count = bigramCounts.get(bigram, 0)  # get count of two input token

        trigram_Probability = (trigram_count + 1) / (bigram_count + size)  # do smoothing
        probabilities[token] = trigram_Probability

    res_suggest = sorted(probabilities.items(), key=lambda x: x[1], reverse=True)[:10]
    return res_suggest


def suggest_next_word(textInput):
    tokenized_input = word_tokenize(textInput.lower())  # convert textInput to lowercase text
    if len(tokenized_input) > 1:
        return trigramSuggestion(tokenized_input)
    else:
        return bigramSuggestion(tokenized_input)


preprocessingData()
trainingCorpus()

size = len(corpus)
dist_corpus = set(corpus)

my_w = tk.Tk()
my_w.geometry("760x400")  # Size of the window
my_w.title("N Grams")   # Adding a title
font1 = ('Times', 18, 'bold')  # font size and style
img = tk.PhotoImage(file="/Users/ahmed Ibrahim/PycharmProjects/NGrams/google.png")
img = img.subsample(11)
l0 = tk.Label(text='Google', font=font1,image=img)   # adding label at top
l0.grid(row=0, column=1)
l0.place(x=380, y=55, anchor="center")

# data source list,
my_list = ['aecde', 'adba', 'acbd', 'abcd', 'abded',
           'bdbd', 'baba', 'bcbc', 'bdbd']


def my_upd(my_widget):  # On selection of option
    my_w = my_widget.widget
    index = int(my_w.curselection()[0])  # position of selection
    value = my_w.get(index)  # selected value
    e1_str.set(e1.get()+' '+value)  # set value for string variable of Entry
    l1.delete(0, END)  # Delete all elements of Listbox


def my_down(my_widget):  # down arrow is clicked
    l1.focus()  # move focus to Listbox
    l1.selection_set(0)  # select the first option


e1_str = tk.StringVar()  # string variable
e1 = tk.Entry(my_w, textvariable=e1_str, font=font1,width=30)  # entry
e1.grid(row=1, column=1, padx=10, pady=0)
e1.place(x=380, y=120, anchor="center")
# listbox
l1 = tk.Listbox(my_w, height=6, font=font1, relief='flat',
                bg='SystemButtonFace', highlightcolor='SystemButtonFace',width=30)

l1.grid(row=2, column=1)

l1.place(x=380, y=220, anchor="center")


def get_data(*args):  # populate the Listbox with matching options
    search_str = e1.get()  # user entered string
    l1.delete(0, END)  # Delete all elements of Listbox
    my_list.clear()
    str = suggest_next_word(search_str)
    for i in range(len(str)):
        my_list.append(str[i][0])
    for element in my_list:
        l1.insert(tk.END, element)  # add matching options to Listbox


# l1.bind('<<ListboxSelect>>', my_upd)
e1.bind('<Down>', my_down)  # down arrow key is pressed
l1.bind('<Right>', my_upd)  # right arrow key is pressed
l1.bind('<Return>', my_upd)  # return key is pressed
e1_str.trace('w', get_data)  #

# print(my_w['bg']) # reading background colour of window
my_w.mainloop()  # Keep the window open
