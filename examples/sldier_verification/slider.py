import base64
from time import sleep

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from scripts.s_login import match

options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])

driver = webdriver.Chrome(options=options)
driver.maximize_window()
driver.get("https://pc-b2b2c.pickmall.cn/login")
sleep(2)

driver.find_element(By.CSS_SELECTOR, "[placeholder='用户名']").send_keys("ceshi")
sleep(1)
driver.find_element(By.CSS_SELECTOR, "[placeholder='密码']").send_keys("")
sleep(1)
driver.find_element(
    By.XPATH,
    '//*[@id="app"]/div/div[2]/div[2]/div[3]/div[1]/form[1]/div[3]/div/button',
).click()
sleep(2)

# Background image = img[1], slider piece = img[2]
img_bg = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[3]/div[1]/img[1]')
img_piece = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[3]/div[1]/img[2]')

s = img_bg.get_attribute("src")
s2 = img_piece.get_attribute("src")
lk = base64.b64decode(s.split(",")[1])
lk2 = base64.b64decode(s2.split(",")[1])

with open("pic.png", "wb") as f:
    f.write(lk)
with open("pic2.png", "wb") as f:
    f.write(lk2)

distance = match("pic.png", "pic2.png")
print(f"drag distance: {distance}")
sleep(2)

slider = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[3]/div[2]/span[2]')
ActionChains(driver).click_and_hold(slider).perform()
sleep(1)
ActionChains(driver).move_by_offset(xoffset=distance, yoffset=0).perform()
sleep(3)
ActionChains(driver).release().perform()
sleep(5)

get_text = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[3]/div/ul[1]/ul/li[1]').text
if get_text == "Hi，欢迎来到lilishop":
    print("login successful")
else:
    print("login failed")

sleep(2)
driver.quit()
