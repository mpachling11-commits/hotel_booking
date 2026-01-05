from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Temporary storage (no database for now)
bookings = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/rooms")
def rooms():
    return render_template("rooms.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/booking", methods=["GET", "POST"])
def booking():
    selected_room = request.args.get("room")

    if request.method == "POST":
        booking_data = {
            "name": request.form["name"],
            "email": request.form["email"],
            "room": request.form["room"],
            "checkin": request.form["checkin"],
            "checkout": request.form["checkout"]
        }

        # Store booking temporarily
        bookings.append(booking_data)

        return render_template("thank_you.html", data=booking_data)

    return render_template("booking.html", room=selected_room)

@app.route("/admin")
def admin_dashboard():
    return render_template("dashboard.html", bookings=bookings)

@app.route("/thank-you")
def thank_you():
    # fallback page if someone directly opens URL
    return render_template("thank_you.html", data=None)

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


