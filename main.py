#!/usr/bin/python
import time
from tempMail import TempMail
from hashlib import md5
from bs4 import BeautifulSoup as BS
import requests
import sys
from multiprocessing.dummy import Pool as ThreadPool
import ptcaccount2
from captchaSolver import CaptchaSolver
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.select import Select
from threading import Thread
from os.path import join, dirname
from dotenv import load_dotenv
import os

class PtcAccMaker:

    def __init__(self):
        dotenv_path = join(dirname(__file__), '.env')
        load_dotenv(dotenv_path)

        self.CAPTCHA_KEY = os.environ.get("CAPTCHA_KEY")
        self.TEMP_MAIL_KEY = os.environ.get("TEMP_MAIL_KEY")

    def solver(self, driver):
        recaptcha = driver.find_element_by_class_name("g-recaptcha")
        reCode = recaptcha.get_attribute("data-sitekey")
        pgurl = driver.current_url

        driver.execute_script("arguments[0].scrollIntoView(true);", recaptcha)

        cs = CaptchaSolver(key=self.CAPTCHA_KEY)

        solvedcaptcha = cs.solve(reCode,pgurl)
        recaptcha_resp = driver.find_element_by_id("g-recaptcha-response")

        captchalen = len(solvedcaptcha)
        elem = driver.find_element_by_name("g-recaptcha-response")
        elem = driver.execute_script("arguments[0].style.display = 'block'; return arguments[0];", elem)
        elem.send_keys(solvedcaptcha)

        print("Captcha successful. Sleeping for 1 second...")
        time.sleep(1)  # Workaround for captcha detecting instant submission? Unverified
        return True

    def cadastration(self, tm):
        
        email = tm.get_email()
        name = tm.get_name()
        password = 'Passw0rd!'

        cs = CaptchaSolver(key=self.CAPTCHA_KEY)
        ptcaccount2.random_account(
                username=name,
                password=password,
                email=email,
                email_tag=False,
                captcha_handler=self.solver)

        # tm.delete_message(mails[0]['mail_id'])
        # print mails
        print "------------------------------------------------------------------"
        print "-> Waiting to confirm email on "+email
        mails = tm.get_mails().body
        while ('error' in mails):
            sys.stdout.flush()
            time.sleep(10)
            mails = tm.get_mails().body


        mailHtml = mails[0]['mail_html'].encode('utf8')
        soup = BS(mailHtml, "lxml")
        links = soup.find_all('a')

        activationLink = links[2]['href']
        print activationLink
        sys.stdout.flush()

        r = requests.get(activationLink)

        confHtml = r.text.encode('utf8')
        soup = BS(confHtml, "lxml")
        confText = soup.find("h2", class_="cufonAlternate")
        print email+": "+confText.string
        sys.stdout.flush()

        f = open('accounts.csv', 'ab')
        f.write('ptc,'+name+','+password+'\n')
        f.close()
    
    def run(self):        
        am = PtcAccMaker()

        tmList = []
        # tmList.append(TempMail())

        for item in range(0,1):
            tmList.append(TempMail(key=self.TEMP_MAIL_KEY))

        # tm = TempMail('testmail')

        pool = ThreadPool(5) 
        results = pool.map(self.cadastration, tmList)

        pool.close() 
        pool.join()

if __name__ == "__main__": 
    am = PtcAccMaker()
    am.run()