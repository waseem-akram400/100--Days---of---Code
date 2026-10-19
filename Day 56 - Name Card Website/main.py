
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    # HTML template ko browser mein dikhana
    return render_template("index.html")


if __name__ == "__main__":
    # Development server start karna
    app.run(debug=True)
