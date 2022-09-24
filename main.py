from tkinter import Tk, Button, Canvas, PhotoImage
from random import randint
from pandas import read_csv, DataFrame, Series
BACKGROUND_COLOR = "#B1DDC6"

# flip card after 3 seconds
# check and x are for wether or not you know the answer
# green for english, white for french
# if you know the answer, the entry gets deleted from the list

# TODO 1: Make the card change back to french every round ---- DONE
# TODO 2: Write code for change_word_x()
    # TODO Bug fix: Prevent it from picking the same word ---- DONE

    # TODO 2.1: Add unknown words to a dataframe (figure out best method to do this)
    # TODO 2.2: Turn said dataframe into words_to_learn.csv when the program finishes or is closed

# TODO 3: Make it actually switch to the English word

# TODO 4: Create pop-up box when opening application that triggers change_language_french()
    # OR come up with better way to trigger this at launch.

# TODO Bug fix: deal with the key errors
# TODO Bug fix: if you click a button before it changes to English, bad things happen.

# AI for switching between languages

word_list = read_csv("french_words.csv")
words_to_learn = {
    "French": [],
    "English": []
}

def change_language_english():
    """Changes the language to english."""
    global word_list
    flash_card.itemconfig(language, text="English")
    flash_card.itemconfig(background, image=back)
    current_word = flash_card.itemcget("current_word", "text")
    current_word_index = word_list[word_list["French"] == current_word]
    flash_card.itemconfig(word, text=word_list["English"][current_word_index])

def change_language_french():
    """Changes the language to french.
    Removes the current word from the list and resets the flash card."""
    global word_list
    flash_card.itemconfig(language, text="French")
    flash_card.itemconfig(background, image=front)
    current_word = word_list["French"][randint(0, len(word_list) - 1)]
    flash_card.itemconfig(word, text=current_word)
    word_list = word_list.drop(word_list.index[word_list.French == current_word])

def change_word_check():
    """Function for the checkmark button."""
    change_language_french()
    flash_card.after(3000, change_language_english)

def change_word_x():
    """Function for the X button."""
    current_word = flash_card.itemcget("current_word", "text")
    words_to_learn["French"].append(current_word)
    # CONTINUE HERE. I was making it add the words to the dictionary.
    # I might have to complete TODO 3 before I continue
    change_language_french()
    flash_card.after(3000, change_language_english)
    print(words_to_learn)

def end_of_session():
    """Adds unknown words to a file new file called 'words_to_learn.csv'"""
    words_to_learn_df = DataFrame.from_dict(words_to_learn)
    words_to_learn_df.to_csv("words_to_learn.csv", index=False)

# Create the UI

window = Tk()
window.title("Flash Cards")
window.config(padx=50, pady=50)

front = PhotoImage(file="images/card_front.png")
back = PhotoImage(file="images/card_back.png")

flash_card = Canvas(width=800, height=526)

background = flash_card.create_image(400, 263, image=front)
language = flash_card.create_text(400, 150, text="French", font=("Arial", 40, "italic"))

# The following line is placeholder for an outdated way of filling in
    # the text at launch. I'm not ready to delete it yet.
# word = flash_card.create_text(400, 263,
#     text=word_list["French"][randint(0, len(word_list) - 1)], font=("Arial", 60, "bold"))

word = flash_card.create_text(400, 263,
    text="", font=("Arial", 60, "bold"), tag="current_word")

flash_card.grid(column=0, row=0, columnspan=2)

x_image = PhotoImage(file="images/wrong.png")
x_button = Button(image=x_image, highlightthickness=0, command=change_word_x)
x_button.grid(column=0, row=1)

check_image = PhotoImage(file="images/right.png")
check_button = Button(image=check_image, highlightthickness=0, command=change_word_check)
check_button.grid(column=1, row=1)

flash_card.after(3000, change_language_english)

window.mainloop()
