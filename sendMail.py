import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_mail(to):
    
    # Email configuration
    sender_email = 'c_cloud2023@outlook.com'
    receiver_email = to
    password = 'C-cloud2023'
    subject = 'Subject of the email'
    message = 'Body of the email'

    # Create a multipart message and set the headers
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach the message to the MIMEMultipart object
    msg.attach(MIMEText(message, 'plain'))

    # Connect to the SMTP server (Outlook)
    smtp_server = 'smtp-mail.outlook.com'
    smtp_port = 587
    smtp_username = sender_email

    # Start the TLS encryption
    smtp_server = smtplib.SMTP(smtp_server, smtp_port)
    smtp_server.starttls()

    # Log in to your Outlook account
    smtp_server.login(smtp_username, password)

    # Send the email
    smtp_server.sendmail(sender_email, receiver_email, msg.as_string())

    # Close the connection to the SMTP server
    smtp_server.quit()