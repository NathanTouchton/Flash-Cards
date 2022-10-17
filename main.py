from tkinter import Tk, Button, Canvas, PhotoImage, messagebox
from random import randint
from pandas import read_csv, DataFrame
BACKGROUND_COLOR = "#B1DDC6"

# flip card after 3 seconds
# check and x are for wether or not you know the answer
# green for english, white for french
# if you know the answer, the entry gets deleted from the list

# TODO 1: Make the card change back to french every round ---- DONE
# TODO 2: Write code for change_word_x()
    # TODO Bug fix: Prevent it from picking the same word ---- DONE

    # TODO 2.1: Add unknown words to a dataframe (figure out best method to do this) ---- DONE
    # TODO 2.2: Turn said dataframe into words_to_learn.csv when the program finishes or is closed

    # ValueError is what I'm looking for

# TODO 3: Make it actually switch to the English word ---- DONE

# TODO 4: Create pop-up box when opening application that triggers change_language_french()
    # OR come up with better way to trigger this at launch. ---- DONE

# TODO 5: Use "words_to_learn.csv" to create the WORD_LIST at launch, if it exists. ---- DONE

# TODO Bug fix: deal with the key errors ---- DONE
# TODO Bug fix: if you click a button before it changes to English, bad things happen.
# TODO Bug fix: initial dialogue box opens in the background

# AI for switching between languages

try:
    WORD_LIST = read_csv("words_to_learn.csv")
except FileNotFoundError:
    WORD_LIST = read_csv("french_words.csv")

words_to_learn = {
    "French": [],
    "English": []
}

def change_language_english():
    """Changes the language to english."""
    global WORD_LIST
    flash_card.itemconfig(language, text="English")
    flash_card.itemconfig(background, image=back)
    current_word = flash_card.itemcget("current_word", "text")
    WORD_LIST.set_index("French", inplace=True)
    current_word_index = WORD_LIST.loc[current_word, "English"]
    flash_card.itemconfig(word, text=current_word_index)
    WORD_LIST.reset_index(inplace=True)

def change_language_french():
    """Changes the language to French"""
    global WORD_LIST
    flash_card.itemconfig(language, text="French")
    flash_card.itemconfig(background, image=front)
    current_word = WORD_LIST["French"][randint(0, len(WORD_LIST) - 1)]
    flash_card.itemconfig(word, text=current_word)

def change_word_check():
    """Function for the checkmark button."""
    global WORD_LIST
    try:
        current_word = flash_card.itemcget("current_word", "text")
        WORD_LIST = WORD_LIST.drop(WORD_LIST.index[WORD_LIST.English == current_word])
        WORD_LIST.reset_index(inplace=True)
        change_language_french()
        flash_card.after(3000, change_language_english)
    except ValueError:
        end_of_session()

def change_word_x():
    """Function for the X button."""
    global WORD_LIST
    current_word = flash_card.itemcget("current_word", "text")
    try:
        if WORD_LIST["English"].isin([current_word]).any():
            words_to_learn["English"].append(current_word)

            WORD_LIST.set_index("English", inplace=True)
            current_word_index = WORD_LIST.loc[current_word, "French"]
            words_to_learn["French"].append(current_word_index)
            WORD_LIST.reset_index(inplace=True)
            WORD_LIST = WORD_LIST.drop(WORD_LIST.index[WORD_LIST.English == current_word])
            WORD_LIST.reset_index(inplace=True)

        elif WORD_LIST["French"].isin([current_word]).any():
            words_to_learn["French"].append(current_word)
            current_word_index = WORD_LIST.index[WORD_LIST.French == current_word]

            WORD_LIST.set_index("French", inplace=True)
            current_word_index = WORD_LIST.loc[current_word, "English"]
            words_to_learn["English"].append(current_word_index)
            WORD_LIST.reset_index(inplace=True)
            WORD_LIST = WORD_LIST.drop(WORD_LIST.index[WORD_LIST.French == current_word])
            WORD_LIST.reset_index(inplace=True)

        change_language_french()
        flash_card.after(3000, change_language_english)
        # print(words_to_learn)
    except ValueError:
        end_of_session()

def end_of_session():
    """Adds unknown words to a file new file called 'words_to_learn.csv'"""
    words_to_learn_df = DataFrame.from_dict(words_to_learn)
    words_to_learn_df.to_csv("words_to_learn.csv", index=False)
    messagebox.showinfo(title="End of session", message="""There are no more words to study\n
        Closing application""")
    window.destroy()

def new_session():
    """This shows a popup window that enables some of the initial functionality."""
    confirm = messagebox.askokcancel(title="Welcome", message="Welcome. Click OK to continue.")
    if confirm:
        change_language_french()
    confirm = False

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
    text="", font=("Arial", 60, "bold"), tag="current_word")

new_session()

flash_card.grid(column=0, row=0, columnspan=2)

x_image = PhotoImage(file="images/wrong.png")
x_button = Button(image=x_image, highlightthickness=0, command=change_word_x)
x_button.grid(column=0, row=1)

check_image = PhotoImage(file="images/right.png")
check_button = Button(image=check_image, highlightthickness=0, command=change_word_check)
check_button.grid(column=1, row=1)

flash_card.after(3000, change_language_english)

window.mainloop()
