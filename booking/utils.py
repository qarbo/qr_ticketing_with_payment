import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# Replace these with your Gmail credentials
email_user = "asiadays.tickets@outlook.com"
email_password = 'qQ12wW34'


BOOKING_REQUEST_EMAIL = """
<html>
<head>
    <meta charset="UTF-8">
    <title>Booking Request Confirmation - Asia Days</title>
</head>
<body>
    <div style="background-color: #f7f7f7; padding: 20px; font-family: Arial, sans-serif;">
        <h1 style="color: #4CAF50;">Booking Request Confirmation</h1>
        <!-- English Version -->
        <div lang="en">
            <p>Dear {fullname},</p>
            <p>Thank you for submitting a booking request with Asia Days. We have received your request and will process it as soon as possible. Here are the details:</p>
            <ul>
                <li><strong>Date:</strong> August 18 at 9 PM</li>
                <li><strong>Location:</strong> Lou Lou Lounge. 1836 McDonald Ave, Brooklyn NY, 11223</li>
                {table}
            </ul>
            <p>To confirm your booking, please make the payment within the next 10 minutes. After that, the booking request will expire.</p>
            <p>You can make the payment by clicking the link below:</p>
            <a href="{booking_link}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Make Payment</a>
            <p>If you have any questions or need further assistance, please don't hesitate to contact us at:</p>
            <ul>
                <li>
                    <strong>Instagram:</strong>
                    <a href="https://https://www.instagram.com/asiadays/" target="_blank">AsiaDay instagram</a>
                </li>
                <li>
                    <strong>Phone Number:</strong> 315-620-0713
                </li>
                <!-- Add more contact information as needed -->
            </ul>
            
            <p>Thank you for choosing Asia Days!</p>
            <p>Best regards,<br>Asia Days Team</p>
        </div>
        <br>
        <!-- Russian Version -->
        <div lang="ru">
            <p>Привет, {fullname},</p>
            <p>Благодарим за подачу запроса на бронирование с Asia Days. Мы получили ваш запрос и обработаем его в кратчайшие сроки. Вот детали вашего запроса:</p>
            <ul>
                <li><strong>Дата: 18 Августа в 9 вечера</li>
                <li><strong>Местоположение:</strong> Lou Lou Lounge. 1836 McDonald Ave, Brooklyn NY, 11223</li>
                {table}
                <!-- Add more booking request details here as needed -->
            </ul>
            <p>Для подтверждения вашего бронирования, пожалуйста, внесите оплату в течение следующих 10 минут. После этого запрос на бронирование будет считаться недействительным.</p>
            <p>Вы можете оплатить, перейдя по следующей ссылке:</p>
            <a href="{booking_link}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Оплатить</a>
            <p>Если у вас возникнут вопросы или вам потребуется дополнительная помощь, не стесняйтесь связаться с нами:</p>
            <ul>
                <li>
                    <strong>Instagram:</strong>
                    <a href="https://https://www.instagram.com/asiadays/" target="_blank">AsiaDay instagram</a>
                </li>
                <li>
                    <strong>Phone Number:</strong> 315-620-0713
                </li>
                <!-- Add more contact information as needed -->
            </ul>
            <p>Спасибо, что выбрали Asia Days!</p>
            <p>С наилучшими пожеланиями,<br>Команда Asia Days</p>
        </div>
    </div>
</body>
</html>
"""


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
                <li><strong>Date:</strong> August 18 at 9 PM</li>
                <li><strong>Location:</strong> Lou Lou Lounge. 1836 McDonald Ave, Brooklyn NY, 11223</li>
        </ul>
        <a href="https://asiadays.us" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Visit Asia Days Website</a>
        <p>You can also scan the QR code below for quick access:</p>
        <div style="text-align: center;">
            <img src="{qr_code_url}" alt="QR Code" style="max-width: 200px; margin: 20px auto;">
        </div>
        <p>If you have any questions or need further assistance, please don't hesitate to contact us at:</p>
        <ul>
            <li>
                <strong>Instagram:</strong>
                <a href="https://https://www.instagram.com/asiadays/" target="_blank">AsiaDay instagram</a>
            </li>
            <li>
                <strong>Phone Number:</strong> 315-620-0713
            </li>
            <!-- Add more contact information as needed -->
        </ul>
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