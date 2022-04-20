#!/usr/bin/env python3

from imapclient import IMAPClient, SEEN

SEEN_FLAG = 'SEEN'
UNSEEN_FLAG = 'UNSEEN'

class GmailWrapper:
    def __init__(self, host, userName, password):
        # force the user to pass along username and password to login as
        self.host = host
        self.userName = userName
        self.password = password
        self.login()

    def login(self):
        print('Logging in as ' + self.userName)
        server = IMAPClient(self.host, use_uid=True, ssl=True)
        server.login(self.userName, self.password)
        self.server = server

    # The IMAPClient sarch returns a list of Id's that match the given criteria
    # An Id in this case identifies a specific email
    def getIdsBySubject(self, subject, unreadOnly=True, folder='INBOX'):
        # search within the specified folder, e.g. Inbox
        self.setFolder(folder)

        # build the search criteria (e.g. unread emails with the given subject)
        self.searchCriteria = [UNSEEN_FLAG, 'SUBJECT', subject]

        if(unreadOnly == False):
            # force the search to include "read" emails too
            self.searchCriteria.append(SEEN_FLAG)
        
        # conduct the search and return the resulting Ids
        return self.server.search(self.searchCriteria)

    def markAsRead(self, mailIds, folder='INBOX'):
        self.setFolder(folder)
        self.server.set_flags(mailIds, [SEEN])

    def setFolder(self, folder):
        self.server.select_folder(folder)