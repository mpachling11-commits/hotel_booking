from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "admin123"

# ---------------- ROOM CAPACITY ----------------
ROOM_CAPACITY = {
    "Deluxe": 10,
    "Luxury": 6,
    "Suite": 3
}

# ---------------- TEMP BOOKING STORAGE ----------------
bookings = []

# ---------------- DATE RANGE FUNCTION ----------------
def date_range(start, end):
    start_date = datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.strptime(end, "%Y-%m-%d")
    dates = []

    while start_date < end_date:
        dates.append(start_date.strftime("%Y-%m-%d"))
        start_date += timedelta(days=1)

    return dates

# ---------------- AVAILABILITY CHECK ----------------
def is_room_available(room_type, check_in, check_out):
    booked_per_day = {}

    for booking in bookings:
        if booking["room_type"] == room_type:
            for d in date_range(booking["check_in"], booking["check_out"]):
                booked_per_day[d] = booked_per_day.get(d, 0) + 1

    for d in date_range(check_in, check_out):
        if booked_per_day.get(d, 0) >= ROOM_CAPACITY[room_type]:
            return False

    return True

# ---------------- OWNER AVAILABILITY ----------------
def availability_by_date():
    availability = {room: {} for room in ROOM_CAPACITY}

    for booking in bookings:
        room = booking["room_type"]
        for d in date_range(booking["check_in"], booking["check_out"]):
            availability[room][d] = availability[room].get(d, 0) + 1

    return availability

# ---------------- ROUTES ----------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/rooms")
def rooms():
    return render_template("rooms.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/booking")
def booking():
    return render_template("booking.html", room="")

@app.route("/book", methods=["POST"])
def book_room():
    name = request.form["name"]
    room_type = request.form["room_type"]
    check_in = request.form["check_in"]
    check_out = request.form["check_out"]

    if not is_room_available(room_type, check_in, check_out):
        return "<h2>Room not available for selected dates</h2>"

    bookings.append({
        "name": name,
        "room_type": room_type,
        "check_in": check_in,
        "check_out": check_out
    })

    return redirect(url_for("thank_you"))

@app.route("/thank-you")
def thank_you():
    return render_template("thank_you.html")

# ---------------- ADMIN LOGIN ----------------
@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "admin123":
            session["admin"] = True
            return redirect(url_for("dashboard"))
        else:
            return "Invalid credentials"

    return render_template("admin_login.html")

# ---------------- OWNER DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    availability = availability_by_date()
    return render_template(
        "dashboard.html",
        bookings=bookings,
        availability=availability,
        room_capacity=ROOM_CAPACITY
    )

@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("index"))

# ---------------- RUN (RENDER SAFE) ----------------
if __name__ == "__main__":
    app.run()

