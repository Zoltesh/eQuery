"""
Provides tools to send emails
"""

import logging
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import keyring

logging.basicConfig(level=logging.INFO)


class Emailer:
    """
    Class used to send emails
    """

    def __init__(self):
        self.smtp_server = 'smtp.Office365.com'
        self.smtp_port = 587
        self.sender_email = keyring.get_password('eQuery', 'sender_email')
        self.sender_password = keyring.get_password('eQuery', 'sender_password')
        # Set up logging
        self.logger_name = os.path.basename(__file__).split(".")[0]
        self.logger = logging.getLogger(self.logger_name)
        self.logger.setLevel(logging.INFO)

    def send_email(self, recipients, subject, body):
        """
        Send email to specified recipients with provided subject and body. Attachments optional.
        :param recipients: List of addresses receiving emails. Separate with commas and spaces e.g.
        '[<EMAIL>, <EMAIL>, <EMAIL>, <EMAIL>]'
        :param subject: Subject of the email e.g. 'Hello World'
        :param body: Body of the message e.g. 'Hello World, we've been trying to reach you about
        your car's extended warranty.'
        :return: bool True if the email was sent, False otherwise
        """
        message = MIMEMultipart()
        message['From'] = self.sender_email
        to_field = ', '.join(recipients)
        message['To'] = to_field
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg=message)
                self.logger.info('Email sent successfully')
                return True
        except AttributeError as ae:
            self.logger.error('Encountered Atrribute Error: %s\nEnsure keyring creds are set.', ae)
        except smtplib.SMTPAuthenticationError as e:
            if e.smtp_code == 334:
                self.logger.error('Encountered smpt code: 334 %\nEnsure keyring creds are set.')
            else:
                self.logger.error('Error sending email with smtp_code: %s', e)
        except smtplib.SMTPException:
            self.logger.error('Encountered smpt code: 535. Authentication unsuccessful. Check your'
                          'credentials in keyring and try again.')
            return False
