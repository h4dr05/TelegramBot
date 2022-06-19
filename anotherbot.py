import ast
from email import message
import json

from telegram_bot_pagination import InlineKeyboardPaginator

import telebot
from bson import json_util
from telebot import types
from database import BooksDatabase


bot = telebot.TeleBot("5313059421:AAEHlVfKWG-DiPS5krh3LToqR_YlNkytfdo")
database = BooksDatabase()
found = []


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
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.row('By title', 'By description', 'By author')
    msg = bot.send_message(message.chat.id, 'Choose the search method', reply_markup=keyboard)
    bot.register_next_step_handler(msg, findBook)

# @bot.message_handler()
def searchbytitle(message, page=1):
    msg = ''
    global found
    found = list(database.find_book(message.text, database.TITLE))
    # print(found)
    keyboard = types.InlineKeyboardMarkup()
    i = 0
    keyboard.row(types.InlineKeyboardButton('Note', callback_data=f"Note: {json_util.dumps(found[i]['_id'])}"))
    if message.text == 'Cancel':
        found = []
        mainmenu(message)
    elif len(found) > 1:
            send_character_page(message)





@bot.callback_query_handler(func=lambda call: call.data.split('#')[0]=='character')
def characters_page_callback(call):
    print(call)
    if hasattr(call, 'message'):
        page = int(call.data.split('#')[1])
        bot.delete_message(
            call.message.chat.id,
            call.message.message_id
        )
        send_character_page(call.message, page=page)
    elif call.chat:
        mainmenu(call)


def send_character_page(message, page=1):
    global found
    page_count = len(found)
    paginator = InlineKeyboardPaginator(
        page_count,
        current_page=page,
        data_pattern='character#{page}'
    )
    # foundFormatted = found[page-1]['title']
    print(found)
    msg = bot.send_message(
        message.chat.id,
        found[page-1]['title'],
        reply_markup=paginator.markup,
        parse_mode='Markdown'
    )
    if message.text == 'Cancel':
        found = []
        mainmenu(message)
    else:
        bot.register_next_step_handler(msg, characters_page_callback)




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


def note(message, book_id): # death note
    print(book_id)
    database.addNote(book_id, message.text)
bot.infinity_polling()