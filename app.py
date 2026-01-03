from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('booking.html')

@app.route('/book', methods=['POST'])
def book():
    name = request.form['name']
    email = request.form['email']
    room = request.form['room']
    checkin = request.form['checkin']
    checkout = request.form['checkout']

    return f"""
    <h2>Booking Confirmed!</h2>
    <p>Name: {name}</p>
    <p>Email: {email}</p>
    <p>Room: {room}</p>
    <p>Check-in: {checkin}</p>
    <p>Check-out: {checkout}</p>
    """

# REQUIRED FOR RENDER
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
