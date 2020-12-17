import telebot
import config
import db
import webbrowser
from telebot import types


bot = telebot.TeleBot(config.TOKEN)

give_name = 0
gallery_name = ' '

markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
markup3 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
markup4 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
keyboard_add = types.InlineKeyboardMarkup()
keyboard_show = types.InlineKeyboardMarkup()
item1 = types.KeyboardButton('"Почати роботу"')
markup1.add(item1)

item2 = types.KeyboardButton('"Створити галерею"')
item3 = types.KeyboardButton('"До створених галерей"')
markup2.add(item2, item3)

item4 = types.KeyboardButton('"Додати фото"')
item5 = types.KeyboardButton('"Показати галерею"')
markup3.add(item4, item5)

item6 = types.KeyboardButton('"Ще"')
item7 = types.KeyboardButton('"Це все!"')
markup4.add(item6, item7)

keyboard_add.add(types.InlineKeyboardButton(text='somename', callback_data='asomename'))
keyboard_show.add(types.InlineKeyboardButton(text='somename', callback_data='ssomename'))


@bot.message_handler(commands=['logs'])
def get_logs(message):
    bot.send_message(message.chat.id, db.logs())


@bot.message_handler(commands=['start'])
def start(message):
    if db.get_id(str(message.from_user.id)) is None:
        db.add(str(message.from_user.id), str(message.from_user.first_name))

    bot.send_message(message.chat.id, "Вітаю, {0.first_name}!\nЯ - <b>{1.first_name}</b>, "
                                      "бот, у якому ви можете створювати власні галереї зображень "
                                      "та виставляти їх на сайті.".format(message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup1)
    print('has began to play' + str(message.from_user.id))



@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.from_user.id, "Напишіть /start")


@bot.message_handler(commands=['stop'])
def stop(message):
    bot.send_message(message.from_user.id, text="Чудово! Чекаю вашої команди)", reply_markup=markup2)


@bot.message_handler(content_types=['photo'])
def pic_handle(message):
    f = open('temp.txt')
    name = f.read()[1:]
    f.close()
    db.add_pics(message.from_user.id, name, message.photo[0].file_id)


def create_gal(id, name):
    db.add_gallery(id, name)
    return name


def show_gallery(id):

    f = open('temp.txt')
    name = f.read()[1:]
    f.close()
    bot.send_message(id, "Галерея: " + name)
    link = db.get_gallery(name)
    for i in link:
        bot.send_photo(id, i[0])


@bot.message_handler(content_types=['text'])
def bot_logic(message):
    keyboard_add = types.InlineKeyboardMarkup()
    keyboard_show = types.InlineKeyboardMarkup()
    if message.text[0] == '"':

        if message.text == '"Почати роботу"' or message.text == '"Це все!"':
            bot.send_message(message.chat.id, text="Чудово! Чекаю вашої команди)", reply_markup=markup2)

        elif message.text == '"Створити галерею"':
            bot.send_message(message.from_user.id, "Як її назвемо? ")

        elif message.text == '"До створених галерей"':
            bot.send_message(message.from_user.id, "Що робитимемо? ", reply_markup=markup3)

        elif message.text == '"Додати фото"' or message.text == '"Ще"':
            list = db.gallery_list(message.from_user.id)
            for i in list:
                keyboard_add.add(types.InlineKeyboardButton(text=i[0], callback_data='a' + i[0]))
            bot.send_message(message.from_user.id, "Оберіть зі списку створених ", reply_markup=keyboard_add)

        elif message.text == '"Показати галерею"':
            list = db.gallery_list(message.from_user.id)
            for i in list:
                keyboard_show.add(types.InlineKeyboardButton(text=i[0], callback_data='s' + i[0]))
            bot.send_message(message.from_user.id, "Оберіть зі списку створених ", reply_markup=keyboard_show)

        elif message.text == '"Додати до існуючої"' or message.text == '"Ще"':
            bot.send_message(message.from_user.id, "Надсилайте мені фото. Надішліть команду /stop коли надішлете всі фото")

    else:
        bot.send_message(message.from_user.id, "Галерею створено. Її назва " + create_gal(message.from_user.id, message.text),
                         reply_markup=markup2)


@bot.callback_query_handler(func=lambda call: True)

def callback_worker(call):

    f = open('temp.txt', 'w')
    f.write(call.data)
    f.close()
    if (call.data[0] == 'a'):
        bot.send_message(call.message.chat.id, "Надсилайте мені фото. Надішліть команду /stop коли надішлете всі фото")
    if (call.data[0] == 's'):
        show_gallery(call.message.chat.id)
        bot.send_message(call.message.chat.id, text="Чекаю команди)", reply_markup=markup2)

bot.polling(none_stop=True)
# RUN
