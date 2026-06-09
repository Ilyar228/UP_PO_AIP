import subprocess
import time
import urllib.request
import urllib.error
import json
import os
import sys

# Configurations
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Start Flask App
print("Starting Flask app in background...")
server_process = subprocess.Popen([sys.executable, "app.py"], cwd=BASE_DIR, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
time.sleep(1.5) # Wait for server to boot

# Helper function to send requests
def send_request(method, path, body=None, token=None):
    url = f"http://127.0.0.1:5000{path}"
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
        
    req_body_str = ""
    if body:
        req_body_str = json.dumps(body)
        data = req_body_str.encode('utf-8')
    else:
        data = None
        
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    
    start_time = time.time()
    try:
        with urllib.request.urlopen(req) as response:
            status_code = response.status
            resp_body = response.read().decode('utf-8')
            try:
                resp_json = json.loads(resp_body)
            except:
                resp_json = resp_body
            elapsed = int((time.time() - start_time) * 1000)
            return status_code, resp_json, req_body_str, headers, elapsed
    except urllib.error.HTTPError as e:
        status_code = e.code
        resp_body = e.read().decode('utf-8')
        try:
            resp_json = json.loads(resp_body)
        except:
            resp_json = resp_body
        elapsed = int((time.time() - start_time) * 1000)
        return status_code, resp_json, req_body_str, headers, elapsed

# Run the Integration Tests
results = []
try:
    # TC-INT-01: Step 1: Login
    print("Executing TC-INT-01 (Step 1): POST /api/auth/login")
    status, resp, req_body, hdrs, elapsed = send_request(
        "POST", "/api/auth/login", 
        body={"login": "user@test.com", "password": "Test1234!"}
    )
    token = resp.get("session_token")
    results.append({
        "tc_id": "TC-INT-01 (Step 1)",
        "method": "POST",
        "path": "/api/auth/login",
        "status": status,
        "response_body": resp,
        "title": "M1 Auth Login (Successful)"
    })
    
    # TC-INT-01: Step 3: Create Booking (Valid Token)
    print("Executing TC-INT-01 (Step 3): POST /api/booking/create")
    status, resp, req_body, hdrs, elapsed = send_request(
        "POST", "/api/booking/create", 
        body={"event_id": 5},
        token=token
    )
    booking_id_tc01 = resp.get("booking_id")
    results.append({
        "tc_id": "TC-INT-01 (Step 3)",
        "method": "POST",
        "path": "/api/booking/create",
        "status": status,
        "response_body": resp,
        "title": "M3 Booking Create (Valid Token, event_id=5)"
    })
    
    # TC-INT-02: M1 -> M3 (Invalid Token)
    print("Executing TC-INT-02: POST /api/booking/create with invalid token")
    status, resp, req_body, hdrs, elapsed = send_request(
        "POST", "/api/booking/create",
        body={"event_id": 5},
        token="INVALID_TOKEN_12345"
    )
    results.append({
        "tc_id": "TC-INT-02",
        "method": "POST",
        "path": "/api/booking/create",
        "status": status,
        "response_body": resp,
        "title": "M3 Booking Create (Invalid Token)"
    })
    
    # TC-INT-03: M2 -> M3 (Non-existing event) - BUG 1
    print("Executing TC-INT-03: POST /api/booking/create with non-existing event_id")
    status, resp, req_body, hdrs, elapsed = send_request(
        "POST", "/api/booking/create",
        body={"event_id": 99999},
        token=token
    )
    results.append({
        "tc_id": "TC-INT-03",
        "method": "POST",
        "path": "/api/booking/create",
        "status": status,
        "response_body": resp,
        "title": "M3 Booking Create (Non-existing event_id=99999) - BUG"
    })
    
    # TC-INT-04: Step 1: Pay booking (tok_test_valid)
    print("Executing TC-INT-04 (Step 1): POST /api/payment/pay")
    status, resp, req_body, hdrs, elapsed = send_request(
        "POST", "/api/payment/pay",
        body={"booking_id": booking_id_tc01, "card_token": "tok_test_valid"}
    )
    results.append({
        "tc_id": "TC-INT-04 (Step 1)",
        "method": "POST",
        "path": "/api/payment/pay",
        "status": status,
        "response_body": resp,
        "title": "M4 Payment Pay (Valid card_token)"
    })
    
    # TC-INT-04: Step 3: GET Booking details (Verify status updated to paid)
    print("Executing TC-INT-04 (Step 3): GET /api/booking/{booking_id}")
    status, resp, req_body, hdrs, elapsed = send_request(
        "GET", f"/api/booking/{booking_id_tc01}",
        token=token
    )
    results.append({
        "tc_id": "TC-INT-04 (Step 3)",
        "method": "GET",
        "path": f"/api/booking/{booking_id_tc01}",
        "status": status,
        "response_body": resp,
        "title": "M3 Booking Get Details (Verify status is paid)"
    })
    
    # TC-INT-05: Double payment - BUG 2
    print("Executing TC-INT-05: POST /api/payment/pay repeat payment")
    status, resp, req_body, hdrs, elapsed = send_request(
        "POST", "/api/payment/pay",
        body={"booking_id": booking_id_tc01, "card_token": "tok_test_valid"}
    )
    results.append({
        "tc_id": "TC-INT-05",
        "method": "POST",
        "path": "/api/payment/pay",
        "status": status,
        "response_body": resp,
        "title": "M4 Payment Pay (Double payment on paid booking) - BUG"
    })
    
    # TC-INT-06 Pre-step: Create a new booking for TC-INT-06
    print("Creating new booking for TC-INT-06...")
    _, temp_resp, _, _, _ = send_request(
        "POST", "/api/booking/create", 
        body={"event_id": 5},
        token=token
    )
    booking_id_tc06 = temp_resp.get("booking_id")
    print(f"Created new booking for TC-INT-06: booking_id={booking_id_tc06}")
    
    # TC-INT-06: Step 1: Pay booking (tok_test_decline)
    print("Executing TC-INT-06 (Step 1): POST /api/payment/pay decline")
    status, resp, req_body, hdrs, elapsed = send_request(
        "POST", "/api/payment/pay",
        body={"booking_id": booking_id_tc06, "card_token": "tok_test_decline"}
    )
    results.append({
        "tc_id": "TC-INT-06 (Step 1)",
        "method": "POST",
        "path": "/api/payment/pay",
        "status": status,
        "response_body": resp,
        "title": "M4 Payment Pay (Card declined)"
    })
    
    # TC-INT-06: Step 3: GET Booking details (Verify status failed) - BUG 3 (remains pending)
    print("Executing TC-INT-06 (Step 3): GET /api/booking/{booking_id}")
    status, resp, req_body, hdrs, elapsed = send_request(
        "GET", f"/api/booking/{booking_id_tc06}",
        token=token
    )
    results.append({
        "tc_id": "TC-INT-06 (Step 3)",
        "method": "GET",
        "path": f"/api/booking/{booking_id_tc06}",
        "status": status,
        "response_body": resp,
        "title": "M3 Booking Get Details (Verify status is failed) - BUG"
    })

finally:
    # Stop the background Flask server
    print("Stopping Flask app...")
    server_process.terminate()
    server_process.wait()

print("\n=== Integration Test Results ===")
for r in results:
    print(f"{r['tc_id']} - {r['title']}")
    print(f"  Method: {r['method']} {r['path']}")
    print(f"  Status: {r['status']}")
    print(f"  Response: {json.dumps(r['response_body'], ensure_ascii=False)}")
    print("-" * 50)
"""Запуск всех автотестов и сохранение вывода для отчёта."""

import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).parent
OUTPUT = BASE / "screenshots" / "autotest_output.txt"


def main() -> int:
    scripts = ["test_calculator.py", "test_webapp.py"]
    lines: list[str] = []

    for script in scripts:
        lines.append(f"=== {script} ===")
        result = subprocess.run(
            [sys.executable, str(BASE / script)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        lines.append(result.stdout)
        if result.stderr:
            lines.append(result.stderr)

    OUTPUT.parent.mkdir(exist_ok=True)
    text = "\n".join(lines)
    OUTPUT.write_text(text, encoding="utf-8")
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode("utf-8", errors="replace").decode("cp1251", errors="replace"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
