import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Email credentials
sender_email = "proposal@buildahome.in"
receiver_email = "aravind.capricon@gmail.com"
password = "buildAhome2022!"

# Email content
subject = "Test Email"
body = "This is a test email sent from Python using GoDaddy SMTP server"

# Create a MIME object
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = subject
msg.attach(MIMEText(body, 'plain'))

# Connect to GoDaddy's SMTP server
try:
    server = smtplib.SMTP('mail.buildahome.in', 587)
    server.set_debuglevel(1)  # Enable debug output
    server.ehlo()
    server.starttls()  # Secure the connection
    server.ehlo()
    server.login(sender_email, password)
    text = msg.as_string()
    server.sendmail(sender_email, receiver_email, text)
    print("Email sent successfully!")
except smtplib.SMTPAuthenticationError as e:
    print("SMTP Authentication error: ", e.smtp_code, e.smtp_error)
except smtplib.SMTPException as e:
    print(f"SMTP error occurred: {e}")
except Exception as e:
    print(f"Error: {e}")
finally:
    try:
        server.quit()
    except Exception as e:
        print(f"Error closing the connection: {e}")