from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailTemplates:
    sender_email = "wenliang2work@gmail.com"
    sender_phone = "+64 1234567890"

    # Email signature (modify this as needed)
    signature = f"""
    <br><br>
    <p style="font-family: Arial, sans-serif; color: #555;">
        Best Regards,<br>
        <strong>Tour Booking Teams</strong><br>
        Contact: <a href="mailto:{sender_email}">{sender_email}</a><br>
        Phone: {sender_phone}<br>
        Address: 123 Tour Booking Company St, Auckland, New Zealand
    </p>
    """

    @classmethod
    def get_base_message(cls, recipient_email, subject):
        # Create a base email message with standard headers
        message = MIMEMultipart()
        message["From"] = cls.sender_email
        message["To"] = recipient_email
        message["Subject"] = subject
        return message

    @classmethod
    def get_registration_success_message(cls, recipient_email):
        # Create the registration success message
        message = cls.get_base_message(recipient_email, "Registration Successful")
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; color: #333;">
                <h2 style="color: #4CAF50;">Welcome to Our Service!</h2>
                <p>Your registration was successful. We are excited to have you on board.</p>
                <p>Enjoy our services and feel free to reach out if you need any support!</p>
                {cls.signature}
            </body>
        </html>
        """
        message.attach(MIMEText(html_content, "html"))
        return message

    @classmethod
    def get_order_submission_message(cls, recipient_email):
        # Create the order submission success message
        message = cls.get_base_message(recipient_email, "Order Submitted Successfully")
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; color: #333;">
                <h2 style="color: #4CAF50;">Order Submitted!</h2>
                <p>Your order has been submitted successfully. We are processing it and will update you with the status soon.</p>
                <p>Thank you for shopping with us!</p>
                {cls.signature}
            </body>
        </html>
        """
        message.attach(MIMEText(html_content, "html"))
        return message

    @classmethod
    def get_order_status_change_message(cls, recipient_email, status):
        # Create the order status change message
        message = cls.get_base_message(recipient_email, "Order Status Update")
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; color: #333;">
                <h2 style="color: #FF9800;">Order Status Changed</h2>
                <p>Your order status has been updated to: <strong>{status}</strong>.</p>
                <p>If you have any questions, please contact our support team.</p>
                {cls.signature}
            </body>
        </html>
        """
        message.attach(MIMEText(html_content, "html"))
        return message


from email_sender import EmailSender

if __name__ == "__main__":
    # Recipient email
    recipient_email = "346225483@qq.com"

    # Create a registration success email
    registration_message = EmailTemplates.get_registration_success_message(
        recipient_email
    )
    # EmailSender.send_email(recipient_email, registration_message)

    # Create an order submission email
    order_submission_message = EmailTemplates.get_order_submission_message(
        recipient_email
    )
    # EmailSender.send_email(recipient_email, order_submission_message)

    # Create an order status change email
    order_status_change_message = EmailTemplates.get_order_status_change_message(
        recipient_email, "Shipped"
    )
    EmailSender.send_email(recipient_email, order_status_change_message)
