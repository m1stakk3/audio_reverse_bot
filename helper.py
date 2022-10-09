import os
import datetime


class FileDirectory:

    def __init__(self, message):
        """создание папок индивидуально под пользователя"""
        self.basic_directory = r"D:\Python\AUDIO BOT\DATA"
        if os.path.exists(self.basic_directory) is False:
            os.mkdir(self.basic_directory)

        if os.path.exists(f"{self.basic_directory}\\{message.from_user.id}") is False:
            os.mkdir(f"{self.basic_directory}\\{message.from_user.id}")

        self.input_directory = f"{self.basic_directory}\\{message.from_user.id}\\INPUT"
        self.output_directory = f"{self.basic_directory}\\{message.from_user.id}\\OUTPUT"

        if os.path.exists(self.input_directory) is False and os.path.exists(self.output_directory) is False:
            os.mkdir(self.input_directory)
            os.mkdir(self.output_directory)

        self.input_path = rf'{self.input_directory}\{str(datetime.datetime.today()).replace(":", "-")[:-7]}.ogg'
        self.output_path = rf'{self.output_directory}\{str(datetime.datetime.today()).replace(":", "-")[:-7]}.ogg'

        if message.text == '/start':

            with open(rf"{self.basic_directory}\{message.from_user.id}\{message.from_user.id}.txt", 'w',
                      encoding='utf-8') as user_data:
                user_data.write(f"User ID: {message.from_user.id}\n"
                                f"Username: {message.from_user.username}\n"
                                f"First name: {message.from_user.first_name}\n"
                                f"Last name: {message.from_user.last_name}\n"
                                f"First usage: {datetime.datetime.today()}\n"
                                f"Lang tag: {message.from_user.language_code}")

    def save_voice(self, voice):
        """получение исходного голосового сообщения и сохранение его в файл"""
        with open(self.input_path, 'wb') as voice_in:
            voice_in.write(voice)

    def save_reversed_voice(self, reversed_voice):
        """сохранение перевернутого голосового"""
        reversed_voice.export(self.output_path, format='ogg', codec='libopus', bitrate='48k')

    def read_reversed_voice(self):
        """считывание итогового файла и передача"""
        with open(self.output_path, 'rb') as answer_voice:
            answer = answer_voice.read()
        return answer


class Logger:

    path: str = rf"D:\Python\AUDIO BOT\LOGS"
    success_count: int = 0
    unsuccess_count: int = 0
    file_name = str(datetime.datetime.today())[:10]

    @staticmethod
    def create_logfile():
        """создание директории с логами и файла"""
        if os.path.exists(Logger.path) is False:
            os.mkdir(Logger.path)
            with open(rf"{Logger.path}\{Logger.file_name}.txt", "w", encoding="utf-8") as logfile:
                logfile.write(f"[{str(datetime.datetime.today())[:-7]}]: Hello world!\n")

    @classmethod
    def correct_log(cls, message, given_file):
        """дополнение в случае успешного выполнения"""
        cls.success_count += 1
        with open(rf"{Logger.path}\{Logger.file_name}.txt", "a+", encoding="utf-8") as logfile:
            logfile.write(f"[{str(datetime.datetime.today())[:-7]}]: successful answer {cls.success_count} | "
                          f"{message.from_user.id} | file: {given_file}\n")

    @classmethod
    def invalid_log(cls):
        """дополнение в случае ошибок"""
        cls.unsuccess_count += 1
        with open(rf"{cls.path}\{cls.file_name}.txt", "a+", encoding="utf-8") as logfile:
            logfile.write(f"[{str(datetime.datetime.today())[:-7]}]: unsuccessful {cls.unsuccess_count}\n")
