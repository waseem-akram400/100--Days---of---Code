import turtle
import random
import math

# Game window
screen = turtle.Screen()
screen.title("Day 95 - Space Invaders")
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.tracer(0)

# Game variables
score = 0
game_over = False
enemy_direction = 1
bullets = []
enemies = []

# Score display
pen = turtle.Turtle()
pen.hideturtle()
pen.penup()
pen.color("white")
pen.goto(-370, 255)

def update_score():
    pen.clear()
    pen.write(
        f"Score: {score}     Move: Left/Right     Shoot: Space",
        font=("Arial", 14, "normal")
    )

# Player spaceship
player = turtle.Turtle()
player.shape("triangle")
player.color("cyan")
player.penup()
player.setheading(90)
player.goto(0, -240)
player_speed = 25

def move_left():
    if not game_over and player.xcor() > -365:
        player.setx(player.xcor() - player_speed)

def move_right():
    if not game_over and player.xcor() < 365:
        player.setx(player.xcor() + player_speed)

# Create enemies
for row in range(3):
    for col in range(8):
        enemy = turtle.Turtle()
        enemy.shape("circle")
        enemy.color(random.choice(["red", "orange", "magenta"]))
        enemy.penup()
        enemy.goto(-280 + col * 80, 180 - row * 55)
        enemies.append(enemy)

# Create a bullet
def shoot():
    if game_over or len(bullets) >= 5:
        return

    bullet = turtle.Turtle()
    bullet.shape("square")
    bullet.color("yellow")
    bullet.shapesize(stretch_wid=0.3, stretch_len=0.8)
    bullet.penup()
    bullet.goto(player.xcor(), player.ycor() + 15)
    bullets.append(bullet)

# Collision check
def touching(a, b, distance=20):
    return math.hypot(
        a.xcor() - b.xcor(),
        a.ycor() - b.ycor()
    ) < distance

# Game over message
message = turtle.Turtle()
message.hideturtle()
message.penup()
message.color("white")

def end_game(text):
    global game_over
    if game_over:
        return

    game_over = True
    message.goto(0, 0)
    message.write(
        text,
        align="center",
        font=("Arial", 24, "bold")
    )
    screen.update()

# Keyboard controls
screen.listen()
screen.onkeypress(move_left, "Left")
screen.onkeypress(move_right, "Right")
screen.onkeypress(move_left, "a")
screen.onkeypress(move_right, "d")
screen.onkeypress(shoot, "space")

def game_loop():
    global enemy_direction, score

    if game_over:
        return

    # Move enemies from side to side
    change_direction = False

    for enemy in enemies:
        new_x = enemy.xcor() + 2 * enemy_direction
        if new_x > 365 or new_x < -365:
            change_direction = True

    if change_direction:
        enemy_direction *= -1
        for enemy in enemies:
            enemy.sety(enemy.ycor() - 20)

    for enemy in enemies:
        enemy.setx(enemy.xcor() + 2 * enemy_direction)

        # Enemies reaching the player mean game over
        if enemy.ycor() < -210:
            end_game("GAME OVER!")
            return

        if touching(enemy, player, 25):
            end_game("GAME OVER!")
            return

    # Move bullets upward
    for bullet in bullets[:]:
        bullet.sety(bullet.ycor() + 12)

        if bullet.ycor() > 290:
            bullet.hideturtle()
            bullets.remove(bullet)
            continue

        # Check bullet-enemy collisions
        hit_enemy = None

        for enemy in enemies:
            if touching(bullet, enemy, 20):
                hit_enemy = enemy
                break

        if hit_enemy is not None:
            hit_enemy.hideturtle()
            enemies.remove(hit_enemy)

            bullet.hideturtle()
            if bullet in bullets:
                bullets.remove(bullet)

            score += 10
            update_score()

    # Win when all enemies are destroyed
    if not enemies:
        end_game("YOU WIN!")
        return

    screen.update()
    screen.ontimer(game_loop, 20)

update_score()
game_loop()
screen.mainloop()
