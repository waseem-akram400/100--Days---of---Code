
from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"

# ---------------------------- READ DATA ------------------------------- #

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/french_words.csv")

to_learn = data.to_dict(orient="records")

current_card = {}


# ---------------------------- NEXT CARD ------------------------------- #

def next_card():
    global current_card, flip_timer

    window.after_cancel(flip_timer)

    current_card = random.choice(to_learn)

    canvas.itemconfig(
        card_title,
        text="French",
        fill="black"
    )

    canvas.itemconfig(
        card_word,
        text=current_card["French"],
        fill="black"
    )

    canvas.itemconfig(
        card_background,
        image=card_front_img
    )

    flip_timer = window.after(
        3000,
        func=flip_card
    )


# ---------------------------- FLIP CARD ------------------------------- #

def flip_card():
    canvas.itemconfig(
        card_title,
        text="English",
        fill="white"
    )

    canvas.itemconfig(
        card_word,
        text=current_card["English"],
        fill="white"
    )

    canvas.itemconfig(
        card_background,
        image=card_back_img
    )


# ---------------------------- KNOW CARD ------------------------------- #

def is_known():
    to_learn.remove(current_card)

    data = pandas.DataFrame(to_learn)

    data.to_csv(
        "data/words_to_learn.csv",
        index=False
    )

    next_card()


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Flashy")
window.config(
    padx=50,
    pady=50,
    bg=BACKGROUND_COLOR
)


# ---------------------------- TIMER ------------------------------- #

flip_timer = window.after(
    3000,
    func=flip_card
)


# ---------------------------- CANVAS ------------------------------- #

canvas = Canvas(
    width=800,
    height=526,
    bg=BACKGROUND_COLOR,
    highlightthickness=0
)

card_front_img = PhotoImage(
    file="images/card_front.png"
)

card_back_img = PhotoImage(
    file="images/card_back.png"
)

card_background = canvas.create_image(
    400,
    263,
    image=card_front_img
)

card_title = canvas.create_text(
    400,
    150,
    text="Title",
    font=("Ariel", 40, "italic")
)

card_word = canvas.create_text(
    400,
    263,
    text="Word",
    font=("Ariel", 60, "bold")
)

canvas.grid(
    column=0,
    row=0,
    columnspan=2
)


# ---------------------------- BUTTONS ------------------------------- #

wrong_img = PhotoImage(
    file="images/wrong.png"
)

wrong_button = Button(
    image=wrong_img,
    highlightthickness=0,
    command=next_card
)

wrong_button.grid(
    column=0,
    row=1
)


right_img = PhotoImage(
    file="images/right.png"
)

right_button = Button(
    image=right_img,
    highlightthickness=0,
    command=is_known
)

right_button.grid(
    column=1,
    row=1
)


# ---------------------------- START ------------------------------- #

next_card()

window.mainloop()
