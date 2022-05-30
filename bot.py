#Import components
from telegram.ext import Updater
from telegram.ext import CommandHandler

def sms(bot, update):
    print('Somebody sent me a /start command, what should I do?')
    bot.message.reply_text('Hello, I am a useless bot (right now at least) \nI am learning though...')


#main function
def main():
    my_bot = Updater("5313059421:AAEHlVfKWG-DiPS5krh3LToqR_YlNkytfdo", "https://telegg.ru/orig/bot", use_context=True)

    my_bot.dispatcher.add_handler(CommandHandler('start', sms))
    
    my_bot.start_polling() # checking for messages from Telegram
    my_bot.idle() #bot is working until it's stopped


main()