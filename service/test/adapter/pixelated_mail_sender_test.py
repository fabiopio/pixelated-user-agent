#
# Copyright (c) 2014 ThoughtWorks, Inc.
#
# Pixelated is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pixelated is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Pixelated. If not, see <http://www.gnu.org/licenses/>.
import unittest
from pixelated.adapter.pixelated_mail import PixelatedMail
from pixelated.adapter.pixelated_mail_sender import PixelatedMailSender
from mockito import *
import test_helper


class PixelatedMailSenderTest(unittest.TestCase):
    def setUp(self):
        self.mail_address = "pixelated@pixelated.org"
        self.mail_sender = PixelatedMailSender(self.mail_address)
        self.mail_sender.smtp_client = mock()

    def test_send_mail_sends_to_To_Cc_and_Bcc(self):
        mail_dict = test_helper.mail_dict()
        mail_dict['header']['to'] = ['to@pixelated.org', 'anotherto@pixelated.org']
        mail_dict['header']['cc'] = ['cc@pixelated.org', 'anothercc@pixelated.org']
        mail_dict['header']['bcc'] = ['bcc@pixelated.org', 'anotherbcc@pixelated.org']

        mail = PixelatedMail.from_dict(mail_dict)
        mail.to_smtp_format = lambda _from: "mail as smtp string"

        self.mail_sender.sendmail(mail)

        expected_recipients = ['to@pixelated.org', 'anotherto@pixelated.org', 'cc@pixelated.org',
                               'anothercc@pixelated.org',
                               'bcc@pixelated.org', 'anotherbcc@pixelated.org']

        verify(self.mail_sender.smtp_client).sendmail(self.mail_address, expected_recipients, "mail as smtp string")
