from turtle import Screen, Turtle

# ---------------- SCREEN SETUP ---------------- #

screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("My Snake Game")

# ---------------- SNAKE BODY ---------------- #

starting_positions = [(0, 0), (-20, 0), (-40, 0)]

segments = []

for position in starting_positions:
    new_segment = Turtle("square")
    new_segment.color("white")
    new_segment.penup()
    new_segment.goto(position)
    segments.append(new_segment)

# Screen open رکھیں
screen.mainloop()