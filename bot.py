import telebot
import requests
import datetime
import os
from pydub import AudioSegment

from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove

bot = telebot.TeleBot("5547424286:AAHnb468ZF9ljFx2C55Lvsc0hLSr2QRI0XU")


@bot.message_handler(commands=['start'])
def send_welcome(message):

    if message.text == '/start' and os.path.exists(f"D:\\Python\\AUDIO BOT\\{message.from_user.id}\\"
                                                   f"{message.from_user.id}.txt") is False:
        os.mkdir(f"D:\\Python\\AUDIO BOT\\{message.from_user.id}\\")
        with open(f"{message.from_user.id}/{message.from_user.id}.txt", 'w', encoding='utf-8') as user_data:
            user_data.write(f"User ID: {message.from_user.id}\n"
                            f"Username: {message.from_user.username}\n"
                            f"First name: {message.from_user.first_name}\n"
                            f"Last name: {message.from_user.last_name}\n"
                            f"First usage: {datetime.datetime.today()}\n"
                            f"Lang tag: {message.from_user.language_code}")
        bot.send_message(message.chat.id, 'Hi, I can make your voice reversed.\n'
                         'Send me voice message :)')
    else:
        markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
        markup.add('Yes', 'No')
        bot.send_message(message.chat.id, 'Hi, do you remember my opportunities?', reply_markup=markup)

        def start_answer_handler(message):
            if message.text.lower() == 'no':
                bot.send_message(message.chat.id, 'I can make your voice reversed.\n'
                                                  'Send me voice message :)', reply_markup=ReplyKeyboardRemove())
            elif message.text.lower() == 'yes':
                bot.send_message(message.chat.id, 'Waiting for voice :)', reply_markup=ReplyKeyboardRemove())

        bot.register_message_handler(start_answer_handler, content_types=['text'])


@bot.message_handler(content_types=['voice'])
def voice_converter(message):
    audio_url = bot.get_file(message.voice.file_id).file_path
    input_audio = requests.get(f"https://api.telegram.org/file/bot5547424286:AAHnb468ZF9ljFx2C55Lvsc0hLSr2QRI0XU/"
                               f"{audio_url}")
    input_audio = input_audio.content

    if os.path.exists(f"D:\\Python\\AUDIO BOT\\{message.from_user.id}\\INPUT") is False:
        os.mkdir(f"D:\\Python\\AUDIO BOT\\{message.from_user.id}\\INPUT")

    input_path = f'D:\\Python\\AUDIO BOT\\{message.from_user.id}\\INPUT\\' \
                 f'{str(datetime.datetime.today()).replace(":", "-")[:-7]}.ogg'

    with open(input_path, 'wb') as audio_in:
        audio_in.write(input_audio)

    if os.path.exists(f"D:\\Python\\AUDIO BOT\\{message.from_user.id}\\OUTPUT") is False:
        os.mkdir(f"D:\\Python\\AUDIO BOT\\{message.from_user.id}\\OUTPUT")

    out_file = f"D:\\Python\\AUDIO BOT\\{message.from_user.id}\\OUTPUT\\" \
               f"{str(datetime.datetime.today()).replace(':', '-')[:-7]}.ogg"

    reversed_audio = AudioSegment.from_ogg(input_path).reverse()
    reversed_audio.export(out_file, format='ogg')
    bot.send_audio(message.chat.id, open(out_file, 'rb'))


bot.infinity_polling()
