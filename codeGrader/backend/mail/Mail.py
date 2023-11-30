"""
Mail Classes
Used to send mails for the CodeGrader
@author: mkaiser
"""

import smtplib
import time as t
from codeGrader.backend.config import config


class Mail:
    """
    Class that represents a mail that can then be sent.
    """

    def __init__(self, receiver: str, subject: str, message: str):
        """
        Constructor of an E-Mail
        @param receiver: The recipient of the email
        @param subject: The subject of the email message.
        @param message: The message that shall be sent to the recipient.
        """
        self.mail = config.mail_address
        self.password = config.mail_password
        self.smtp = config.mail_smtp
        self.port = config.mail_port  # 578
        self.use_authentication = config.use_authentication
        self.sender = config.sender

        self.receiver = receiver
        self.subject = subject
        self.message = message

        self.message = self._message_constructor(self.sender, self.receiver, self.subject, self.message)

    def send(self):
        """
        Sends the prepared mail to the receiver.
        @return: No return made
        """
        pass

        with smtplib.SMTP(host=self.smtp, port=self.port) as server:
            if self.use_authentication:
                server.starttls()
                server.login(self.mail, self.password)

            server.sendmail(self.sender, self.receiver, self.message)

    def _message_constructor(self):
        """

        @param sender:
        @param receiver:
        @param subject:
        @param message:
        @return:
        """
        message_text = (
                    "From: " + self.sender + "\n" + "To: " + self.receiver + "\n" + "Subject: " + self.subject + "\n\n" + self.message)
        return message_text
