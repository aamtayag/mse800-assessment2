from flask import Flask, request, jsonify
from email_sender import EmailSender
from email_templates import EmailTemplates


app = Flask(__name__)


# curl -X POST http://localhost:5000/send-email -H "Content-Type: application/json" -d "{\"recipient_email\": \"346225483@qq.com\", \"email_type\": \"registration_success\"}"
@app.route("/send-email", methods=["POST"])
def send_email():
    try:
        # Get JSON data from the request
        data = request.json
        recipient_email = data.get("recipient_email")
        email_type = data.get("email_type")
        status = data.get(
            "status", ""
        )  # Optional, only needed for status change emails

        # Check the email type and create the corresponding message
        if email_type == "registration_success":
            message = EmailTemplates.get_registration_success_message(recipient_email)
        elif email_type == "order_submission":
            message = EmailTemplates.get_order_submission_message(recipient_email)
        elif email_type == "order_status_change":
            if not status:
                return (
                    jsonify(
                        {
                            "error": "Missing 'status' field for order_status_change email"
                        }
                    ),
                    400,
                )
            message = EmailTemplates.get_order_status_change_message(
                recipient_email, status
            )
        else:
            return jsonify({"error": "Invalid email type"}), 400

        # Send the email using EmailSender
        EmailSender.send_email(recipient_email, message)

        return jsonify({"message": "Email sent successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
