import smtplib
from email.message import EmailMessage

def send_email(subject, message, to_emails):
    sender = 'bagget7777@gmail.com'
    password = 'iqhvbrcvdhswkwab'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    msg = EmailMessage()
    msg.set_content(message)

    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ", ".join(to_emails)
    
    try:
        server.login(sender, password)
        server.send_message(msg)
        return "200 OK"
    except Exception as error:
        return str(error)

emails = ['toktorovkurmanbek92@gmail.com', 'ktoktorov144@gmail.com', 'toktoroveldos15@gmail.com', 'bagget7777@gmail.com']

result = send_email('bagget777', 'Hello From Backend Group 8', emails)
print(result)
