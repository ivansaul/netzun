from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
 
# https://netzun.com/cursos-online/mi-primera-importacion
# Github credentials
# witaval443@ezgiant.com
username = "wayab66743@chotunai.com"
password = "wayab66743@chotunai.com"
 
# initialize the Chrome driver
driver = webdriver.Chrome("chromedriver")
 
# head to github login page
driver.get("https://netzun.com/ingresar")
# find username/email field and send the username itself to the input field
driver.find_element(By.NAME,'email').send_keys(username)
# find password input field and insert password as well
driver.find_element(By.NAME,'password').send_keys(password)
# click login button
driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div/div[2]/form/div[2]').click()

sleep(7)

driver.get("https://netzun.com/mis-contenidos/cursos/261/1264/4346")


sleep(1)
# Espera a que se haya cargado la página
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "script")))

sleep(10)
pageSource = driver.page_source
fileToWrite = open("page_source.html", "w")
fileToWrite.write(pageSource)
fileToWrite.close()

sleep(70)
print("okkkkkkkkkk")
 