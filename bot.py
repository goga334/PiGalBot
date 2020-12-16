import telebot
import config
import db
import webbrowser
from telebot import types
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

bot = telebot.TeleBot(config.TOKEN)

give_name = 0

markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

item1 = types.KeyboardButton('"Почати роботу"')
markup1.add(item1)

item2 = types.KeyboardButton('"Додати фото"')
item3 = types.KeyboardButton('"Показати галерею"')
markup2.add(item2, item3)

#key = types.InlineKeyboardButton(text='4', callback_data='4')
#keyboard.add(key)

@bot.message_handler(commands=['logs'])
def get_logs(message):
    bot.send_message(message.chat.id, db.logs())


@bot.message_handler(commands=['start'])
def start(message):
    if db.get_id(str(message.from_user.id)) is None:
        db.add_user(str(message.from_user.id), str(message.from_user.first_name))
        print('add')
    else:

        print('restart')
    bot.send_message(message.chat.id, "Вітаю, {0.first_name}!\nЯ - <b>{1.first_name}</b>, "
                                      "бот, у якому ви можете створювати власні галереї зображень "
                                      "та виставляти їх на сайті.".format(message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup1)
    print('{0} has began to play'.format(message.from_user))
    print('has began to play' + str(message.from_user.id))



@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.from_user.id, "Напишіть /start")

@bot.message_handler(content_types=['photo'])
def pic_handle(message):
    db.add_pics(message.photo.file_id, '1234')

@bot.message_handler(content_types=['text'])
def bot_logic(message):

    if message.text == '"Почати роботу"':
        bot.send_message(message.chat.id, text="Чудово! Чекаю вашої команди)", reply_markup=markup2)
    elif message.text == '"Показати галерею"':
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized");
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")
        # options.add_argument('headless')
        options.add_argument('window-size=1920x935')
        browser = webdriver.Chrome(options=options)
        browser.get('https://drive.google.com/drive/u/3/my-drive')
        browser.find_element_by_xpath('//*[@id="identifierId"]').send_keys('pigalbot@gmail.com')
        browser.find_element_by_xpath('//*[@id="identifierNext"]/div/button/div[2]').click()

        element = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input'))
        )

        browser.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input').click()
        browser.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input').send_keys('pigalbot1234')
        browser.find_element_by_xpath('//*[@id="passwordNext"]/div/button/div[2]').click()

        print(browser)

        bot.send_message(message.from_user.id, "Ось усі фото, які ви мені завантажували")
    elif message.text == '"Додати фото"':
        bot.send_message(message.from_user.id, "Надсилайте мені фото. Надішліть команду /stop коли завершите")

    else:
        bot.send_message(message.from_user.id, "Є! Що тепер робитимемо?)", reply_markup=markup2)



bot.polling(none_stop=True)
# RUN
