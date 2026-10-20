from flask import Flask, render_template, request, redirect, url_for, flash
import os
import smtplib
from email.message import EmailMessage

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "day60-local-key")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        sender_email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not sender_email or not message:
            flash("Please fill in all fields.", "error")
            return redirect(url_for("contact"))

        smtp_host = os.environ.get("SMTP_ADDRESS")
        smtp_port = int(os.environ.get("SMTP_PORT", "587"))
        smtp_user = os.environ.get("SMTP_USER")
        smtp_password = os.environ.get("SMTP_PASSWORD")
        recipient = os.environ.get("CONTACT_EMAIL")

        if not all([smtp_host, smtp_user, smtp_password, recipient]):
            app.logger.info(
                "Contact form received: %s, %s, %s",
                name, sender_email, message
            )
            flash(
                "Form received, but email is not configured yet. "
                "See the Terminal for setup instructions.",
                "info"
            )
            return redirect(url_for("contact"))

        try:
            email = EmailMessage()
            email["Subject"] = f"Contact form message from {name}"
            email["From"] = smtp_user
            email["To"] = recipient
            email["Reply-To"] = sender_email
            email.set_content(
                f"Name: {name}\n"
                f"Email: {sender_email}\n\n"
                f"Message:\n{message}"
            )

            with smtplib.SMTP(smtp_host, smtp_port, timeout=20) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.send_message(email)

            flash("Your email was sent successfully!", "success")

        except (OSError, smtplib.SMTPException, ValueError):
            app.logger.exception("Email sending failed")
            flash("Email could not be sent. Check your SMTP settings.", "error")

        return redirect(url_for("contact"))

    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
