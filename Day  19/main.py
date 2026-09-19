from turtle import Turtle, Screen

# Turtle بنائیں
timmy = Turtle()

# Turtle کی شکل
timmy.shape("turtle")

# Drawing کی speed
timmy.speed("fastest")

# Screen بنائیں
screen = Screen()

# Keyboard کو سننے کے لیے
screen.listen()


# آگے
def move_forward():
    timmy.forward(20)


# پیچھے
def move_backward():
    timmy.backward(20)


# بائیں مڑنا
def turn_left():
    timmy.left(15)


# دائیں مڑنا
def turn_right():
    timmy.right(15)


# Screen صاف کرنا
def clear_screen():
    timmy.clear()
    timmy.penup()
    timmy.home()
    timmy.pendown()


# Keyboard controls
screen.onkey(move_forward, "Up")
screen.onkey(move_backward, "Down")
screen.onkey(turn_left, "Left")
screen.onkey(turn_right, "Right")

# C دبانے سے drawing صاف ہوگی
screen.onkey(clear_screen, "c")

# Window کھلی رہے گی
screen.mainloop()