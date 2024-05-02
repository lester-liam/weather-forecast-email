import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def sendEmail(subject, recipient_email, html_body):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 465

    context = ssl.create_default_context()
    
    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as smtp:
            smtp.login(os.environ.get("SMTP_LOGIN_USERNAME"), os.environ.get("SMTP_LOGIN_PASSWORD"))
            
            msg = MIMEMultipart()
            msg['From'] = os.environ.get("SMTP_LOGIN_USERNAME")
            msg['To'] = recipient_email
            msg['Subject'] = subject

            msg.attach(MIMEText(html_body, 'html'))

            # Send the email
            smtp.send_message(msg)

            status = smtp.quit()
            return(status)
        
    except Exception as e:
        return(e)