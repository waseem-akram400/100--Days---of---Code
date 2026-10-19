
import tkinter as tk
from quiz_brain import QuizBrain


THEME_COLOR = "#375362"


class QuizInterface:
    def __init__(self, quiz: QuizBrain):
        self.quiz = quiz

        self.window = tk.Tk()
        self.window.title("Day 34 - Trivia Quiz")
        self.window.config(
            padx=20,
            pady=20,
            bg=THEME_COLOR
        )
        self.window.minsize(width=350, height=400)

        self.score_label = tk.Label(
            text="Score: 0",
            fg="white",
            bg=THEME_COLOR,
            font=("Arial", 12, "bold")
        )
        self.score_label.grid(row=0, column=1, pady=10)

        self.canvas = tk.Canvas(
            width=320,
            height=250,
            bg="white",
            highlightthickness=0
        )
        self.question_text = self.canvas.create_text(
            160,
            125,
            width=280,
            text="Loading question...",
            font=("Arial", 17, "italic"),
            fill=THEME_COLOR
        )
        self.canvas.grid(
            row=1,
            column=0,
            columnspan=2,
            pady=20
        )

        self.true_button = tk.Button(
            text="True",
            width=12,
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            command=lambda: self.answer_question("True")
        )
        self.true_button.grid(
            row=2,
            column=0,
            padx=5,
            pady=10
        )

        self.false_button = tk.Button(
            text="False",
            width=12,
            font=("Arial", 12, "bold"),
            bg="#F44336",
            fg="white",
            command=lambda: self.answer_question("False")
        )
        self.false_button.grid(
            row=2,
            column=1,
            padx=5,
            pady=10
        )

        self.feedback_label = tk.Label(
            text="",
            fg="white",
            bg=THEME_COLOR,
            font=("Arial", 12, "bold")
        )
        self.feedback_label.grid(
            row=3,
            column=0,
            columnspan=2,
            pady=10
        )

        self.get_next_question()
        self.window.mainloop()

    def get_next_question(self):
        self.canvas.config(bg="white")

        if self.quiz.still_has_questions():
            self.current_question = self.quiz.next_question()

            self.canvas.itemconfig(
                self.question_text,
                text=self.current_question.text
            )

            self.score_label.config(
                text=f"Score: {self.quiz.score}"
            )

            self.feedback_label.config(text="")

            self.true_button.config(state="normal")
            self.false_button.config(state="normal")

        else:
            self.show_final_score()

    def answer_question(self, user_answer):
        self.true_button.config(state="disabled")
        self.false_button.config(state="disabled")

        is_correct = self.quiz.check_answer(
            user_answer,
            self.current_question.answer
        )

        if is_correct:
            self.canvas.config(bg="#90EE90")
            self.feedback_label.config(text="Correct! Well done.")
        else:
            self.canvas.config(bg="#FF9999")
            self.feedback_label.config(text="Incorrect!")

        self.score_label.config(
            text=f"Score: {self.quiz.score}"
        )

        self.window.after(1000, self.get_next_question)

    def show_final_score(self):
        self.canvas.config(bg="white")

        self.canvas.itemconfig(
            self.question_text,
            text=(
                "Quiz Finished!\n\n"
                f"Your final score: {self.quiz.score}"
                f" / {len(self.quiz.question_list)}"
            )
        )

        self.true_button.config(state="disabled")
        self.false_button.config(state="disabled")
        self.feedback_label.config(text="Thank you for playing!")