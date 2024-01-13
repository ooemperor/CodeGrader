# CodeGrader - https://github.com/ooemperor/CodeGrader
# Copyright © 2023, 2024 Michael Kaiser <michael.kaiser@emplabs.ch>
#
# This file is part of CodeGrader.
#
# CodeGrader is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CodeGrader is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CodeGrader.  If not, see <http://www.gnu.org/licenses/>.

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

    def __init__(self, receiver: str, subject: str, message: str) -> None:
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

    def send(self) -> None:
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

    def _message_constructor(self) -> str:
        """
        Construct a properly formatted message ready to send
        @return: The constructed message text
        @rtype: str
        """
        message_text = (
                    "From: " + self.sender + "\n" + "To: " + self.receiver + "\n" + "Subject: " + self.subject + "\n\n" + self.message)
        return message_text
