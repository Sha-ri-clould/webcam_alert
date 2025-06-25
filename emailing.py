import smtplib
from email.message import  EmailMessage
import os

sender_email = os.getenv("EMAIL")
password = os.getenv("webcam_password")
receiver_email = os.getenv("EMAIL")

def send_email(image_path):
    email= EmailMessage()
    email["Subject"]= "New Customer Showed Up!"
    email.set_content("Hey!, We saw a new customer.Open the image below.")
    with open(image_path, 'rb') as file:
        content = file.read()
    email.add_attachment(content, maintype='image',subtype='PNG')
    gmail = smtplib.SMTP('smtp.gmail.com', 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(sender_email, password)
    gmail.sendmail(sender_email,receiver_email,email.as_string())
    gmail.quit()
    print("Email sent")

if __name__ == '__main__':
    send_email(image_path="images/frame50.png")