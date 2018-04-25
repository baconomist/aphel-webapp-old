import smtplib
import threading

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(receivers, subject, body):
    threading.Thread(target=email_thread, args=(receivers, subject, body)).start()


def email_thread(receivers, subject, body):
    gmail_user = 'pchackersofficial@gmail.com'
    gmail_password = 'SHADAPWATERLOO'

    # Newline removes email header config(fixes no output when using ":")
    #body = "\n" + body

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = gmail_user
    msg['To'] = receivers

    msg.attach(MIMEText(body, "html"))

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, receivers, msg.as_string())
        server.close()

        print("Email Sent!")
    except:
        print("Something went wrong...")

# sendEmail(["pchackersofficial@gmail.com"],"Mr. Sender","Subject","Body")
