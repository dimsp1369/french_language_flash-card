from tkinter import *
from pandas import *
import random

BACKGROUND_COLOR = "#B1DDC6"
FRENCH_TITLE = 'French'
ENGLISH_TITLE = 'English'
current_dict = {}
word_dict = []


def fetch_data():
    global word_dict
    try:
        raw_data = read_csv("data/words_to_learn.csv")
    except FileNotFoundError:
        original_raw_data = read_csv("data/french_words.csv")
        word_dict = original_raw_data.to_dict(orient="records")
    else:
        word_dict = raw_data.to_dict(orient="records")


# --------------------- SETUP ---------------------------- #

window = Tk()
window.title("Flash Card")
window.config(padx=50, pady=50, background=BACKGROUND_COLOR)

# CARD
canvas = Canvas(width=800, height=526, background=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
card_image = canvas.create_image(400, 263, image=card_front)
title_text = canvas.create_text(400, 150, text=FRENCH_TITLE, font=("Ariel", 40, "italic"))
word_text = canvas.create_text(400, 263, font=("Ariel", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)


# --------------------- SETUP ---------------------------- #

# --------------------- LOGIC ---------------------------- #

def next_card(is_remember=False):
    global current_dict, timer_id, word_dict
    if is_remember:
        word_dict.remove(current_dict)
        new_raw_data = DataFrame(word_dict)
        new_raw_data.to_csv("data/words_to_learn.csv", index=False)
    window.after_cancel(timer_id)
    current_dict = random.choice(word_dict)
    canvas.itemconfig(word_text, text=current_dict[FRENCH_TITLE], fill="black")
    canvas.itemconfig(card_image, image=card_front)
    canvas.itemconfig(title_text, text=FRENCH_TITLE, fill="black")
    timer_id = window.after(3000, flip_card)


def flip_card():
    canvas.itemconfig(card_image, image=card_back)
    canvas.itemconfig(title_text, text=ENGLISH_TITLE, fill="white")
    canvas.itemconfig(word_text, text=current_dict[ENGLISH_TITLE], fill="white")


timer_id = window.after(3000, flip_card)
# --------------------- LOGIC ---------------------------- #


# --------------------- UI ------------------------------- #

# BUTTONS

X_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=X_image, highlightthickness=0, borderwidth=0, cursor="hand2",
                      command=lambda: next_card(False))
wrong_button.grid(column=0, row=1)

V_image = PhotoImage(file="images/right.png")
right_button = Button(image=V_image, highlightthickness=0, borderwidth=0, cursor="hand2",
                      command=lambda: next_card(True))
right_button.grid(column=1, row=1)
# --------------------- UI ------------------------------- #

fetch_data()
next_card()
window.mainloop()
