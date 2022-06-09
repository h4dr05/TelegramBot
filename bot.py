import telegram.ext
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, CallbackQueryHandler



class Bot(telegram.ext.Updater):
    def __init__(self, token, base_url="https://api.telegram.org/bot", use_context=True):
        super(Bot, self).__init__(token=token,
                                  base_url=base_url, use_context=use_context)

    def run(self):
        self.dispatcher.add_handler(
            telegram.ext.CommandHandler('start', self.start))
        self.start_polling()  # checking for messages from Telegram
        self.idle()  # bot is working until it's stopped

    def start(self, bot, update):
        print('Somebody sent me a /start command, what should I do?')
        reply_markup = [
            [
                InlineKeyboardButton(callback_data='Submenu 2-1', text='By author'),
                InlineKeyboardButton(callback_data='Submenu 2-2', text='By title'),
                InlineKeyboardButton(callback_data='Submenu 2-3', text='By description'),
            ]
        ]

        bot.message.reply_text(
            'Greeting! You can use this bot to search books through the archive.\nPlease choose the option on the menu below:',
            reply_markup=InlineKeyboardMarkup(reply_markup))

    def queryHandler(self, update:Update, context: CallbackContext):
        query = update.callback_query.data
        update.callback_query.answer()

        if 'Submenu 2-1' in query:
            print('Submenu 2-1')


# Initiate the bot
def run():
    token_fd = open('.token', 'r')
    token = token_fd.read().strip()
    token_fd.close()

    bot = Bot(token=token)
    bot.run()
