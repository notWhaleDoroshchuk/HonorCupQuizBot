# -*- coding: utf-8 -*-
path = 'C:\Temp\Token.txt'
with open(path, "r") as f:
    TOKEN = f.readline()
from selenium import webdriver
import time
browser = webdriver.Firefox(executable_path='geckodriver.exe')
browser.get(TOKEN)
battle_button = browser.find_element_by_class_name('about__buttons')
print(battle_button)
battle_button.click()
time.sleep(4)
category = browser.find_elements_by_class_name('slider__item')
category[1].click()
theme = browser.find_elements_by_class_name('profile__theme')
theme[1].click()
game = browser.find_element_by_xpath('/html/body/app/div[1]/nomination/div/div/div[2]/div[3]/div[2]/div/div/div[2]/div')#('button-group-2x')
game.click();
while 1:
    while 1:
        if browser.find_elements_by_class_name('game__answer') :
            print("true")
            break