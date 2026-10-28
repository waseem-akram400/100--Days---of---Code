from flask import Flask, render_template, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "change-this-development-key"

PRODUCTS = [
    {"id": 1, "name": "Wireless Headphones", "price": 4500, "emoji": "🎧", "description": "Enjoy your favourite music."},
    {"id": 2, "name": "Smart Watch", "price": 6500, "emoji": "⌚", "description": "Keep track of your daily activity."},
    {"id": 3, "name": "Coffee Mug", "price": 850, "emoji": "☕", "description": "A perfect mug for your coffee."},
    {"id": 4, "name": "Backpack", "price": 3200, "emoji": "🎒", "description": "A useful bag for everyday travel."},
    {"id": 5, "name": "Desk Lamp", "price": 1800, "emoji": "💡", "description": "Brighten up your workspace."},
    {"id": 6, "name": "Camera", "price": 18500, "emoji": "📷", "description": "Capture your favourite moments."},
]


def get_product(product_id):
    for product in PRODUCTS:
        if product["id"] == product_id:
            return product
    return None


@app.context_processor
def cart_count():
    cart = session.get("cart", {})
    return {"cart_count": sum(cart.values())}


@app.route("/")
def home():
    return render_template("index.html", products=PRODUCTS)


@app.route("/add/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    product = get_product(product_id)

    if product is None:
        flash("Product nahi mila.")
        return redirect(url_for("home"))

    cart = session.get("cart", {})
    key = str(product_id)
    cart[key] = cart.get(key, 0) + 1
    session["cart"] = cart

    flash(f'{product["name"]} cart mein add ho gaya!')
    return redirect(url_for("home"))


@app.route("/cart")
def view_cart():
    cart = session.get("cart", {})
    items = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_product(int(product_id))
        if product:
            subtotal = product["price"] * quantity
            items.append({
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal
            })
            total += subtotal

    return render_template("cart.html", items=items, total=total)


@app.route("/remove/<int:product_id>", methods=["POST"])
def remove_from_cart(product_id):
    cart = session.get("cart", {})
    cart.pop(str(product_id), None)
    session["cart"] = cart
    flash("Product cart se remove kar diya gaya.")
    return redirect(url_for("view_cart"))


@app.route("/checkout", methods=["POST"])
def checkout():
    cart = session.get("cart", {})

    if not cart:
        flash("Aap ka cart khaali hai.")
        return redirect(url_for("view_cart"))

    session["cart"] = {}
    flash("Demo order place ho gaya! Yeh sirf practice checkout hai.")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
