import re
from bs4 import BeautifulSoup
from pprint import pprint

from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def login(email: str, password: str):

    # chrome driver options
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)

    # initialize the Chrome driver
    driver = webdriver.Chrome("chromedriver", options=options)
    
    # go to netzun login page
    driver.get("https://netzun.com/ingresar")

    # wait for eamil element to be available
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.NAME, "email")))
    # find email and pass field and insert
    driver.find_element(By.NAME,'email').send_keys(email)
    driver.find_element(By.NAME,'password').send_keys(password)
    # click login button
    driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div/div[2]/form/div[2]').click()
    
    # wait for mis-contenidos element to be available
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div[1]/header/nav[1]/ul/li[7]/a')))
    
def process_course(url: str):
    
    # go to netzun course page
    driver.get(url)

    # waiit for the page to load
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "script")))
    
    pageSource = driver.page_source
    fileToWrite = open("xxxx_page_source.html", "w")
    fileToWrite.write(pageSource)
    fileToWrite.close()


def main():

    # Netzun credentials
    email = "wayab66743@chotunai.com"
    password = "wayab66743@chotunai.com"

    # url course
    url_course =  "https://netzun.com/mis-contenidos/cursos/261/1264/4346"

    login(email, password)
    #process_course(url=url_course)


if __name__ == "__main__":
    main()