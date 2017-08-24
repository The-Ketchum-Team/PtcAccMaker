#!/usr/bin/python
import random
import string
from hashlib import md5
import unirest

class TempMail:
    
    def __init__(self, key=None, name=None):
        if key is None:
            print "You must give a TempMail api Key"
        else:
            self.key = key
            
        if name is None:
            self.name = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))
        else:       
            self.name = name
        
        domains = self.get_domains().body
        self.domain = random.choice(domains)

        self.email = self.name+domains[0]
        # self.email = self.name+self.domain
        self.hash = self.get_hash()

    def get_name(self):
        return self.name

    def get_email(self):
        return self.email

    def get_hash(self, email=None):
        if email is None:
            return md5(self.email).hexdigest()
        else:       
            return md5(email).hexdigest()

    def get_domains(self):
        domains = unirest.get("https://privatix-temp-mail-v1.p.mashape.com/request/domains/",
            headers={
                "X-Mashape-Key": self.key,
                "Accept": "application/json"
            }
        )

        return domains

    def get_mails(self):
        mails = unirest.get("https://privatix-temp-mail-v1.p.mashape.com/request/mail/id/"+self.hash+"/",
            headers={
                "X-Mashape-Key": self.key,
                "Accept": "application/json"
            }
        )

        return mails

    def get_message(self, email):
        message = unirest.get("https://privatix-temp-mail-v1.p.mashape.com/request/one_mail/id/{md5}/",
            headers={
                "X-Mashape-Key": self.key,
                "Accept": "application/json"
            }
        )

        return message

    def delete_message(self, hash):
        response = unirest.get("https://privatix-temp-mail-v1.p.mashape.com/request/delete/id/"+hash+"/",
            headers={
                "X-Mashape-Key": self.key,
                "Accept": "application/json"
            }
        )
