from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

browser = webdriver.Chrome(r"C:\Users\geoff\Downloads\chromedriver_win32\chromedriver.exe")
browser.get("https://studentservices.uwo.ca/secure/timetables/mastertt/ttindex.cfm")
browser.maximize_window()

courseNum = input("Enter course number: ")
secNum = input("Enter section number: ")

inputCourseNum = browser.find_element_by_id("inputCatalognbr")
inputCourseNum.send_keys(courseNum + Keys.ENTER)

rows = len(browser.find_elements_by_xpath("/html/body/div/div/div[3]/table[1]/tbody/tr"))
cols = len(browser.find_elements_by_xpath("/html/body/div/div/div[3]/table[1]/tbody/tr[1]/td"))

for r in range(1, rows+1):
    for p in range(1, cols+1):
        value = browser.find_element_by_xpath("/html/body/div/div/div[3]/table[1]/tbody/tr[" + str(r) + "]/td[" + str(p) + "]")
        if value.text == secNum:
            print(value.text)
            print(browser.find_element_by_xpath("/html/body/div/div/div[3]/table[1]/tbody/tr[" + str(r) + "]/td[10]").text)