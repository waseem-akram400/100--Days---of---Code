from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path

app = Flask(__name__)

# Database ki file isi project folder mein banegi
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + str(
    Path(__file__).resolve().parent / "books-collection.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# Database mein har kitab ka record
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    author = db.Column(db.String(150), nullable=False)
    rating = db.Column(db.Float, nullable=False)


@app.route("/")
def home():
    books = db.session.execute(
        db.select(Book).order_by(Book.title)
    ).scalars().all()
    return render_template("index.html", books=books)


@app.route("/add", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip()
        rating_text = request.form.get("rating", "").strip()

        if not title or not author or not rating_text:
            return "Please fill in all fields.", 400

        try:
            rating = float(rating_text)
            if not 0 <= rating <= 10:
                return "Rating must be between 0 and 10.", 400
        except ValueError:
            return "Rating must be a number.", 400

        new_book = Book(title=title, author=author, rating=rating)
        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for("home"))

    return render_template("add.html")


@app.route("/edit/<int:book_id>", methods=["GET", "POST"])
def edit_book(book_id):
    book = db.get_or_404(Book, book_id)

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip()
        rating_text = request.form.get("rating", "").strip()

        if not title or not author or not rating_text:
            return "Please fill in all fields.", 400

        try:
            rating = float(rating_text)
            if not 0 <= rating <= 10:
                return "Rating must be between 0 and 10.", 400
        except ValueError:
            return "Rating must be a number.", 400

        book.title = title
        book.author = author
        book.rating = rating
        db.session.commit()

        return redirect(url_for("home"))

    return render_template("edit.html", book=book)


@app.route("/delete/<int:book_id>", methods=["POST"])
def delete_book(book_id):
    book = db.get_or_404(Book, book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for("home"))


# Database aur table pehli baar zaroor banayein
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
