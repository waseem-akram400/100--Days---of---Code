from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path

app = Flask(__name__)

# Database ki file isi project folder mein save hogi
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + str(
    Path(__file__).resolve().parent / "movies.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# Har movie ka record
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    year = db.Column(db.Integer, nullable=True)
    description = db.Column(db.Text, nullable=True)
    rating = db.Column(db.Float, nullable=True)
    review = db.Column(db.Text, nullable=True)
    img_url = db.Column(db.String(500), nullable=True)


# Requirement 1 and 5: Movies ko rating ke mutabiq dikhana
@app.route("/")
def home():
    movies = db.session.execute(
        db.select(Movie).order_by(
            Movie.rating.desc().nullslast(),
            Movie.title.asc()
        )
    ).scalars().all()

    return render_template("index.html", movies=movies)


# Requirement 2: Rating aur review edit karna
@app.route("/edit/<int:movie_id>", methods=["GET", "POST"])
def edit_movie(movie_id):
    movie = db.get_or_404(Movie, movie_id)

    if request.method == "POST":
        rating_text = request.form.get("rating", "").strip()

        try:
            rating = float(rating_text)
            if not 0 <= rating <= 10:
                return "Rating 0 se 10 ke darmiyan honi chahiye.", 400
        except ValueError:
            return "Barah-e-karam durust rating likhein.", 400

        movie.rating = rating
        movie.review = request.form.get("review", "").strip()
        db.session.commit()

        return redirect(url_for("home"))

    return render_template("edit.html", movie=movie)


# Requirement 3: Movie delete karna
@app.route("/delete/<int:movie_id>", methods=["POST"])
def delete_movie(movie_id):
    movie = db.get_or_404(Movie, movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for("home"))


# Requirement 4: Nayi movie add karna
@app.route("/add", methods=["GET", "POST"])
def add_movie():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        year_text = request.form.get("year", "").strip()
        description = request.form.get("description", "").strip()
        img_url = request.form.get("img_url", "").strip()

        if not title:
            return "Movie ka title zaroor likhein.", 400

        try:
            year = int(year_text) if year_text else None
        except ValueError:
            return "Year durust number hona chahiye.", 400

        new_movie = Movie(
            title=title,
            year=year,
            description=description,
            img_url=img_url,
            rating=None,
            review=None
        )

        db.session.add(new_movie)
        db.session.commit()

        return redirect(url_for("edit_movie", movie_id=new_movie.id))

    return render_template("add.html")


# Pehli baar database aur table banayein
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
