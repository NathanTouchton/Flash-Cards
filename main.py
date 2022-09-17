from tkinter import Tk, Button, Canvas, PhotoImage
from pandas import read_csv
BACKGROUND_COLOR = "#B1DDC6"

# flip card after 3 seconds
# check and x are for wether or not you know the answer
# green for english, white for french
# if you know the answer, the entry gets deleted from the list

# AI for the word picker


# Create the UI
window = Tk()
window.title("Flash Cards")
window.config(padx=50, pady=50)

front = PhotoImage(file="images/card_front.png")

flash_card = Canvas(width=800, height=526)
flash_card.create_image(400, 263, image=front)
flash_card.create_text(400, 150, text="Title", font=("Arial", 40, "italic"))
flash_card.create_text(400, 263, text="Word", font=("Arial", 60, "bold"))
flash_card.grid(column=0, row=0, columnspan=2)

wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0)
wrong_button.grid(column=0, row=1)

right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0)
right_button.grid(column=1, row=1)

window.mainloop()
