
from tkinter import *
from tkinter import messagebox
import random
import string
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    letters = string.ascii_letters
    numbers = string.digits
    symbols = "!#$%&()*+"

    password_letters = [
        random.choice(letters)
        for _ in range(random.randint(8, 10))
    ]

    password_symbols = [
        random.choice(symbols)
        for _ in range(random.randint(2, 4))
    ]

    password_numbers = [
        random.choice(numbers)
        for _ in range(random.randint(2, 4))
    ]

    password_list = password_letters + password_symbols + password_numbers

    random.shuffle(password_list)

    password = "".join(password_list)

    password_entry.delete(0, END)
    password_entry.insert(0, password)

    # Password automatically copy to clipboard
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save_password():

    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    # Check empty fields
    if website == "" or password == "":
        messagebox.showwarning(
            title="Oops",
            message="Please don't leave any fields empty."
        )
        return

    # Confirmation popup
    is_ok = messagebox.askokcancel(
        title=website,
        message=f"These are the details entered:\n\n"
                f"Email: {email}\n"
                f"Password: {password}\n\n"
                f"Is it okay to save?"
    )

    if not is_ok:
        return

    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    # Try to read existing JSON data
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)

    # If data.json doesn't exist
    except FileNotFoundError:
        data = new_data

    # If data.json exists, update it
    else:
        data.update(new_data)

    # Save updated data
    with open("data.json", "w") as data_file:
        json.dump(data, data_file, indent=4)

    # Clear fields
    website_entry.delete(0, END)
    password_entry.delete(0, END)


# ---------------------------- FIND PASSWORD ------------------------------- #

def find_password():

    website = website_entry.get()

    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)

    except FileNotFoundError:
        messagebox.showerror(
            title="Error",
            message="No password data found."
        )
        return

    try:
        website_data = data[website]

    except KeyError:
        messagebox.showinfo(
            title="Not Found",
            message=f"No details for {website} exist."
        )

    else:
        email = website_data["email"]
        password = website_data["password"]

        messagebox.showinfo(
            title=website,
            message=f"Email: {email}\nPassword: {password}"
        )

        # Copy password to clipboard
        pyperclip.copy(password)


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()

window.title("Password Manager")

window.config(padx=50, pady=50)


# ---------------------------- LOGO ------------------------------- #

canvas = Canvas(
    width=200,
    height=200,
    highlightthickness=0
)

logo = PhotoImage(file="logo.png")

canvas.create_image(
    100,
    100,
    image=logo
)

canvas.grid(
    column=1,
    row=0
)


# ---------------------------- WEBSITE ------------------------------- #

website_label = Label(
    text="Website:"
)

website_label.grid(
    column=0,
    row=1
)


website_entry = Entry(
    width=21
)

website_entry.grid(
    column=1,
    row=1
)

website_entry.focus()


search_button = Button(
    text="Search",
    width=13,
    command=find_password
)

search_button.grid(
    column=2,
    row=1
)


# ---------------------------- EMAIL ------------------------------- #

email_label = Label(
    text="Email/Username:"
)

email_label.grid(
    column=0,
    row=2
)


email_entry = Entry(
    width=35
)

email_entry.grid(
    column=1,
    row=2,
    columnspan=2
)

email_entry.insert(
    0,
    "your@email.com"
)


# ---------------------------- PASSWORD ------------------------------- #

password_label = Label(
    text="Password:"
)

password_label.grid(
    column=0,
    row=3
)


password_entry = Entry(
    width=21
)

password_entry.grid(
    column=1,
    row=3
)


generate_button = Button(
    text="Generate Password",
    command=generate_password
)

generate_button.grid(
    column=2,
    row=3
)


# ---------------------------- ADD BUTTON ------------------------------- #

add_button = Button(
    text="Add",
    width=36,
    command=save_password
)

add_button.grid(
    column=1,
    row=4,
    columnspan=2
)


# ---------------------------- MAIN LOOP ------------------------------- #

window.mainloop()