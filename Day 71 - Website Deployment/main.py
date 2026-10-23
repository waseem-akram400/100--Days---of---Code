import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Secret information is supplied through environment variables.
app.config["SECRET_KEY"] = os.environ.get(
    "FLASK_SECRET_KEY", "local-development-key-only"
)

# Use PostgreSQL on the hosting server, or SQLite locally.
database_url = os.environ.get("DATABASE_URL", "sqlite:///blog.db")

# Some hosting services supply postgres:// URLs.
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)


@app.route("/")
def home():
    posts = db.session.execute(
        db.select(BlogPost).order_by(BlogPost.id.desc())
    ).scalars().all()
    return render_template("index.html", posts=posts)


@app.route("/new", methods=["GET", "POST"])
def new_post():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()

        if not title or not content:
            flash("Please enter both a title and content.", "error")
            return render_template("new_post.html")

        post = BlogPost(title=title, content=content)
        db.session.add(post)
        db.session.commit()

        flash("Your post was published!", "success")
        return redirect(url_for("home"))

    return render_template("new_post.html")


@app.route("/health")
def health():
    # A simple endpoint for checking that the web service responds.
    return {"status": "ok"}, 200


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
