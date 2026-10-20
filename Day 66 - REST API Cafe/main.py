from flask import Flask, jsonify, request
import csv
import os
import random
import uuid

app = Flask(__name__)

# Data file aur API key
DATA_FILE = os.path.join(os.path.dirname(__file__), "cafes.csv")
API_KEY = "my-secret-api-key"

FIELDS = [
    "id", "name", "map_url", "img_url", "location", "seats",
    "has_toilet", "has_wifi", "has_sockets", "can_take_calls",
    "coffee_price"
]


def read_cafes():
    """CSV file se tamam cafes parhna."""
    with open(DATA_FILE, "r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def save_cafes(cafes):
    """Updated cafes ko CSV file mein save karna."""
    with open(DATA_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(cafes)


def error_response(message, status_code):
    return jsonify({"error": message}), status_code


# GET: Ek random cafe
@app.route("/random", methods=["GET"])
def random_cafe():
    cafes = read_cafes()

    if not cafes:
        return error_response("No cafes found.", 404)

    return jsonify(cafe=random.choice(cafes)), 200


# GET: Tamam cafes
@app.route("/all", methods=["GET"])
def all_cafes():
    return jsonify(cafes=read_cafes()), 200


# GET: Naam ya location se cafe dhoondhna
@app.route("/search", methods=["GET"])
def search_cafe():
    query = request.args.get("name", "").strip().lower()

    if not query:
        return error_response("Please provide ?name= cafe name or location.", 400)

    cafes = read_cafes()
    matches = [
        cafe for cafe in cafes
        if query in cafe["name"].lower()
        or query in cafe["location"].lower()
    ]

    if not matches:
        return error_response("No matching cafe found.", 404)

    return jsonify(cafes=matches), 200


# POST: Naya cafe add karna
@app.route("/add", methods=["POST"])
def add_cafe():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return error_response("Please send a valid JSON object.", 400)

    name = str(data.get("name", "")).strip()
    location = str(data.get("location", "")).strip()

    if not name or not location:
        return error_response("Cafe name and location are required.", 400)

    cafes = read_cafes()

    new_cafe = {field: "" for field in FIELDS}
    new_cafe.update(data)
    new_cafe["id"] = str(uuid.uuid4())
    new_cafe["name"] = name
    new_cafe["location"] = location

    # Sirf allowed fields CSV mein save hongi
    new_cafe = {field: str(new_cafe.get(field, "")) for field in FIELDS}

    cafes.append(new_cafe)
    save_cafes(cafes)

    return jsonify(
        message="Cafe added successfully.",
        cafe=new_cafe
    ), 201


# PATCH: Cafe ki coffee price update karna
@app.route("/update-price/<cafe_id>", methods=["PATCH"])
def update_price(cafe_id):
    data = request.get_json(silent=True)

    if not isinstance(data, dict) or "coffee_price" not in data:
        return error_response("Send coffee_price in JSON.", 400)

    price = str(data["coffee_price"]).strip()

    if not price:
        return error_response("Coffee price cannot be empty.", 400)

    cafes = read_cafes()

    for cafe in cafes:
        if cafe["id"] == cafe_id:
            cafe["coffee_price"] = price
            save_cafes(cafes)
            return jsonify(
                message="Coffee price updated.",
                cafe=cafe
            ), 200

    return error_response("Cafe not found.", 404)


# DELETE: API key ke zariye cafe delete karna
@app.route("/report-closed/<cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    supplied_key = request.args.get("api-key", "")

    if supplied_key != API_KEY:
        return error_response("Invalid or missing API key.", 403)

    cafes = read_cafes()
    remaining = [cafe for cafe in cafes if cafe["id"] != cafe_id]

    if len(remaining) == len(cafes):
        return error_response("Cafe not found.", 404)

    save_cafes(remaining)

    return jsonify(message="Cafe deleted successfully."), 200


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Welcome to the Cafe REST API!",
        "endpoints": {
            "random_cafe": "GET /random",
            "all_cafes": "GET /all",
            "search": "GET /search?name=multan",
            "add_cafe": "POST /add",
            "update_price": "PATCH /update-price/<cafe_id>",
            "delete_cafe": "DELETE /report-closed/<cafe_id>?api-key=my-secret-api-key"
        }
    }), 200


if __name__ == "__main__":
    app.run(debug=True)
