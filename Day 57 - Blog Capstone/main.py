
from flask import Flask, render_template, abort, url_for

app = Flask(__name__)

# Blog posts ka sample data
posts = [
    {
        "id": 1,
        "title": "Learning Python",
        "subtitle": "My journey into programming",
        "author": "Waseem Akram",
        "body": "Python is a beginner-friendly programming language. "
                "I am learning variables, functions, loops, Flask, and HTML."
    },
    {
        "id": 2,
        "title": "My First Flask Website",
        "subtitle": "Building websites with Python",
        "author": "Waseem Akram",
        "body": "Flask helps us build web applications with Python. "
                "Jinja allows us to display dynamic content inside HTML templates."
    },
    {
        "id": 3,
        "title": "Understanding Jinja",
        "subtitle": "Dynamic HTML made simple",
        "author": "Waseem Akram",
        "body": "Jinja uses double curly braces to display values and "
                "percent-delimited tags to run template logic."
    }
]


@app.route("/")
def home():
    # Tamam blog posts homepage par dikhayen
    return render_template("index.html", posts=posts)


@app.route("/post/<int:post_id>")
def show_post(post_id):
    # ID ke mutabiq post dhoondhna
    selected_post = next(
        (post for post in posts if post["id"] == post_id),
        None
    )

    # Agar post mojood na ho to 404 error
    if selected_post is None:
        abort(404)

    return render_template("post.html", post=selected_post)


if __name__ == "__main__":
    app.run(debug=True)
