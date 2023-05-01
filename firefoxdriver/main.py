from functions import *
from selenium import webdriver
from selenium.webdriver.firefox.service import Service

"""Чистим файл"""
with open("report.json", "w") as file:
    file.write("")

def main():
    value, filename = variables()

    options = webdriver.FirefoxOptions()
    options.binary_location = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
    service = Service("C:\\Users\\Алексей\\PycharmProjects\\automation_WEB_task_1\\firefoxdriver\\geckodriver.exe")
    driver = webdriver.Firefox(service=service, options=options)

    driver.maximize_window()
    driver.get(url="https://ru.investing.com/equities/russia")

    main_data(driver, value, filename)

if __name__=='__main__':
    main()
