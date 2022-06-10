import telegram.ext
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
from database import BooksDatabase
import pprint

class Bot(telegram.ext.Updater):
    def __init__(self, token, base_url="https://api.telegram.org/bot", use_context=True):
        super(Bot, self).__init__(token=token,
                                  base_url=base_url, use_context=use_context)

    def run(self):
        self.database = BooksDatabase()
        self.dispatcher.add_handler(
            telegram.ext.CommandHandler('start', self.start))
        self.dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), self.echo))    
        self.start_polling()  # checking for messages from Telegram
        self.idle()  # bot is working until it's stopped
        
    def start(self, bot, update):
        print('Somebody sent me a /start command, what should I do?')
        reply_markup = [
            [
                InlineKeyboardButton(text='By title', callback_data="1"),
                InlineKeyboardButton(text='By author', callback_data="2"),
                InlineKeyboardButton(text='By description', callback_data="3"),
            ]
        ]

        bot.message.reply_text(
            'Greeting! You can use this bot to search books through the archive.\nPlease choose the option on the menu below:',
            reply_markup=InlineKeyboardMarkup(reply_markup))


    def echo(self, update: Update, context: CallbackContext):
        d = list(self.database.find_book(update.message.text, self.database.TITLE))
        pprint.pprint(d)
        context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
        

    # def queryHandler(self, update:Update, context: CallbackContext):
    #     query = update.callback_query.data
    #     update.callback_query.answer()

    #     if 'Submenu 2-1' in query:
    #         print('Submenu 2-1')


# Initiate the bot
def run():
    token_fd = open('.token', 'r')
    token = token_fd.read().strip()
    token_fd.close()
    
    bot = Bot(token=token)
    bot.run()
