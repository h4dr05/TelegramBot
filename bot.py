import telegram.ext


class Bot(telegram.ext.Updater):
    def __init__(self, token, base_url="https://api.telegram.org/bot", use_context=True):
        super(Bot, self).__init__(token=token,
                                  base_url=base_url, use_context=use_context)

    def run(self):
        self.dispatcher.add_handler(
            telegram.ext.CommandHandler('start', self.sms))
        self.start_polling()  # checking for messages from Telegram
        self.idle()  # bot is working until it's stopped

    def sms(self, bot, update):
        print('Somebody sent me a /start command, what should I do?')
        bot.message.reply_text(
            'Hello, I am a useless bot (right now at least)\nI am learning though...')


# Initiate the bot
def run():
    token_fd = open('.token', 'r')
    token = token_fd.read().strip()
    token_fd.close()

    bot = Bot(token=token)
    bot.run()
