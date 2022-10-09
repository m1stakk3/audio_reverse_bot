import telebot
import requests
import os
from helper import FileDirectory, Logger
from pydub import AudioSegment
from pydub.utils import mediainfo
from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove

bot = telebot.TeleBot("5547424286:AAHnb468ZF9ljFx2C55Lvsc0hLSr2QRI0XU")
logger = Logger.create_logfile()


@bot.message_handler(commands=['start'])
def commands_handler(message):

    if message.text == '/start' and os.path.exists(rf"D:\Python\AUDIO BOT\DATA\{message.from_user.id}\{message.from_user.id}.txt") is False:
        FileDirectory(message)
        bot.send_message(message.chat.id, 'Hi, I can make your voice reversed.\n'
                         'Send me voice message :)')
    else:
        markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
        markup.add('Yes', 'No')
        bot.send_message(message.chat.id, 'Hi, do you remember my opportunities?', reply_markup=markup)

        def start_answer_handler(msg):
            if msg.text.lower() == 'no':
                bot.send_message(msg.chat.id, 'I can make your voice reversed. Send me voice message :)',
                                 reply_markup=ReplyKeyboardRemove())
            elif msg.text.lower() == 'yes':
                bot.send_message(msg.chat.id, 'Waiting for voice :)', reply_markup=ReplyKeyboardRemove())

        bot.register_message_handler(start_answer_handler, content_types=['text'])


@bot.message_handler(content_types=['voice'])
def voice_converter(message):
    audio_url = bot.get_file(message.voice.file_id).file_path
    try:
        input_voice = requests.get(f"https://api.telegram.org/file/bot5547424286:AAHnb468ZF9ljFx2C55Lvsc0hLSr2QRI0XU/"
                                   f"{audio_url}").content

        user_data = FileDirectory(message)
        user_data.save_voice(input_voice)

        reversed_voice = AudioSegment.from_ogg(user_data.input_path).reverse()
        user_data.save_reversed_voice(reversed_voice)

        meta = mediainfo(user_data.output_path)

        bot.send_voice(message.chat.id, user_data.read_reversed_voice(), duration=meta.get('duration'))
        Logger.correct_log(message, user_data.output_path)
    except BaseException:
        bot.send_message(message.chat.id, 'Server currently busy. Attempt later :-)')
        Logger.invalid_log()

    del audio_url
    del input_voice
    del reversed_voice
    del meta


bot.infinity_polling()
