import getpass
import smtplib
from email.mime.multipart import MIMEMultipart
# MIMEText for creating body of the email message.
from email.mime.text import MIMEText
# MIMEApplication attaching application-specific data (like CSV files) to email messages.
from email.mime.application import MIMEApplication


def send_mail():

    HOST = "smtp.gmail.com"
    PORT = 587

    FROM_EMAIL = "thegenetic04@gmail.com"
    TO_EMAIL = "thegenetic00@proton.me"

    PASSWORD = "ergb mimw pfdb wqdo"

    SUBJECT = "Mail sent using python!"
    MESSAGE = """
    Hi,
    Its a test mail.

    Regards
    thegenetic
    """

    PATH_TO_FILE = '13-11-2024_14-53-40.txt'

    # Forming the message body
    message = MIMEMultipart()
    message['Subject'] = SUBJECT
    message['From'] = FROM_EMAIL
    message['To'] = TO_EMAIL
    body_part = MIMEText(MESSAGE)
    message.attach(body_part)

    # Attaching the file
    with open(PATH_TO_FILE, 'rb') as file:
        message.attach(MIMEApplication(file.read(), Name="13-11-2024_14-53-40.txt"))


    smtp = smtplib.SMTP(HOST, PORT)
    status_code, response = smtp.ehlo()
    print(f"[*] Echoing the server: {status_code} {response}")

    status_code, response = smtp.starttls()
    print(f"[*] Establishing a secure tls connection: {status_code} {response}")

    status_code, response = smtp.login(FROM_EMAIL, PASSWORD)
    print(f"[*] Loggin in: {status_code} {response}")

    smtp.sendmail(FROM_EMAIL, TO_EMAIL, message.as_string())
    smtp.close()



