
import json
from urllib.request import Request, urlopen
from html import unescape


def get_questions():
    url = "https://opentdb.com/api.php?amount=10&type=boolean"

    try:
        request = Request(
            url,
            headers={"User-Agent": "PythonTriviaQuiz/1.0"}
        )

        with urlopen(request, timeout=10) as response:
            result = json.loads(response.read().decode("utf-8"))

        if result.get("response_code") != 0:
            raise ValueError("API did not return questions.")

        questions = result.get("results", [])

        if not questions:
            raise ValueError("No questions received.")

        cleaned_questions = []

        for item in questions:
            cleaned_questions.append({
                "question": unescape(item["question"]),
                "correct_answer": item["correct_answer"]
            })

        return cleaned_questions

    except Exception as error:
        print("Online questions could not be loaded:", error)
        print("Using saved questions instead.")

        return [
            {
                "question": "The Sun is a star.",
                "correct_answer": "True"
            },
            {
                "question": "Fish can live without water.",
                "correct_answer": "False"
            },
            {
                "question": "Python is a programming language.",
                "correct_answer": "True"
            },
            {
                "question": "The Earth is flat.",
                "correct_answer": "False"
            },
            {
                "question": "A week has seven days.",
                "correct_answer": "True"
            },
            {
                "question": "The Moon is a star.",
                "correct_answer": "False"
            },
            {
                "question": "Water freezes at 0 degrees Celsius under standard pressure.",
                "correct_answer": "True"
            },
            {
                "question": "There are 100 minutes in one hour.",
                "correct_answer": "False"
            },
            {
                "question": "Humans need oxygen to survive.",
                "correct_answer": "True"
            },
            {
                "question": "The Python list index starts at 1.",
                "correct_answer": "False"
            }
        ]