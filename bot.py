import telebot
import config
import modes
import db
import webbrowser
from telebot import types


bot = telebot.TeleBot(config.TOKEN)

give_name = 0
gallery_name = ' '
set_name = 0

markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
markup3 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
markup4 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
markup_empty = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
keyboard = types.InlineKeyboardMarkup()
item1 = types.KeyboardButton('"Почати роботу"')
markup1.add(item1)

item2 = types.KeyboardButton('"Створити галерею"')
item3 = types.KeyboardButton('"До створених галерей"')
markup2.add(item2, item3)

item4 = types.KeyboardButton('"Редагувати галерею"')
item5 = types.KeyboardButton('"Показати галерею"')
item6 = types.KeyboardButton('"Видалити галерею"')
markup3.add(item4, item5, item6)


item7 = types.KeyboardButton('"Додати зображення"')
item8 = types.KeyboardButton('"Видалити зображення"')
markup4.add(item7, item8)

keyboard.add(types.InlineKeyboardButton(text='somename', callback_data='somename'))


@bot.message_handler(commands=['logs'])
def get_logs(message):
    bot.send_message(message.chat.id, db.logs())


@bot.message_handler(commands=['start'])
def start(message):
    if db.get_id(str(message.from_user.id)) is None:
        db.add(str(message.from_user.id), str(message.from_user.first_name))

    bot.send_message(message.chat.id, "Вітаю, {0.first_name}!\nЯ - <b>{1.first_name}</b>, "
                                      "бот, у якому ви можете створювати власні галереї зображень "
                     .format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup1)
    print('has began to play' + str(message.from_user.id))



@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.from_user.id, "Напишіть /start")


@bot.message_handler(commands=['stop'])
def stop(message):
    bot.send_message(message.from_user.id, text="Чудово! Чекаю вашої команди)", reply_markup=markup2)


@bot.message_handler(content_types=['photo'])
def pic_handle(message):
    name = modes.gall_name
    if modes.gall_mode == 1:
        db.add_pics(message.from_user.id, name, message.photo[0].file_id)

def create_gal(id, name):
    if db.check_gallery(name):
        modes.set_gal = 1
        return "Галерея з іменем " + name + " вже існує"
    else:
        db.add_gallery(id, name)
        return "Галерею створено. Її назва " + name


def show_gallery(id):
    bot.send_message(id, "Галерея: " + modes.gall_name)
    link = db.get_gallery(modes.gall_name)
    modes.index = 0
    for i in link:
        modes.index = modes.index+1
        bot.send_photo(id, i[0], modes.index)


def delete_gallery(id):
    name = modes.gall_name
    print(name)
    db.delete_gallery(name)
    bot.send_message(id, "Галерея " + name + " видалена")


@bot.message_handler(content_types=['text'])
def bot_logic(message):
    keyboard = types.InlineKeyboardMarkup()
    if message.text[0] == '"':

        if message.text == '"Почати роботу"' or message.text == '"Це все!"':
            bot.send_message(message.chat.id, text="Чудово! Чекаю вашої команди)", reply_markup=markup2)

        elif message.text == '"Створити галерею"':
            modes.set_gal = 1
            bot.send_message(message.from_user.id, "Як її назвемо? ")

        elif message.text == '"До створених галерей"':
            bot.send_message(message.from_user.id, "Що робитимемо? ", reply_markup=markup3)

        elif message.text == '"Видалити галерею"':
            list = db.gallery_list(message.from_user.id)
            modes.gall_mode = 21
            for i in list:
                keyboard.add(types.InlineKeyboardButton(text=i[0], callback_data=i[0]))
            bot.send_message(message.from_user.id, "Оберіть зі списку створених ", reply_markup=keyboard)

        elif message.text == '"Редагувати галерею"':
            bot.send_message(message.from_user.id, "Що робитимемо? ", reply_markup=markup4)

        elif message.text == '"Показати галерею"':
            list = db.gallery_list(message.from_user.id)
            modes.gall_mode = 0
            for i in list:
                keyboard.add(types.InlineKeyboardButton(text=i[0], callback_data=i[0]))
            bot.send_message(message.from_user.id, "Оберіть зі списку створених ", reply_markup=keyboard)


        elif message.text == '"Додати зображення"':
            modes.gall_mode = 1
            list = db.gallery_list(message.from_user.id)
            for i in list:
                keyboard.add(types.InlineKeyboardButton(text=i[0], callback_data=i[0]))
            bot.send_message(message.from_user.id, "Оберіть зі списку створених ", reply_markup=keyboard)

        elif message.text == '"Видалити зображення"':
            modes.gall_mode = 22
            list = db.gallery_list(message.from_user.id)
            for i in list:
                keyboard.add(types.InlineKeyboardButton(text=i[0], callback_data=i[0]))
            bot.send_message(message.from_user.id, "Оберіть зі списку створених ", reply_markup=keyboard)

    elif modes.gall_mode == 22:
        link = db.get_gallery(modes.gall_name)
        db.delete_pics(link[int(message.text)-1][0])
        bot.send_message(message.from_user.id,
                         "Видалено) Надішліть команду /stop коли видалите всі фото")

    elif modes.set_gal == 1:
        modes.set_gal = 0
        bot.send_message(message.from_user.id, create_gal(message.from_user.id, message.text),
                         reply_markup=markup2)

    else:
        bot.send_message(message.from_user.id, "Я не розумію, чого саме я не розумію. Напиши /help.", reply_markup=markup_empty)

@bot.callback_query_handler(func=lambda call: True)

def callback_worker(call):

    modes.gall_name = call.data

    if (modes.gall_mode == 1):
        bot.send_message(call.message.chat.id, "Надсилайте мені фото. Надішліть команду /stop коли надішлете всі фото")
    if (modes.gall_mode == 0):
        show_gallery(call.message.chat.id)
        bot.send_message(call.message.chat.id, text="Чекаю команди)", reply_markup=markup2)
    if (modes.gall_mode == 21):
        delete_gallery(call.message.chat.id)
        bot.send_message(call.message.chat.id, text="Чекаю команди)", reply_markup=markup2)
    if (modes.gall_mode == 22):
        show_gallery(call.message.chat.id)
        bot.send_message(call.message.chat.id, "Напишіть номер зображення, яке хочете видалити. Надішліть команду /stop коли завершите видалення")


bot.polling(none_stop=True)
# RUN