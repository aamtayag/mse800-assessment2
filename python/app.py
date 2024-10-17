import http
import logging
from flask import Flask, request, jsonify
from email_sender import EmailSender
from email_templates import EmailTemplates

import system
import booking
import consts
import users

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
            return jsonify({"error": result}), http.HTTPStatus.BAD_REQUEST

        customer_email = result["customer_email"]
        tour = result["tour"]

        bookingopt = booking.booking_operation()

        result = bookingopt.update_booking_status(customer_email, tour, consts.BOOKING_STATUS_CANCELLED)
        if result == True:
            return jsonify({"code":0,"message": "modify success"}), http.HTTPStatus.OK
        else:
            return jsonify({"code":1,"message": "modify failed"}), http.HTTPStatus.OK


    except Exception as e:
        return jsonify({"error": str(e)}), http.HTTPStatus.INTERNAL_SERVER_ERROR


'''
DESCRIPTION: admin create users
url: http://localhost:5001/admin-create-users
method: POST
request:
body:
{   
    "logined_username": "admin",
    "new_user_email": "test@gmail.com",
    "firstname": "test_firstname",
    "lastname": "test_lastname",
    "password": "123456"
}

response:
{
    "code":0,
    "message": "success"
}


'''
@app.route("/admin-create-users", methods=["POST"])
def admin_create_users():
    try:
        # Get JSON data from the request
        data = request.json

        # Validate common fields
        valid, result = validate_request(data, ["logined_username", "new_user_email", "firstname", "lastname", "password"])
        if not valid:
            logging.error(f"validate_request failed: {result}, data: {data}")
            return jsonify({"error": result}), http.HTTPStatus.BAD_REQUEST


        logined_username = result["logined_username"]
        new_user_email = result["new_user_email"]
        firstname = result["firstname"]
        lastname = result["lastname"]
        password = result["password"]

        if logined_username != consts.ADMIN_NAME:
            logging.error(f"only admin can create users")
            return jsonify({"code": 1, "message": "failed,only admin can create users"}), http.HTTPStatus.FORBIDDEN


        users_opt = users.user_operation()
        add_user_result = users_opt.add_user(firstname, lastname, new_user_email, password, consts.ROLE_USER, '')
        if add_user_result == False:
            logging.error(f"add_user failed")
            return jsonify({"code": 1, "message": "failed"}), http.HTTPStatus.OK

        return jsonify({"code": 0, "message": "success"}), http.HTTPStatus.OK


    except Exception as e:
        return jsonify({"error": str(e)}), http.HTTPStatus.INTERNAL_SERVER_ERROR



'''


DESCRIPTION: admin modify user roles

url: http://localhost:5000/admin-modify-user-roles
method: POST
request:
body:
{
    "logined_username": "admin",
    "user_email": "test@gmail.com",
    "to_roles": "admin"
}

response:
{
    "code":0,
    "message": "success"
}


'''

@app.route("/admin-modify-user-roles", methods=["POST"])
def admin_modify_user_roles():
    try:
        # Get JSON data from the request
        data = request.json

        # Validate common fields
        valid, result = validate_request(data, ["logined_username", "user_email", "to_roles"])
        if not valid:
            logging.error(f"validate_request failed: {result}, data: {data}")
            return jsonify({"error": result}), http.HTTPStatus.BAD_REQUEST

        logined_username = result["logined_username"]
        user_email = result["user_email"]
        to_roles = result["to_roles"]

        if logined_username != consts.ADMIN_NAME:
            logging.error(f"only admin can modify user roles")
            return jsonify({"code": 1, "message": "failed,only admin can modify user roles"}), http.HTTPStatus.FORBIDDEN


        if to_roles != consts.ROLE_ADMIN and to_roles != consts.ROLE_USER:
            logging.error(f"to_roles is invalid: {to_roles}")
            return jsonify({"code": 1, "message": "failed"}),http.HTTPStatus.BAD_REQUEST

        users_opt = users.user_operation()
        modify_user_roles_result = users_opt.modify_user_roles(user_email, to_roles)
        if modify_user_roles_result == False:
            logging.error(f"modify_user_roles failed")
            return jsonify({"code": 1, "message": "failed"}), http.HTTPStatus.OK









        return jsonify({"code": 0, "message": "success"}), http.HTTPStatus.OK


    except Exception as e:
        return jsonify({"error": str(e)}), http.HTTPStatus.INTERNAL_SERVER_ERROR


'''
DESCRIPTION: admin query userlist
url: http://localhost:5000/admin-query-userlist
method: GET
request:
body:
{
    "logined_username": "admin"
}

response:
{
    "code":0,
    "message": "success",
    "userlist": [
        {
            "email": "user1@gmail.com","roles": "admin","first_name":"","last_name":""
        },
        {
            "email": "user2@gmail.com","roles": "user","first_name":"","last_name":""
        },
        {
            "email": "user3@gmail.com","roles": "user","first_name":"","last_name":""
        }
    ]
}

'''

@app.route("/admin-query-userlist", methods=["GET"])
def admin_query_userlist():
    try:
        # Get JSON data from the request
        data = request.json
        # Validate common fields
        valid, result = validate_request(data, ["logined_username"])
        if not valid:
            logging.error(f"validate_request failed: {result}, data: {data}")
            return jsonify({"error": result}), http.HTTPStatus.BAD_REQUEST

        logined_username = result["logined_username"]
        if logined_username != consts.ADMIN_NAME:
            logging.error(f"only admin can query userlist")
            return jsonify({"code": 1, "message": "failed,only admin can query userlist"}), http.HTTPStatus.FORBIDDEN

        users_opt = users.user_operation()
        userlist = users_opt.query_user_list()
        if userlist == []:
            logging.error(f"query_user_list failed")
            return jsonify({"code": 1, "message": "failed"}), http.HTTPStatus.OK


        userlist_json = []
        for user in userlist:
            user_json = {
                "email": user.userid,
                "roles": user.role,
                "first_name": user.fname,
                "last_name": user.lname
            }
            userlist_json.append(user_json)

        return jsonify({"code": 0, "message": "success", "userlist": userlist_json}), http.HTTPStatus.OK

    except Exception as e:
        return jsonify({"error": str(e)}), http.HTTPStatus.INTERNAL_SERVER_ERROR




if __name__ == "__main__":
    system.init_log()
    system.init_system()
    app.run(host="0.0.0.0", port=5000, debug=True)
