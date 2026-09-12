from turtle import Turtle, Screen
import random

# Hirst painting کے colours
color_list = [
    (235, 219, 190),
    (236, 232, 224),
    (198, 160, 103),
    (143, 91, 48),
    (187, 141, 84),
    (100, 70, 45),
    (218, 200, 169),
    (160, 110, 70),
    (75, 110, 120),
    (120, 150, 145),
    (190, 80, 60),
    (230, 150, 90)
]

# Turtle بنائیں
tim = Turtle()

tim.speed("fastest")
tim.penup()
tim.hideturtle()

# RGB colours کے لیے
screen = Screen()
screen.colormode(255)

# Starting position
tim.setheading(225)
tim.forward(300)
tim.setheading(0)

# 10 rows
for row in range(10):

    # ہر row میں 10 dots
    for dot in range(10):
        tim.dot(20, random.choice(color_list))
        tim.forward(50)

    # اگلی row پر جائیں
    tim.setheading(90)
    tim.forward(50)

    tim.setheading(180)
    tim.forward(500)

    tim.setheading(0)

screen.exitonclick()