from flask import Flask, render_template

app = Flask(__name__)

# Dummy blog data
posts = [
    {
        "id": 1,
        "title": "میرا پہلا بلاگ",
        "subtitle": "100 Days of Code کا سفر",
        "body": "یہ Day 59 کا بلاگ پروجیکٹ ہے۔ یہ Flask سے بنایا گیا ہے۔"
    },
    {
        "id": 2,
        "title": "Flask سیکھنا آسان ہے",
        "subtitle": "Python سے ویب سائٹ بنانا",
        "body": "Flask ایک بہت ہی آسان اور طاقتور فریم ورک ہے۔"
    }
]

@app.route('/')
def home():
    return render_template("index.html", all_posts=posts)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/post/<int:post_id>')
def show_post(post_id):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == post_id:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)

if __name__ == "__main__":
    app.run(debug=True)