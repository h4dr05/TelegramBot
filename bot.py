import telegram.ext


def sms(bot, update):
    print('Somebody sent me a /start command, what should I do?')
    bot.message.reply_text(
        'Hello, I am a useless bot (right now at least) \nI am learning though...')


# Initiate the bot
def run():
    token_fd = open('.token', 'r')
    token = token_fd.read().strip()
    token_fd.close()

    my_bot = telegram.ext.Updater(token=token,
                                  base_url="https://telegg.ru/orig/bot",
                                  use_context=True)

    my_bot.dispatcher.add_handler(telegram.ext.CommandHandler('start', sms))
    my_bot.start_polling()  # checking for messages from Telegram
    my_bot.idle()  # bot is working until it's stopped
