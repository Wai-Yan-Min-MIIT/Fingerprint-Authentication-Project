import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


def send_email(subject, to, body, attachment_path):
    gmail_user = 'testerwaiyan@gmail.com'
    gmail_password = 'epxemhusdamumqbm'
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(gmail_user, gmail_password)

    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with open(attachment_path, 'rb') as f:
        part = MIMEApplication(
            f.read(), Name=os.path.basename(attachment_path))
        part['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(
            attachment_path)
        msg.attach(part)

    server.sendmail(gmail_user, to, msg.as_string())
    server.quit()
