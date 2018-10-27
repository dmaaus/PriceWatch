from selenium import webdriver
import smtplib
import configparser
import sys
import time

config = configparser.ConfigParser()
config.read('config.ini')
url = config['WebElement']['url']

browser = webdriver.Chrome()
browser.get(url)

element1pos = config['WebElement']['element1pos']
element1posList = element1pos.split(', ')
element2pos = config['WebElement']['element2pos']
element2posList =  element2pos.split(', ')

lower_bound_string = config['Number']['lower_bound']
lower_bound_list = lower_bound_string.split(', ')
upper_bound_string = config['Number']['upper_bound']
upper_bound_list = upper_bound_string.split(', ')
timer = float(config['Number']['timer_in_sec'])

email_subject = config['Email']['email_sbj']
email_txt = config['Email']['email_txt']
recipientListString = config['Email']['recipient']
recipientList = recipientListString.split(', ')

config.read('login.ini')
id = config['Credential']['id']
pw = config['Credential']['pw']

while 1:
	for i in range(0, len(element1posList)):
		element1 = browser.find_element_by_xpath(element1posList[i]).text
		element2 = browser.find_element_by_xpath(element2posList[i]).text
		changes = float(element1)-float(element2)
		if changes < float(lower_bound_list[i]) or changes > float(upper_bound_list[i]):
			emailServer = smtplib.SMTP('smtp.gmail.com', 587)
			emailServer.ehlo()
			emailServer.starttls()
			emailServer.login(id, pw)
			email_text = email_txt + ' ' + str(changes)
			msg = 'Subject: {}\n\n{}'.format(email_subject, email_text)
			for r in recipientList:
				emailServer.sendmail(id, r, msg)
			emailServer.quit()
			time.sleep(timer)
