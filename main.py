#!/usr/bin/python
import os
import sys, traceback
import time
from hashlib import md5
from multiprocessing.dummy import Pool as ThreadPool
from os.path import dirname, join
from threading import Thread
from pyvirtualdisplay import Display
from logger import Logger
import logging


sys.path.append('ptcaccount2')
import ptcaccount2
import requests
from bs4 import BeautifulSoup as BS
from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import (StaleElementReferenceException,
                                        TimeoutException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

from captchaSolver import CaptchaSolver
from tempMail import TempMail


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

        elem = driver.find_element_by_name("g-recaptcha-response")
        elem = driver.execute_script("arguments[0].style.display = 'block'; return arguments[0];", elem)
        elem.send_keys(solvedcaptcha)

        # print("Captcha successful. Sleeping for 1 second...")
        logging.info("Captcha successful. Sleeping for 1 second...")
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
        # print "------------------------------------------------------------------"
        logging.info("------------------------------------------------------------------")
        # print "-> Waiting to confirm email on "+email
        logging.info("-> Waiting to confirm email on "+email)
        
        mails = tm.get_mails().body
        while ('error' in mails):
            sys.stdout.flush()
            time.sleep(10)
            mails = tm.get_mails().body


        mailHtml = mails[0]['mail_html'].encode('utf8')
        soup = BS(mailHtml, "lxml")
        links = soup.find_all('a')

        activationLink = links[2]['href']
        # print activationLink
        logging.info(activationLink)
        
        
        sys.stdout.flush()

        r = requests.get(activationLink)

        confHtml = r.text.encode('utf8')
        soup = BS(confHtml, "lxml")
        confText = soup.find("h2", class_="cufonAlternate")
        # print email+": "+confText.string
        logging.info(email+": "+confText.string)
        
        sys.stdout.flush()

        f = open('accounts.csv', 'ab')
        f.write('ptc,'+name+','+password+'\n')
        f.close()
        # print "==============================================================================================="
        logging.info("===============================================================================================")
        
        sys.stdout.flush()
    
    def run(self):
        display = Display(visible=0, size=(800, 600))
        display.start()

        am = PtcAccMaker()

        tmList = []
        # tmList.append(TempMail())

        tm = TempMail(key=self.TEMP_MAIL_KEY)

        results = self.cadastration(tm)
        # for item in range(0,1):
        #     tmList.append(TempMail(key=self.TEMP_MAIL_KEY))

        # # tm = TempMail('testmail')

        # pool = ThreadPool(5) 
        # results = pool.map(self.cadastration, tmList)

        # pool.close() 
        # pool.join()

if __name__ == "__main__":
    
    logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s',filename='logs_file',filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    for i in range(0,100):
        while True:
            try:
                # print "Creating account started"
                logging.info("Creating account started")
                am = PtcAccMaker()
                am.run()

                # print "Creating account finished, another after 5 minutes"
                logging.info("Creating account finished, another after 5 minutes")

                time.sleep(300)
            except:
                # print "Error happened, retrying after 1 minute"
                logging.info("Error happened, retrying after 1 minute")
                traceback.print_exc(file=sys.stdout)
                time.sleep(60)
                
                continue
            break
