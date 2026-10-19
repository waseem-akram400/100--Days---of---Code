
from tkinter import *


def calculate():
    miles = float(miles_input.get())
    kilometers = miles * 1.60934
    kilometer_result.config(text=kilometers)


# Window بنانا
window = Tk()
window.title("Miles to Kilometers Converter")
window.minsize(width=300, height=200)
window.config(padx=20, pady=20)


# Miles کا Label
miles_label = Label(text="Miles")
miles_label.grid(column=2, row=0)


# Miles کا Input Box
miles_input = Entry(width=10)
miles_input.grid(column=1, row=0)


# برابر (=) کا Label
equal_label = Label(text="is equal to")
equal_label.grid(column=0, row=1)


# Kilometers کا Result
kilometer_result = Label(text="0")
kilometer_result.grid(column=1, row=1)


# Kilometers کا Label
kilometer_label = Label(text="Km")
kilometer_label.grid(column=2, row=1)


# Calculate Button
calculate_button = Button(text="Calculate", command=calculate)
calculate_button.grid(column=1, row=2)


# Window چلانا
window.mainloop()