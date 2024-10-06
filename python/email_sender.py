import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailSender:
    # Class-level variables for email server information and credentials
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "wenliang2work@gmail.com"
    sender_password = "wputhriymdljvmtc"

    @classmethod
    def send_email(cls, recipient_email, message):
        try:
            # Connect to the SMTP server
            server = smtplib.SMTP(cls.smtp_server, cls.smtp_port)
            server.starttls()  # Start TLS encryption
            server.login(
                cls.sender_email, cls.sender_password
            )  # Log in to the email account

            # Send the email
            server.send_message(message)
            print("Email sent successfully!")

            # Close the server connection
            server.quit()

        except Exception as e:
            print(f"Failed to send email: {e}")

    @classmethod
    def get_test_message(cls, recipient_email):
        # Create a test email message
        message = MIMEMultipart()
        message["From"] = cls.sender_email
        message["To"] = recipient_email
        message["Subject"] = "Test Email"

        # Email content
        body = "This is a test email sent from Python."
        message.attach(MIMEText(body, "plain"))

        return message


# Main function for testing
if __name__ == "__main__":
    # Recipient email
    recipient_email = "346225483@qq.com"

    # Create a test message
    test_message = EmailSender.get_test_message(recipient_email)

    # Send the test email
    EmailSender.send_email(recipient_email, test_message)
