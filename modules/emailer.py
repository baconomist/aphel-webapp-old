import smtplib
import threading


def send_email(receivers, subject, body):
    threading.Thread(target=email_thread, args=(receivers, subject, body)).start()


def email_thread(receivers, subject, body):
    gmail_user = 'pchackersofficial@gmail.com'
    gmail_password = 'SHADAPWATERLOO'
    body = 'Subject: %s\n%s\n' % (subject, body)

    # Newline removes email header config(fixes no output when using ":")
    body = "\n" + body
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, receivers, body)
        server.close()

        print("Email Sent!")
    except:
        print("Something went wrong...")

# sendEmail(["pchackersofficial@gmail.com"],"Mr. Sender","Subject","Body")
