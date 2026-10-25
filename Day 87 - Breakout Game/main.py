
import tkinter as tk
import random


# گیم کی چوڑائی اور اونچائی
WIDTH = 800
HEIGHT = 600

# پیڈل کی سیٹنگز
PADDLE_WIDTH = 110
PADDLE_HEIGHT = 15
PADDLE_SPEED = 30

# گیند کی سیٹنگز
BALL_SIZE = 16
BALL_SPEED_X = 4
BALL_SPEED_Y = -4

# اینٹوں کی سیٹنگز
BRICK_ROWS = 5
BRICK_COLS = 10
BRICK_WIDTH = 68
BRICK_HEIGHT = 22
BRICK_GAP = 6
BRICK_TOP = 70


class BreakoutGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Day 87 - Breakout Game")
        self.root.resizable(False, False)

        # گیم کی معلومات
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.ball_dx = BALL_SPEED_X
        self.ball_dy = BALL_SPEED_Y

        # گیم کا کینوس
        self.canvas = tk.Canvas(
            root,
            width=WIDTH,
            height=HEIGHT,
            bg="#101827",
            highlightthickness=0
        )
        self.canvas.pack()

        # اسکور اور باقی جانیں
        self.score_text = self.canvas.create_text(
            20, 20,
            anchor="w",
            text="Score: 0",
            fill="white",
            font=("Arial", 15, "bold")
        )

        self.lives_text = self.canvas.create_text(
            WIDTH - 20, 20,
            anchor="e",
            text="Lives: 3",
            fill="white",
            font=("Arial", 15, "bold")
        )

        # پیڈل بنائیں
        paddle_y = HEIGHT - 45
        self.paddle = self.canvas.create_rectangle(
            WIDTH // 2 - PADDLE_WIDTH // 2,
            paddle_y,
            WIDTH // 2 + PADDLE_WIDTH // 2,
            paddle_y + PADDLE_HEIGHT,
            fill="#38bdf8",
            outline=""
        )

        # گیند بنائیں
        self.ball = self.canvas.create_oval(
            WIDTH // 2 - BALL_SIZE // 2,
            HEIGHT // 2,
            WIDTH // 2 + BALL_SIZE // 2,
            HEIGHT // 2 + BALL_SIZE,
            fill="#facc15",
            outline=""
        )

        # تمام اینٹوں کی فہرست
        self.bricks = []
        self.create_bricks()

        # پیغام دکھانے کے لیے
        self.message = self.canvas.create_text(
            WIDTH // 2,
            HEIGHT // 2,
            text="",
            fill="white",
            font=("Arial", 26, "bold")
        )

        # کی بورڈ کنٹرول
        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)
        self.root.bind("<KeyPress-a>", self.move_left)
        self.root.bind("<KeyPress-d>", self.move_right)
        self.root.bind("<KeyPress-A>", self.move_left)
        self.root.bind("<KeyPress-D>", self.move_right)
        self.root.bind("<KeyPress-r>", self.restart)
        self.root.bind("<KeyPress-R>", self.restart)

        self.canvas.focus_set()

        # گیم شروع کریں
        self.game_loop()

    def create_bricks(self):
        """کینوس پر اینٹوں کی قطاریں بنائیں۔"""

        colors = [
            "#fb7185",
            "#fb923c",
            "#facc15",
            "#4ade80",
            "#60a5fa"
        ]

        total_width = (
            BRICK_COLS * BRICK_WIDTH
            + (BRICK_COLS - 1) * BRICK_GAP
        )
        start_x = (WIDTH - total_width) // 2

        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):
                x1 = start_x + col * (BRICK_WIDTH + BRICK_GAP)
                y1 = BRICK_TOP + row * (BRICK_HEIGHT + BRICK_GAP)
                x2 = x1 + BRICK_WIDTH
                y2 = y1 + BRICK_HEIGHT

                brick = self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=colors[row],
                    outline="#101827",
                    width=2
                )

                self.bricks.append(brick)

    def move_left(self, event=None):
        """پیڈل کو بائیں طرف حرکت دیں۔"""
        if self.game_over:
            return

        x1, y1, x2, y2 = self.canvas.coords(self.paddle)

        if x1 > 0:
            self.canvas.move(self.paddle, -PADDLE_SPEED, 0)

        # پیڈل کو دیوار سے باہر جانے سے روکیں
        x1, y1, x2, y2 = self.canvas.coords(self.paddle)
        if x1 < 0:
            self.canvas.move(self.paddle, -x1, 0)

    def move_right(self, event=None):
        """پیڈل کو دائیں طرف حرکت دیں۔"""
        if self.game_over:
            return

        x1, y1, x2, y2 = self.canvas.coords(self.paddle)

        if x2 < WIDTH:
            self.canvas.move(self.paddle, PADDLE_SPEED, 0)

        # پیڈل کو دائیں دیوار سے باہر جانے سے روکیں
        x1, y1, x2, y2 = self.canvas.coords(self.paddle)
        if x2 > WIDTH:
            self.canvas.move(self.paddle, WIDTH - x2, 0)

    def game_loop(self):
        """بار بار گیند کو حرکت دے کر ٹکراؤ چیک کریں۔"""
        if not self.game_over:
            self.move_ball()

        self.root.after(16, self.game_loop)

    def move_ball(self):
        """گیند کی حرکت اور ٹکراؤ سنبھالیں۔"""
        self.canvas.move(self.ball, self.ball_dx, self.ball_dy)

        x1, y1, x2, y2 = self.canvas.coords(self.ball)

        # بائیں اور دائیں دیواروں سے ٹکراؤ
        if x1 <= 0:
            self.ball_dx = abs(self.ball_dx)
        elif x2 >= WIDTH:
            self.ball_dx = -abs(self.ball_dx)

        # اوپر والی دیوار سے ٹکراؤ
        if y1 <= 40:
            self.ball_dy = abs(self.ball_dy)

        # پیڈل سے ٹکراؤ
        px1, py1, px2, py2 = self.canvas.coords(self.paddle)

        if (
            self.ball_dy > 0
            and y2 >= py1
            and y1 <= py2
            and x2 >= px1
            and x1 <= px2
        ):
            self.ball_dy = -abs(self.ball_dy)

            # پیڈل پر گیند کہاں لگی، اس کے مطابق زاویہ بدلیں
            paddle_center = (px1 + px2) / 2
            ball_center = (x1 + x2) / 2
            hit_position = (ball_center - paddle_center) / (PADDLE_WIDTH / 2)

            self.ball_dx = hit_position * 5

            # بالکل سیدھی حرکت سے بچنے کے لیے
            if abs(self.ball_dx) < 1.2:
                self.ball_dx = 1.2 if self.ball_dx >= 0 else -1.2

        # اینٹ سے ٹکراؤ
        overlapping_items = self.canvas.find_overlapping(x1, y1, x2, y2)

        for item in overlapping_items:
            if item in self.bricks:
                self.canvas.delete(item)
                self.bricks.remove(item)

                self.score += 10
                self.canvas.itemconfig(
                    self.score_text,
                    text=f"Score: {self.score}"
                )

                # اینٹ ٹوٹنے پر گیند واپس اچھلے
                self.ball_dy *= -1
                break

        # اگر تمام اینٹیں ٹوٹ جائیں تو جیت
        if not self.bricks:
            self.end_game("YOU WIN!\nPress R to play again")
            return

        # اگر گیند نیچے گر جائے تو ایک جان کم
        if y1 > HEIGHT:
            self.lives -= 1
            self.canvas.itemconfig(
                self.lives_text,
                text=f"Lives: {self.lives}"
            )

            if self.lives <= 0:
                self.end_game("GAME OVER\nPress R to try again")
            else:
                self.reset_ball()

    def reset_ball(self):
        """گیند کو دوبارہ پیڈل کے اوپر رکھیں۔"""
        self.canvas.coords(
            self.ball,
            WIDTH // 2 - BALL_SIZE // 2,
            HEIGHT // 2,
            WIDTH // 2 + BALL_SIZE // 2,
            HEIGHT // 2 + BALL_SIZE
        )

        # اگلی کوشش میں گیند کی سمت بدل سکتی ہے
        self.ball_dx = random.choice([-4, 4])
        self.ball_dy = -4

    def end_game(self, text):
        """گیم ختم ہونے یا جیتنے کا پیغام دکھائیں۔"""
        self.game_over = True
        self.canvas.itemconfig(
            self.message,
            text=text,
            fill="#86efac" if "WIN" in text else "#fca5a5"
        )

    def restart(self, event=None):
        """R دبانے پر گیم دوبارہ شروع کریں۔"""
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.ball_dx = BALL_SPEED_X
        self.ball_dy = BALL_SPEED_Y

        self.canvas.delete("all")

        # اسکور، جانیں، پیڈل، گیند اور اینٹیں دوبارہ بنائیں
        self.score_text = self.canvas.create_text(
            20, 20, anchor="w",
            text="Score: 0",
            fill="white",
            font=("Arial", 15, "bold")
        )

        self.lives_text = self.canvas.create_text(
            WIDTH - 20, 20, anchor="e",
            text="Lives: 3",
            fill="white",
            font=("Arial", 15, "bold")
        )

        paddle_y = HEIGHT - 45
        self.paddle = self.canvas.create_rectangle(
            WIDTH // 2 - PADDLE_WIDTH // 2,
            paddle_y,
            WIDTH // 2 + PADDLE_WIDTH // 2,
            paddle_y + PADDLE_HEIGHT,
            fill="#38bdf8",
            outline=""
        )

        self.ball = self.canvas.create_oval(
            WIDTH // 2 - BALL_SIZE // 2,
            HEIGHT // 2,
            WIDTH // 2 + BALL_SIZE // 2,
            HEIGHT // 2 + BALL_SIZE,
            fill="#facc15",
            outline=""
        )

        self.bricks = []
        self.create_bricks()

        self.message = self.canvas.create_text(
            WIDTH // 2,
            HEIGHT // 2,
            text="",
            fill="white",
            font=("Arial", 26, "bold")
        )

        self.canvas.focus_set()


if __name__ == "__main__":
    window = tk.Tk()
    game = BreakoutGame(window)
    window.mainloop()
