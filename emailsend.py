from email.mime.base import MIMEBase
from email import encoders
import smtplib
from email.mime.multipart import MIMEMultipart
import os

def SendMail(sender_email,reciver_email,email_password,email_subject,xlsx_filename):
    sender_email = sender_email
    receiver_email = reciver_email
    password = email_password
    smtp_server = "smtp.gmail.com"
    smtp_port = 587 

    message = MIMEMultipart()
    message['From'] =sender_email
    message['To'] = reciver_email
    message['Subject'] = email_subject

    try:
        with open(xlsx_filename, "rb") as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())  
            encoders.encode_base64(part)  
            
            part.add_header(
                'Content-Disposition',
                f'attachment; filename={os.path.basename(xlsx_filename)}'
            )
            message.attach(part)

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

        return "Email sent successfully!"
    
    except Exception as e:
        return e
   
    finally:
        server.quit()