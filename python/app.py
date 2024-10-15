import logging
from flask import Flask, request, jsonify
from email_sender import EmailSender
from email_templates import EmailTemplates

import system
import booking
import consts

app = Flask(__name__)


# Utility function to validate request data and return required fields
def validate_request(data, required_fields):
    missing_fields = [
        field for field in required_fields if field not in data or not data.get(field)
    ]
    if missing_fields:
        return False, f"Missing fields: {', '.join(missing_fields)}"
    return True, {field: data.get(field) for field in required_fields}


# curl -X POST http://localhost:5000/send-email -H "Content-Type: application/json" -d "{\"recipient_email\": \"346225483@qq.com\", \"email_type\": \"registration_success\"}"
@app.route("/send-email", methods=["POST"])
def send_email():
    try:
        # Get JSON data from the request
        data = request.json

        # Validate common fields
        valid, result = validate_request(data, ["recipient_email", "email_type"])
        if not valid:
            return jsonify({"error": result}), 400

        recipient_email = result["recipient_email"]
        email_type = result["email_type"]

        # Handle different email types
        if email_type == "registration_success":
            message = EmailTemplates.get_registration_success_message(recipient_email)

        elif email_type == "order_submission":
            # Validate fields required for order_submission
            valid, result = validate_request(data, ["order_id", "email_name"])
            if not valid:
                return jsonify({"error": result}), 400

            message = EmailTemplates.get_order_submission_message(
                recipient_email,
                {"order_id": result["order_id"], "name": result["email_name"]},
            )

        elif email_type == "order_status_change":
            # Validate fields required for order_status_change
            valid, result = validate_request(data, ["status"])
            if not valid:
                return jsonify({"error": result}), 400

            message = EmailTemplates.get_order_status_change_message(
                recipient_email, result["status"]
            )

        else:
            return jsonify({"error": "Invalid email type"}), 400

        # Send the email using EmailSender
        EmailSender.send_email(recipient_email, message)

        return jsonify({"message": "Email sent successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



'''
DESCRIPTION: booking cancellation

url: http://localhost:5001/booking-cancellation
method: POST
body:
{
    "customer_email": "test@gmail.com",
    "tour": "tour1"
}

response:
{
    "code":0,
    "message": "modify success"
}

curl command:
    curl -X POST http://localhost:5001/booking-cancellation -H "Content-Type: application/json" -d "{\"customer_email\": \"test@gmail.com\", \"tour\": \"tour1\"}"
    

'''
@app.route("/booking-cancellation", methods=["POST"])
def booking_cancellation():
    try:
        # Get JSON data from the request
        data = request.json

        # Validate common fields
        valid, result = validate_request(data, ["customer_email", "tour"])
        if not valid:
            logging.error(f"validate_request failed: {result}, data: {data}")
            return jsonify({"error": result}), 400

        customer_email = result["customer_email"]
        tour = result["tour"]

        bookingopt = booking.booking_operation()

        result = bookingopt.update_booking_status(customer_email, tour, consts.BOOKING_STATUS_CANCELLED)
        if result == True:
            return jsonify({"code":0,"message": "modify success"}), 200
        else:
            return jsonify({"code":1,"message": "modify failed"}), 200


    except Exception as e:
        return jsonify({"error": str(e)}), 500





if __name__ == "__main__":
    system.init_log()
    app.run(host="0.0.0.0", port=5000)
