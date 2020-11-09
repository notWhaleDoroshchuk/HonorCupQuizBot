# -*- coding: utf-8 -*-
# Python 3.x syntax
import json
import time
from selenium import webdriver


# Method for waiting while we searching opponent
def Searching():
    while 1:
        if browser.find_elements_by_class_name('game__answer'):
            break


# Method for Restart game
def Restart(count_of_questions):
    if count_of_questions == 5:
        restart_button = browser.find_element_by_xpath('/html/body/app/div[1]/result/div/div/div[9]/div[1]')
        restart_button.click()
        Searching()
        count_of_questions = 0
    return count_of_questions


# Method for waiting next question
def Wait_Question():
    while browser.find_elements_by_class_name('game__answer'):
        continue
    time.sleep(15)


# Method fot take questions and answers from website
def Take_Question_And_Answers():
    round_answers = browser.find_elements_by_class_name('game__answer')
    answers = [round_answers[0].text, round_answers[1].text, round_answers[2].text, round_answers[3].text]
    round_question = browser.find_element_by_class_name('game__question-text').text
    # I save questions as dictionary
    take_question = {
        'question': round_question,
        'answers': answers
    }
    return take_question


# Method for find answer on site and click
def Check_Answer(Question, db, index):
    scores = browser.find_element_by_class_name('game__user-value').text
    round_answers = browser.find_elements_by_class_name('game__answer')
    for i in range(len(Question['answers'])):
        if db[index]['answers'][0] == Question['answers'][i]:
            round_answers[i].click()
            break
    # Check status of answer (true or false)
    # if false - delete this answer from DataBase
    # else delete all answer except him
    if scores == browser.find_element_by_class_name('game__user-value').text:
        db[index]['answers'].pop(0)
    else:
        true_answer = db[index]['answers'][0]
        db[index]['answers'].clear()
        db[index]['answers'].append(true_answer)
    return db


# Check have we already had this question
def Check_Question(Question, db):
    check = 1
    for i in range(len(db)):
        if Question['question'] == db[i]['question']:
            db = Check_Answer(Question, db, i)
            check = 0
            break
    if check:
        db.append(Question)
        db = Check_Answer(Question, db, len(db) - 1)
    return db


# your token on HonorCup
path = 'C:\Temp\Token.txt'
with open(path, "r") as f:
    TOKEN = f.readline()

# Load data from file if they are there
try:
    database = json.load(open('data_base.json', encoding="utf-8"))
except:
    database = []

# open HonorCup site
browser = webdriver.Firefox(executable_path='geckodriver.exe')
browser.get(TOKEN)
time.sleep(2)

# Click on battle button
battle_button = browser.find_element_by_class_name('about__buttons')
battle_button.click()
time.sleep(2)

# Choose a category
category = browser.find_elements_by_class_name('slider__item')
category[1].click()

# Choose a theme
theme = browser.find_elements_by_class_name('profile__theme')
theme[1].click()

# Click on button 'play'
game = browser.find_element_by_xpath(
    '/html/body/app/div[1]/nomination/div/div/div[2]/div[3]/div[2]/div/div/div[2]/div')  # ('button-group-2x')
game.click()

# Searching opponent
Searching()
count = 0

# Count of games which we want to play
games = 1
time.sleep(4)

# Play
while games:

    # Restart game
    count = Restart(count)

    # Take answers and questions fro site
    quest = Take_Question_And_Answers()

    # Check question
    database = Check_Question(quest, database)

    # Waiting for the next question
    Wait_Question()
    count += 1

    if count == 5:
        games -= 1

# Unload Database to file
with open('data_base.json', 'w', encoding="utf-8") as f:
    json.dump(database, f, indent=2, ensure_ascii=False)

# Close browser
browser.close()
