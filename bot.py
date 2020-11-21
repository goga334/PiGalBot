import telebot
import config
import webbrowser
from telebot import types

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['logs'])
def get_logs(message):
    bot.send_message(message.chat.id, db.logs(), reply_markup=markup1)

@bot.message_handler(commands=['start'])
def start(message):
    if db.get_id(str(message.from_user.id)) is  None :
        db.add(str(message.from_user.id))
        print('add')
    else:
        db.restart(str(message.from_user.id))
        print('restart')
    player.money = db.get_money(str(message.from_user.id))
    bot.send_message(message.chat.id, "Вітаю, {0.first_name}!\nЯ - <b>{1.first_name}</b>, "
                                      "бот для гри BlackJack.".format(message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup1)
    print('{0} has began to play'.format(message.from_user))
    print('has began to play'+str(message.from_user.id))

@bot.message_handler(commands=['help'])
def help(message):
	bot.send_message(message.from_user.id, "Напишіть /start")

@bot.message_handler(commands=['rules'])
def help(message):
	webbrowser.open('https://uk.wikipedia.org/wiki/%D0%91%D0%BB%D0%B5%D0%BA%D0%B4%D0%B6%D0%B5%D0%BA', new=2)

@bot.message_handler(content_types=['text'])
def bot_logic(message):



@bot.callback_query_handler(func=lambda call: True)

def callback_worker(call):




bot.polling(none_stop=True)
# RUN