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


class Mailbox:

    def __init__(self, mailbox_name, querier):
        self.mailbox_name = mailbox_name
        self.mailbox_tag = mailbox_name.lower()
        self.querier = querier

    def mails(self):
        _mails = self.querier.all_mails_by_mailbox(self.mailbox_name)

        result = []
        for mail in _mails:
            result.append(mail)
        return result

    def mails_by_tags(self, tags):
        if 'all' in tags or self.mailbox_tag in tags:
            return self.mails()
        return [mail for mail in self.mails() if len(mail.tags.intersection(tags)) > 0]

    def mail(self, mail_id):
        return self.querier.mail(mail_id)

    def add(self, mail):
        return self.querier.create_mail(mail, self.mailbox_name)

    def remove(self, ident):
        mail = self.querier.mail(ident)
        mail.remove_all_tags()
        self.querier.remove_mail(mail)

    @classmethod
    def create(cls, mailbox_name, soledad_querier):
        return Mailbox(mailbox_name, soledad_querier)
