from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, URL, NumberRange
from wtforms import IntegerField
import csv
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get(
    "FLASK_SECRET_KEY", "day62-local-development-key"
)

CSV_FILE = os.path.join(app.root_path, "cafes.csv")

FIELDS = [
    "Cafe Name",
    "Location",
    "Open",
    "Close",
    "Coffee Rating",
    "Wifi Rating",
    "Power Rating",
    "Cafe URL",
]


class CafeForm(FlaskForm):
    cafe_name = StringField("Cafe Name", validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired(), URL()])
    open_time = StringField("Opening Time", validators=[DataRequired()])
    close_time = StringField("Closing Time", validators=[DataRequired()])
    coffee_rating = SelectField(
        "Coffee Rating",
        choices=[("☕", "☕"), ("☕☕", "☕☕"), ("☕☕☕", "☕☕☕"),
                 ("☕☕☕☕", "☕☕☕☕"), ("☕☕☕☕☕", "☕☕☕☕☕")],
        validators=[DataRequired()]
    )
    wifi_rating = SelectField(
        "WiFi Rating",
        choices=[("✘", "✘"), ("💪", "💪"), ("💪💪", "💪💪"),
                 ("💪💪💪", "💪💪💪"), ("💪💪💪💪", "💪💪💪💪"),
                 ("💪💪💪💪💪", "💪💪💪💪💪")],
        validators=[DataRequired()]
    )
    power_rating = SelectField(
        "Power Socket Rating",
        choices=[("✘", "✘"), ("🔌", "🔌"), ("🔌🔌", "🔌🔌"),
                 ("🔌🔌🔌", "🔌🔌🔌"), ("🔌🔌🔌🔌", "🔌🔌🔌🔌"),
                 ("🔌🔌🔌🔌🔌", "🔌🔌🔌🔌🔌")],
        validators=[DataRequired()]
    )
    submit = SubmitField("Add Cafe")


def read_cafes():
    if not os.path.exists(CSV_FILE):
        return []
    with open(CSV_FILE, newline="", encoding="utf-8-sig") as file:
        return list(csv.DictReader(file))


def save_cafe(cafe):
    file_exists = os.path.exists(CSV_FILE)
    with open(CSV_FILE, "a", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        if not file_exists or os.path.getsize(CSV_FILE) == 0:
            writer.writeheader()
        writer.writerow(cafe)


@app.route("/")
def home():
    return render_template("index.html", cafes=read_cafes())


@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        cafe = {
            "Cafe Name": form.cafe_name.data,
            "Location": form.location.data,
            "Open": form.open_time.data,
            "Close": form.close_time.data,
            "Coffee Rating": form.coffee_rating.data,
            "Wifi Rating": form.wifi_rating.data,
            "Power Rating": form.power_rating.data,
            "Cafe URL": form.location.data,
        }
        save_cafe(cafe)
        flash("Cafe added successfully!", "success")
        return redirect(url_for("home"))
    return render_template("add.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
