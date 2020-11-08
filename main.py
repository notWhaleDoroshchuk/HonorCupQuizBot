# -*- coding: utf-8 -*-
# Python 3.x syntax
class Question:
    """docstring"""
    def __init__(self, question, answers):
        self.question = question
        self.answers = answers
#your token on HonorCup
path = 'C:\Temp\Token.txt'
with open(path, "r") as f:
    TOKEN = f.readline()

from selenium import webdriver
import time

#open HonorCup site
browser = webdriver.Firefox(executable_path='geckodriver.exe')
browser.get(TOKEN)

#Click on battle button
battle_button = browser.find_element_by_class_name('about__buttons')
battle_button.click()
time.sleep(2)
#Choose a category
category = browser.find_elements_by_class_name('slider__item')
category[1].click()

#Choose a theme
theme = browser.find_elements_by_class_name('profile__theme')
theme[1].click()

#Click on button 'play'
game = browser.find_element_by_xpath('/html/body/app/div[1]/nomination/div/div/div[2]/div[3]/div[2]/div/div/div[2]/div')#('button-group-2x')
game.click()

#searching opponent
while 1:
    if browser.find_elements_by_class_name('game__answer'):
        break
count = 0
while 1:

    #restart game
    if count == 5:
        restart_button = browser.find_element_by_xpath('/html/body/app/div[1]/result/div/div/div[9]/div[1]')
        restart_button.click()
        count = 0
        while 1:
            if browser.find_elements_by_class_name('game__answer'):
                break

    #take answers
    round_answers = browser.find_elements_by_class_name('game__answer')
    round_answers[0].click()
    answ = round_answers[1].text

    #waiting for the next question
    while browser.find_elements_by_class_name('game__answer'):
        continue
    time.sleep(5)
    count += 1
