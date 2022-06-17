import ast
import json

import telebot
from bson import json_util
from telebot import types
from database import BooksDatabase


bot = telebot.TeleBot("5313059421:AAEHlVfKWG-DiPS5krh3LToqR_YlNkytfdo")
database = BooksDatabase()



@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.row('Search')
    mesg = bot.send_message(message.chat.id,'Click search, to... search', reply_markup=keyboard)
    bot.register_next_step_handler(mesg, mainmenu)

def findBook(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.row('Cancel')
    match message.text:
        case 'By title':
            msg = bot.send_message(message.chat.id, 'Введите название книги', reply_markup=keyboard)
            bot.register_next_step_handler(msg, searchbytitle)
            return
        case 'By description':
            msg = bot.send_message(message.chat.id, 'Введите описание книги', reply_markup=keyboard)
            bot.register_next_step_handler(msg, searchbydescription)
            return

        case 'By author':
            msg = bot.send_message(message.chat.id, 'Введите автора книги', reply_markup=keyboard)
            bot.register_next_step_handler(msg, searchbyauthor)
            return
        case _:
            msg = bot.send_message(message.chat.id, 'Something went wrong')


def mainmenu(message):
    print(message.text)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.row('By title', 'By description', 'By author')
    msg = bot.send_message(message.chat.id, 'Choose the search method', reply_markup=keyboard)
    bot.register_next_step_handler(msg, findBook)

# @bot.message_handler()
def searchbytitle(message):
    msg = ''
    found = list(database.find_book(message.text, database.TITLE))
    keyboard = types.InlineKeyboardMarkup()
    i = 0
    keyboard.row(types.InlineKeyboardButton('Note', callback_data=f"Note: {json_util.dumps(found[i]['_id'])}"))
    if message.text == 'Cancel':
        mainmenu(message)
    else:
        while i < len(found):
            bot.send_photo(message.chat.id, found[i]['thumbnailUrl'])
            msg = bot.send_message(message.chat.id, found[i]['title'], reply_markup=keyboard)
            i = i + 1
        bot.register_next_step_handler(msg, searchbytitle)


# @bot.message_handler()
def searchbydescription(message):
    msg = ''
    found = list(database.find_book(message.text, database.DESCRIPTION))
    keyboard = types.InlineKeyboardMarkup()
    i = 0
    keyboard.row(types.InlineKeyboardButton('Note', callback_data=f"Note: {json_util.dumps(found[i]['_id'])}"))
    if message.text == 'Cancel':
        mainmenu(message)
    else:
        while i < len(found):
            bot.send_photo(message.chat.id, found[i]['thumbnailUrl'])
            msg = bot.send_message(message.chat.id, found[i]['title'], reply_markup=keyboard)
            i = i + 1
        bot.register_next_step_handler(msg, searchbydescription)

# @bot.message_handler()
def searchbyauthor(message):
    msg = ''
    found = list(database.find_book(message.text, database.AUTHOR))
    keyboard = types.InlineKeyboardMarkup()
    i = 0
    keyboard.row(types.InlineKeyboardButton('Note', callback_data=f"Note: {json_util.dumps(found[i]['_id'])}"))
    if message.text == 'Cancel':
        mainmenu(message)
    else:
        while i < len(found):
            bot.send_photo(message.chat.id, found[i]['thumbnailUrl'])
            msg = bot.send_message(message.chat.id, found[i]['title'], reply_markup=keyboard)
            i = i + 1
        bot.register_next_step_handler(msg, searchbyauthor)

@bot.callback_query_handler(func=lambda call: True)
def handler(call: types.CallbackQuery):
    addNote(call.message, call.data)


def addNote(message, book):
    msg = bot.send_message(message.chat.id,
                            'Insert the Note' )

    bot.register_next_step_handler(msg, note, book[19: len(book)-1])


def note(message, book_id):
    print(book_id)
    database.addNote(book_id, message.text)
bot.infinity_polling()