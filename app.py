from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/rooms')
def rooms():
    return render_template('rooms.html')

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/booking", methods=["GET", "POST"])
def booking():
    selected_room = request.args.get("room")

    if request.method == "POST":
        return redirect(url_for("thank_you"))

    return render_template("booking.html", room=selected_room)


@app.route("/thank-you")
def thank_you():
    return render_template("thank_you.html")


