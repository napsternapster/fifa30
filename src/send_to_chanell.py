import os
import telegram


def send_msg(msg):
    BOT_TOKEN = os.environ.get('TOKEN')
    CHANNEL_ID = -1001150172687
    bot = telegram.Bot(BOT_TOKEN)
    try:
        bot.send_message(CHANNEL_ID, msg, disable_web_page_preview=True, parse_mode=telegram.ParseMode.MARKDOWN)
    except Exception as ex:
        print(f'Exception of type {type(ex).__name__} in (): {str(ex)}')
    finally:
        print('Finished sending.')
