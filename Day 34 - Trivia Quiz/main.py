
from data import get_questions
from question_model import Question
from quiz_brain import QuizBrain
from ui import QuizInterface


question_data = get_questions()

question_bank = [
    Question(
        text=item["question"],
        answer=item["correct_answer"]
    )
    for item in question_data
]

quiz = QuizBrain(question_bank)
quiz_ui = QuizInterface(quiz)