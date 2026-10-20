from flask import Flask, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

app = Flask(__name__)
app.config["SECRET_KEY"] = "replace-this-with-a-private-secret-key"


class ContactForm(FlaskForm):
    name = StringField(
        "Your Name",
        validators=[DataRequired(), Length(min=2, max=50)]
    )

    email = EmailField(
        "Your Email",
        validators=[DataRequired(), Email()]
    )

    message = TextAreaField(
        "Your Message",
        validators=[DataRequired(), Length(min=10, max=1000)]
    )

    submit = SubmitField("Send Message")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data

        # For this lesson, display the submitted data on the result page.
        return render_template(
            "success.html",
            name=name,
            email=email,
            message=message
        )

    return render_template("contact.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
