import smtplib

GMAIL_USER = "email"
GMAIL_PWD = "pwd"

def sendEmail(recipient, body):

    FROM = "Elkayam House"
    TO = recipient
    SUBJECT = "Who's Home?"
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server_ssl.ehlo() # optional, called by login()
        server_ssl.login(GMAIL_USER, GMAIL_PWD)
        server_ssl.sendmail(FROM, TO, message)
        server_ssl.close()
        print('successfully sent the mail')
    except:
        print("failed to send mail")