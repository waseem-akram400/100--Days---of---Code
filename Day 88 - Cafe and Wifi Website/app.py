from flask import Flask, render_template, request, redirect, url_for
import csv
import os

app = Flask(__name__)

CSV_FILE = os.path.join(os.path.dirname(__file__), "cafes.csv")

FIELDS = [
    "name", "location", "map_url", "open_time", "close_time",
    "coffee", "wifi", "power"
]


def create_csv():
    """اگر CSV فائل موجود نہیں تو نئی فائل بنائیں۔"""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerow({
                "name": "Example Cafe",
                "location": "Multan, Pakistan",
                "map_url": "https://maps.google.com/",
                "open_time": "9:00 AM",
                "close_time": "10:00 PM",
                "coffee": "☕☕☕",
                "wifi": "Yes",
                "power": "Yes"
            })


def get_cafes():
    create_csv()
    with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


@app.route("/")
def home():
    cafes = get_cafes()
    return render_template("index.html", cafes=cafes)


@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    if request.method == "POST":
        cafe = {
            "name": request.form.get("name", "").strip(),
            "location": request.form.get("location", "").strip(),
            "map_url": request.form.get("map_url", "").strip(),
            "open_time": request.form.get("open_time", "").strip(),
            "close_time": request.form.get("close_time", "").strip(),
            "coffee": request.form.get("coffee", "☕☕☕"),
            "wifi": request.form.get("wifi", "Yes"),
            "power": request.form.get("power", "Yes")
        }

        if not cafe["name"] or not cafe["location"]:
            return render_template(
                "add.html",
                error="Please enter both the cafe name and location."
            )

        create_csv()
        with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDS)
            writer.writerow(cafe)

        return redirect(url_for("home"))

    return render_template("add.html", error=None)


if __name__ == "__main__":
    create_csv()
    app.run(debug=True)
