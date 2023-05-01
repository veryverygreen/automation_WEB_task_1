from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from concurrent.futures import ThreadPoolExecutor
import json

no_div = "Нет информации о дивидендах"

"""Сбор переменных от пользователя"""
def variables():
    value = input("Введите процент повышения цены ")
    value = float(value.replace('%', '').replace(',', '.'))

    filename = input("Введите имя файла, где будут отображаться дивиденды: ")
    with open(f"{filename}.json", "w") as file:
        file.write("")
    return value, filename


"""Часть ссылок на страницы содержит "?cid", ссылки на страницы с дивидендами по таким акциям отличаются"""
def check_link(link):
    if '?cid' in link:
        first_part, second_part = link.split('?')
        link = first_part + '-dividends?' + second_part
    else:
        link += '-dividends'
    return link


"""Запись данных в json файл"""
def write_json(file, data):

    with open(file, "a") as file:
        json.dump(data, file)
        file.write("\n")


"""Получение данных для дальнейшей записи в json"""
def get_json(name, price):
    write_json("report.json", {
        "Name": f"{name}",
        "Price": f"{price}",
    })


"""Поиск дивидендов"""
def get_report(link,filename):
    service = Service("C:\\Users\\Алексей\\PycharmProjects\\automation_WEB_task_1\\chromedriver\\chromedriver.exe")
    new_driver = webdriver.Chrome(service=service)
    new_driver.maximize_window()
    new_driver.get(url=link)

    name = new_driver.find_element(By.XPATH, "/html/body/div[5]/section/div[7]/h2").text[20:]

    try:
        if new_driver.find_element(By.XPATH, "//div[@class='earningNoData']").text == "Нет данных для отображения":
            div = no_div
    except Exception:
        div = new_driver.find_element(By.XPATH, "/html/body/div[5]/section/table/tbody/tr[1]/td[5]").text
        if "u041" in div:
            div = new_driver.find_element(By.XPATH, "/html/body/div[5]/section/table/tbody/tr/td[5]").text

        write_json(filename + ".json", {
            "Name": name,
            "Dividends": div,
        })
    new_driver.quit()


def main_data(driver, value, filename):
    link_list = []
    for i in range(1, 41):
        signal = driver.find_element(By.XPATH,
                            f"/html/body/div/div[2]/div/div/div[2]/main/div[3]/div[2]/table/tbody/tr[{i}]/td[6]").text[:-1]
        signal = float(signal.replace('+', '').replace('%', '').replace(',', '.'))
        if float(signal) >= value:
            link = driver.find_element(By.XPATH,
                                f"/html/body/div/div[2]/div/div/div[2]/main/div[3]/div[2]/table/tbody/tr[{i}]/td[1]/div/a").get_attribute("href")
            link_list.append(check_link(link))

            name = driver.find_element(By.XPATH,
                                f"/html/body/div/div[2]/div/div/div[2]/main/div[3]/div[2]/table/tbody/tr[{i}]/td[1]/div/a/h4/span[1]/span[2]").text

            price = driver.find_element(By.XPATH,
                                f"/html/body/div/div[2]/div/div/div[2]/main/div[3]/div[2]/table/tbody/tr[{i}]/td[2]").text
            get_json(name, price)

    with ThreadPoolExecutor() as executor:
        executor.map(get_report, link_list, [filename]*len(link_list))
