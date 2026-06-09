from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory database
bookings = {}
events = {1: "Concert", 2: "Theater", 3: "Cinema", 4: "Opera", 5: "Rock Festival"}
valid_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjEsImV4cCI6MTcxNzk1ODAwMH0.abc123xyz_token_here"

# Seed booking for TC-INT-01 step 3 (will be overwritten if created dynamically)
bookings[1042] = {
    "booking_id": 1042,
    "booking_status": "pending",
    "event_id": 5
}

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json or {}
    username = data.get('login')
    password = data.get('password') or data.get('pass')
    if username == "user@test.com" and password == "Test1234!":
        return jsonify({"session_token": valid_token}), 200
    return jsonify({"error": "Unauthorized", "message": "Invalid login or password"}), 401

@app.route('/api/booking/create', methods=['POST'])
def create_booking():
    # Check token
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith("Bearer "):
        return jsonify({"error": "Unauthorized", "message": "Missing or malformed session token"}), 401
    
    token = auth_header.split(" ")[1]
    if token != valid_token:
        return jsonify({"error": "Unauthorized", "message": f"Invalid session token: {token}"}), 401
    
    data = request.json or {}
    event_id = data.get('event_id')
    if event_id is None:
        return jsonify({"error": "Bad Request", "message": "Missing event_id"}), 400
        
    # BUG-001: M3 Booking does not verify if event_id exists in M2 Catalog
    # Expected behavior: if event_id not in events, return 404
    # But because of the bug, we allow creating bookings for any event_id (e.g. 99999)
    # So we do NOT check, except we can log it or just create it.
    
    booking_id = 1042 + len(bookings)
    # If 1042 is already there and we are creating booking for event 5, reuse 1042
    if event_id == 5 and 1042 in bookings and bookings[1042]["booking_status"] == "pending":
        booking_id = 1042
    elif event_id == 99999:
        booking_id = 1043  # Force 1043 for the invalid event bug
    
    new_booking = {
        "booking_id": booking_id,
        "booking_status": "pending",
        "event_id": event_id
    }
    bookings[booking_id] = new_booking
    return jsonify(new_booking), 200

@app.route('/api/payment/pay', methods=['POST'])
def pay_booking():
    data = request.json or {}
    booking_id = data.get('booking_id')
    card_token = data.get('card_token')
    
    if booking_id not in bookings:
        return jsonify({"error": "Not Found", "message": "Booking not found"}), 404
        
    booking = bookings[booking_id]
    
    # BUG-002: M4 Payment does not check if the booking is already paid
    # Expected behavior: if booking["booking_status"] == "paid", return 409 Conflict
    # But because of the bug, we allow double payment and process it again!
    # So we do NOT check if status is paid.
    
    if card_token == "tok_test_valid":
        booking["booking_status"] = "paid"
        return jsonify({"payment_status": "success", "transaction_id": f"tx_88321042"}), 200
        
    elif card_token == "tok_test_decline":
        # BUG-003: M4 fails to update M3 booking status to failed when payment is declined
        # Expected behavior: booking["booking_status"] = "failed"
        # But because of the bug, we leave it as "pending"
        return jsonify({"error": "Payment Declined", "message": "Card declined", "payment_status": "declined"}), 402
        
    return jsonify({"error": "Bad Request", "message": "Invalid card token"}), 400

@app.route('/api/booking/<int:booking_id>', methods=['GET'])
def get_booking(booking_id):
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith("Bearer ") or auth_header.split(" ")[1] != valid_token:
        return jsonify({"error": "Unauthorized", "message": "Invalid session token"}), 401
        
    if booking_id not in bookings:
        return jsonify({"error": "Not Found", "message": "Booking not found"}), 404
        
    return jsonify(bookings[booking_id]), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)
"""WebCalc — веб-калькулятор на Flask (вся логика на Python)."""

from flask import Flask, redirect, render_template, request, session, url_for

from calculator_ui import CalculatorState

app = Flask(__name__)
app.secret_key = "webcalc-dev-key"


def _get_state() -> CalculatorState:
    return CalculatorState.from_dict(session.get("calc"))


def _save_state(state: CalculatorState) -> None:
    session["calc"] = state.to_dict()


@app.route("/", methods=["GET", "POST"])
def index():
    state = _get_state()

    if request.method == "POST":
        action = request.form.get("action", "")
        value = request.form.get("value")
        try:
            state.handle(action, value)
        except ValueError:
            state.error = "Некорректное действие"
        _save_state(state)
        return redirect(url_for("index"))

    return render_template(
        "index.html",
        display=state.display(),
        error=state.error,
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
