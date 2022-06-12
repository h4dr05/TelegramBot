import telebot
from telebot import types

from database import BooksDatabase

bot = telebot.TeleBot("5313059421:AAEHlVfKWG-DiPS5krh3LToqR_YlNkytfdo")
database = BooksDatabase()


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(types.InlineKeyboardButton('Search', callback_data='Search'))
    mesg = bot.send_message(message.chat.id, 'Click Search to find the book you want',
                            reply_markup=keyboard)
    bot.register_next_step_handler(mesg, mainmenu)


@bot.callback_query_handler(func=lambda call: True)
def handler(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(types.InlineKeyboardButton('Cancel', callback_data='Cancel'))
    match call.data:
        case 'Search':
            mainmenu(call.message)
        case 'By title':
            msg = bot.send_message(call.message.chat.id, 'Type book name', reply_markup=keyboard)
            # searchbytitle(call.message, call.data)
            bot.register_next_step_handler(msg, searchbytitle)
            return
        case 'By description':
            msg = bot.send_message(call.message.chat.id, 'Type book desc', reply_markup=keyboard)
            bot.register_next_step_handler(msg, searchbydescription)
            return
        case 'By author':
            msg = bot.send_message(call.message.chat.id, 'Type book author', reply_markup=keyboard)
            bot.register_next_step_handler(msg, searchbyauthor)
            return
        case 'Cancel':
            mainmenu(call.message)
        case _:
            msg = bot.send_message(call.message.chat.id,
                                   'Something went wrong eh')


def mainmenu(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row_width = 3
    keyboard.row(types.InlineKeyboardButton('By title', callback_data='By title'),
                 types.InlineKeyboardButton('By description', callback_data='By description'),
                 types.InlineKeyboardButton('By author', callback_data='By author'))
    msg = bot.send_message(message.chat.id, 'Choose the search method', reply_markup=keyboard)


# def findBook(call: types.CallbackQuery):
#     keyboard = types.ReplyKeyboardMarkup(True, False)
#     keyboard.row('Cancel')
#     match call.message:
#         case 'By title':
#             msg = bot.send_message(call.message.chat.id, 'Type book name', reply_markup=keyboard)
#             bot.register_next_step_handler(msg, searchbytitle)
#             return
#         case 'By description':
#             msg = bot.send_message(call.message.chat.id, 'Type book desc', reply_markup=keyboard)
#             bot.register_next_step_handler(msg, searchbydescription)
#             return
#
#         case 'By author':
#             msg = bot.send_message(call.message.chat.id, 'Type book author', reply_markup=keyboard)
#             bot.register_next_step_handler(msg, searchbyauthor)
#             return
#         case _:
#             msg = bot.send_message(call.message.chat.id,
#                                    'Что-то пошло не так, иди нахуй, на кнопки понажимай, сука ебаная')

def searchbytitle(message):
    found = database.find_book(message.text, database.TITLE)
    text = database.to_string(list(found))
    msg = bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(msg, mainmenu)
    msg = None


# @bot.message_handler()
def searchbydescription(message):
    found = database.find_book(message.text, database.DESCRIPTION)
    text = database.to_string(list(found))
    msg = bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(msg, mainmenu)
    msg = None


# @bot.message_handler()
def searchbyauthor(message):
    found = database.find_book(message.text, database.AUTHOR)
    text = database.to_string(list(found))
    msg = bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(msg, mainmenu)
    msg = None


bot.infinity_polling()
