from flask import Flask, render_template, request, redirect, url_for
import json
import os
import uuid

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), "tasks.json")


def load_tasks():
    """فائل سے کام پڑھیں؛ فائل نہ ہو تو خالی فہرست دیں۔"""
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def save_tasks(tasks):
    """تمام کام JSON فائل میں محفوظ کریں۔"""
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(tasks, file, ensure_ascii=False, indent=4)


@app.route("/")
def home():
    tasks = load_tasks()
    total = len(tasks)
    completed = sum(1 for task in tasks if task["done"])
    remaining = total - completed

    return render_template(
        "index.html",
        tasks=tasks,
        total=total,
        completed=completed,
        remaining=remaining
    )


@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title", "").strip()

    if title:
        tasks = load_tasks()
        tasks.append({
            "id": str(uuid.uuid4()),
            "title": title,
            "done": False
        })
        save_tasks(tasks)

    return redirect(url_for("home"))


@app.route("/toggle/<task_id>", methods=["POST"])
def toggle_task(task_id):
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            task["done"] = not task["done"]
            break

    save_tasks(tasks)
    return redirect(url_for("home"))


@app.route("/delete/<task_id>", methods=["POST"])
def delete_task(task_id):
    tasks = load_tasks()
    tasks = [task for task in tasks if task["id"] != task_id]
    save_tasks(tasks)

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
