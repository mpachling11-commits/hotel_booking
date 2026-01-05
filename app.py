from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "admin123"

# Temporary storage (no database for now)
bookings = []

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")

# ---------------- ROOMS ----------------
@app.route("/rooms")
def rooms():
    return render_template("rooms.html")

# ---------------- CONTACT ----------------
@app.route("/contact")
def contact():
    return render_template("contact.html")

# ---------------- BOOKING ----------------
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

        bookings.append(booking_data)

        return render_template("thank_you.html", data=booking_data)

    return render_template("booking.html", room=selected_room)

# ---------------- THANK YOU ----------------
@app.route("/thank-you")
def thank_you():
    return render_template("thank_you.html", data=None)

# ---------------- ADMIN LOGIN ----------------
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "1234":
            session["admin"] = True
            return redirect(url_for("dashboard"))

    return render_template("admin_login.html")

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if not session.get("admin"):
        return redirect(url_for("admin"))

    return render_template("dashboard.html", bookings=bookings)

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
