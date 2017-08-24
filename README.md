# Pokemon Trainer Club Account Maker (BETA!)
Script heavily based on the original [PTCAccount2](https://github.com/Kitryn/PTCAccount2), by [Kitryn](https://github.com/Kitryn).

## Description
An automatic creation of PTC accounts, with automatic CAPTCHA input using [2Captcha API](http://2captcha.com/) and automatic EMAIL CONFIRMATION using [TempMail API](https://temp-mail.org/en/api/). This script is built on Selenium, which utilises a browser for automation rather than pure HTTP requests.

## Installation

This script runs on Selenium using ChromeDriver. See the [Google documentation](https://sites.google.com/a/chromium.org/chromedriver/downloads) for platform specific installation.

OSX Installation: `brew install chromedriver`

Once ChromeDriver is installed, clone this repo and install all dependencies using pip:

`pip install -r requirements.txt`

NOTE: Google Chrome (the browser) must be installed for this script to work!

## Use

Fill the .env-example file with your API keys, save it with the name of .env

Finally run main.py using python 2