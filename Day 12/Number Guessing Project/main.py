import random

# Game ka introduction
print("Welcome to the Number Guessing Game!")
print("I'm thinking of a number between 1 and 100.")

# Computer ek random number choose karega
answer = random.randint(1, 100)

# Difficulty choose karein
difficulty = input("Choose a difficulty. Type 'easy' or 'hard': ").lower()

if difficulty == "easy":
    attempts = 10
else:
    attempts = 5

# Game loop
while attempts > 0:
    print(f"\nYou have {attempts} attempts remaining.")

    guess = int(input("Make a guess: "))

    if guess == answer:
        print(f"You got it! The answer was {answer}.")
        break

    elif guess > answer:
        print("Too high.")

    else:
        print("Too low.")

    attempts -= 1

    if attempts == 0:
        print(f"\nYou've run out of guesses. The answer was {answer}.")