
from flask import Flask
import random

app = Flask(__name__)

secret_number = random.randint(0, 9)


@app.route("/")
def home():
    return """
    <html>
        <body style="text-align:center; font-family:Arial;
                     background-color:#f0f8ff; padding:50px;">
            <h1>Welcome to the Number Guessing Game!</h1>
            <h2>Guess a number between 0 and 9</h2>
            <p>URL ke aakhir mein apna number likhein.</p>
            <p>Example: <b>http://127.0.0.1:5000/5</b></p>
        </body>
    </html>
    """


@app.route("/<int:guess>")
def check_guess(guess):
    if guess < secret_number:
        message = "Too low! Try a higher number."
        color = "blue"
    elif guess > secret_number:
        message = "Too high! Try a lower number."
        color = "red"
    else:
        message = "You got it! You win!"
        color = "green"

    return f"""
    <html>
        <body style="text-align:center; font-family:Arial;
                     padding:50px;">
            <h1 style="color:{color};">{message}</h1>
            <h2>Your guess: {guess}</h2>
            <a href="/">Play Again</a>
        </body>
    </html>
    """


if __name__ == "__main__":
    app.run(debug=True)
