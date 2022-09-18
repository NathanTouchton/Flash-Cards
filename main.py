from tkinter import Tk, Button, Canvas, PhotoImage
from random import randint
from pandas import read_csv
BACKGROUND_COLOR = "#B1DDC6"

# flip card after 3 seconds
# check and x are for wether or not you know the answer
# green for english, white for french
# if you know the answer, the entry gets deleted from the list

# AI for switching between languages
def change_language():
    flash_card.itemconfig(language, text="English")
    flash_card.itemconfig(background, image=back)

# AI for the word picker

word_list = read_csv("french_words.csv")

def change_word_check():
    global word_list
    current_word = word_list["French"][randint(0, len(word_list.index - 2))]
    flash_card.itemconfig(word, text=current_word)
    word_list = word_list.drop(word_list.index[word_list.French == current_word])

# TODO 1: Make the card change back to french every round
# TODO 2: Write code for change_word_x()

# def change_word_x():

# Create the UI
window = Tk()
window.title("Flash Cards")
window.config(padx=50, pady=50)

front = PhotoImage(file="images/card_front.png")
back = PhotoImage(file="images/card_back.png")

flash_card = Canvas(width=800, height=526)

background = flash_card.create_image(400, 263, image=front)
language = flash_card.create_text(400, 150, text="French", font=("Arial", 40, "italic"))
word = flash_card.create_text(400, 263,
    text=word_list["French"][randint(0, len(word_list.index - 2))], font=("Arial", 60, "bold"))

flash_card.grid(column=0, row=0, columnspan=2)

wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0)
wrong_button.grid(column=0, row=1)

right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0, command=change_word_check)
right_button.grid(column=1, row=1)

flash_card.after(3000, change_language)

window.mainloop()
