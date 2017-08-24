#!/usr/bin/python

import requests 
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.select import Select
import sys

class CaptchaSolver:
    def __init__(self, key):
        if key is None:
            print "You must give a 2captcha api Key"
        else:
            self.key = key

    def solve(self, recode, pgurl):
        service_key = self.key # 2captcha service key 
        google_site_key = recode 
        pageurl = pgurl
        url = "http://2captcha.com/in.php?key=" + service_key + "&method=userrecaptcha&googlekey=" + google_site_key + "&pageurl=" + pageurl 
        resp = requests.get(url) 
        if resp.text[0:2] != 'OK': 
            # quit('Service error. Error code:' + resp.text) 
            return False
        else:
            captcha_id = resp.text[3:]
            ret = self.wait(service_key, captcha_id)
            return ret
            # return True

    def wait(self, service_key, captcha_id):
        fetch_url = "http://2captcha.com/res.php?key="+ service_key + "&action=get&id=" + captcha_id

        for i in range(1, 10):	
            time.sleep(5) # wait 5 sec.
            resp = requests.get(fetch_url)
            if resp.text[0:2] == 'OK':
                break
                    
        return resp.text[3:]