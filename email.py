import smtplib


def send_email(subject, msg):
    EMAIL_ADDRESS = "botgreenglo@gmail.com"
    PASSWORD = "iamo tirh hudn naav"
    TO = "hudaayy14@gmail.com"
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(EMAIL_ADDRESS, PASSWORD)
        message = 'Subject: {}\n\n{}'.format(subject, msg)
        server.sendmail(EMAIL_ADDRESS, TO, message)
        server.quit()
        text = "The email was sent!"
    except:
        text = "The email failed to send!"
    print(text) 


