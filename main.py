from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from twilio.rest import Client
import time
import os

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

isFull = True

browser = webdriver.Chrome(r"C:\Users\geoff\Downloads\chromedriver_win32\chromedriver.exe")
browser.get("https://studentservices.uwo.ca/secure/timetables/mastertt/ttindex.cfm")
browser.maximize_window()

subject = input("Enter the first 3 letters of the subject: ")
courseNum = input("Enter course number: ")
secNum = input("Enter section number: ")
#FIXME: Check for non-existent course numbers/section numbers/subjects
phoneNum = input("Enter your phone number (must be in the format 6473609346): ")

inputSubject = browser.find_element_by_id("inputSubject")
inputSubject.send_keys(subject + Keys.ENTER)

inputCourseNum = browser.find_element_by_id("inputCatalognbr")
inputCourseNum.send_keys(courseNum + Keys.ENTER)

rows = len(browser.find_elements_by_xpath("/html/body/div/div/div[3]/table[1]/tbody/tr"))
cols = len(browser.find_elements_by_xpath("/html/body/div/div/div[3]/table[1]/tbody/tr[1]/td"))

while isFull:
    for r in range(1, rows+1):
        for p in range(1, cols+1):
            value = browser.find_element_by_xpath("/html/body/div/div/div[3]/table[1]/tbody/tr[" + str(r) + "]/td[" + str(p) + "]")
            if value.text == secNum:
                if browser.find_element_by_xpath("/html/body/div/div/div[3]/table[1]/tbody/tr[" + str(r) + "]/td[10]").text == "Full":
                    isFull = True
                    browser.refresh()
                    time.sleep(5)
                else:
                    isFull = False
    print(isFull)

message = client.messages.create(
    body = "Hurry!, " + subject.upper() + ' ' + courseNum + ' Section ' + secNum + " is No Longer Full! Register now at student.uwo.ca",
    from_ = '+16473609346',
    to = '+1' + phoneNum
)

browser.close()