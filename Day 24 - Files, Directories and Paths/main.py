from turtle import Turtle, Screen
import random
import time

# --- PLAYER ---
class Player(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("turtle")
        self.penup()
        self.goto(0, -280)
        self.setheading(90)

    def go_up(self):
        self.forward(10)

    def go_to_start(self):
        self.goto(0, -280)

    def is_at_finish(self):
        return self.ycor() > 280

# --- CAR ---
class CarManager:
    def __init__(self):
        self.all_cars = []
        self.car_speed = 5

    def create_car(self):
        if random.randint(1, 6) == 1:
            new_car = Turtle("square")
            new_car.shapesize(stretch_wid=1, stretch_len=2)
            new_car.penup()
            new_car.color(random.choice(["red","orange","yellow","green","blue","purple"]))
            new_car.goto(300, random.randint(-250, 250))
            self.all_cars.append(new_car)

    def move_cars(self):
        for car in self.all_cars:
            car.backward(self.car_speed)

    def level_up(self):
        self.car_speed += 10

# --- SCOREBOARD ---
class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.level = 1
        self.hideturtle()
        self.penup()
        self.goto(-280, 250)
        self.write(f"Level: {self.level}", align="left", font=("Courier", 24, "normal"))

    def increase_level(self):
        self.level += 1
        self.clear()
        self.write(f"Level: {self.level}", align="left", font=("Courier", 24, "normal"))

    def game_over(self):
        self.goto(0, 0)
        self.write("GAME OVER", align="center", font=("Courier", 24, "normal"))

# --- MAIN GAME ---
screen = Screen()
screen.setup(width=600, height=600)
screen.tracer(0)

player = Player()
car_manager = CarManager()
scoreboard = Scoreboard()

screen.listen()
screen.onkey(player.go_up, "Up")

game_is_on = True
while game_is_on:
    time.sleep(0.1)
    screen.update()
    car_manager.create_car()
    car_manager.move_cars()

    for car in car_manager.all_cars:
        if car.distance(player) < 20:
            game_is_on = False
            scoreboard.game_over()

    if player.is_at_finish():
        player.go_to_start()
        car_manager.level_up()
        scoreboard.increase_level()

screen.exitonclick()