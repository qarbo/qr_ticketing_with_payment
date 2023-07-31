import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# Replace these with your Gmail credentials
email_user = "asiadays.tickets@outlook.com"
email_password = 'qQ12wW34'


SUCCESSFULL_BOOKING_BODY = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Booking Confirmation - Asia Days</title>
</head>
<body>
    <div style="background-color: #f7f7f7; padding: 20px; font-family: Arial, sans-serif;">
        <h1 style="color: #4CAF50;">Booking Confirmation</h1>
        <p>Dear {fullname},</p>
        <p>We are excited to confirm your booking with Asia Days. Here are the details:</p>
        <ul>
            <li><strong>Date:</strong> 8/18 at 9 PM</li>
            <li><strong>Location:</strong> Lou Lou Lounge. 1836 McDonald Ave, Brooklyn NY, 11223</li>
        </ul>
        <a href="https://asiadays.us" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Visit Asia Days Website</a>
        <p>You can also scan the QR code below for quick access:</p>
        <div style="text-align: center;">
            <img src="https://asiadays.us/generate-qr-code/{booking_id}" alt="QR Code" style="max-width: 200px; margin: 20px auto;">
        </div>
        <p>If you have any questions or need further assistance, please don't hesitate to contact us at [Contact Email/Phone].</p>
        <p>Thank you for choosing Asia Days! We look forward to seeing you soon.</p>
        <p>Best regards,<br>Asia Days Team</p>
    </div>
</body>
</html>
"""


def send_email_with_image(to_email, subject, body):
    try:
        # Set up the SMTP server
        smtp_server = smtplib.SMTP('smtp-mail.outlook.com', 587)
        smtp_server.starttls()
        smtp_server.login(email_user, email_password)

        # Create a multipart message
        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = to_email
        msg['Subject'] = subject

        # Add body text to the email
        msg.attach(MIMEText(body, 'html'))

        # Load the image from the file path and attach it to the email
        # with open(image_path, 'rb') as image_file:
        #     image_data = image_file.read()
        # image = MIMEImage(image_data, name='image.png')
        # msg.attach(image)

        # Send the email
        smtp_server.sendmail(email_user, to_email, msg.as_string())

        print("Email sent successfully!")

    except Exception as e:
        print("Error sending email:", e)

    finally:
        smtp_server.quit()