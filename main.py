from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from twilio.rest import Client
from flask import Flask
from flask import request
import time
import os

app = Flask(__name__)

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

output = ""

@app.route("/")
def index():
    subject = request.args.get("subject", "")
    course = request.args.get("course", "")
    section = request.args.get("section", "")
    phone = request.args.get("phone", "")
    if phone:
        checker(subject, course, section, phone)
    #FIXME: Check for non-existent course numbers/section numbers/subjects
    return ("""<form action="" method="get">
                First 3 letters of subject (e.g KIN):
                <input type="text" name="subject">
                <br>
                Course number (e.g. 2000B):
                <input type="text" name="course">
                <br>
                Section number (e.g. 200):
                <input type="text" name="section"> MUST BE 3 DIGITS
                <br>
                Phone number (e.g. 6471231234)
                <input type="text" name="phone">
                <br>
                <input type="submit" value="Monitor">
              </form>"""
              + "Output: "
              + output
    )

def checker(subject, course, section, phone):
    global output
    isFull = True
    browser = webdriver.Chrome(r"C:\Users\geoff\Downloads\chromedriver_win32\chromedriver.exe")
    browser.get("https://studentservices.uwo.ca/secure/timetables/mastertt/ttindex.cfm")
    browser.maximize_window()
    inputSubject = browser.find_element_by_id("inputSubject")
    inputSubject.send_keys(subject + Keys.ENTER)

    inputCourseNum = browser.find_element_by_id("inputCatalognbr")
    inputCourseNum.send_keys(course + Keys.ENTER)
    try:
        rows = len(browser.find_elements_by_xpath("/html/body/div/div/div[3]/table[1]/tbody/tr"))
        cols = len(browser.find_elements_by_xpath("/html/body/div/div/div[3]/table[1]/tbody/tr[1]/td"))
    except:
        output += "ERROR1"
#        return

    while isFull:
        try:
            for r in range(1, rows+1):
                for p in range(1, cols+1):
                    value = browser.find_element_by_xpath("/html/body/div/div/div[3]/table[1]/tbody/tr[" + str(r) + "]/td[" + str(p) + "]")
                    if value.text == section:
                        if browser.find_element_by_xpath("/html/body/div/div/div[3]/table[1]/tbody/tr[" + str(r) + "]/td[10]").text == "Full":
                            isFull = True
                            browser.refresh()
                        else:
                            isFull = False
        except Exception as e:
            output += "ERROR2"
            print(e)
#            return
        output += str(isFull)
        print(str(isFull) + course)
        if isFull:
            time.sleep(10)
    
    message = client.messages.create(
    body = "Hurry! " + subject.upper() + ' ' + course + ' Section ' + section + " is No Longer Full! Register now at student.uwo.ca",
    from_ = '+16473609346',
    to = '+1' + phone
    )
    
    browser.close()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
