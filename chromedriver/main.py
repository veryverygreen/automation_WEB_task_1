from functions import *
from selenium.webdriver.chrome.service import Service

"""Чистим файл"""
with open("report.json", "w") as file:
    file.write("")

def main():
    value, filename = variables()

    service = Service("C:\\Users\\Алексей\\PycharmProjects\\automation_WEB_task_1\\chromedriver\\chromedriver.exe")
    driver = webdriver.Chrome(service=service)

    driver.maximize_window()
    driver.get(url="https://ru.investing.com/equities/russia")

    main_data(driver, value, filename)

if __name__ == '__main__':
    main()
