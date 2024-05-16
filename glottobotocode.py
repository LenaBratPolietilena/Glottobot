import telebot
from telebot import types
from aiogram.types import (ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton)

glottobot = telebot.TeleBot('6968053374:AAFnvlfo95Bvfn7IzPPSHWI6keFEoFFiiBU')


users = {}


@glottobot.message_handler(commands=['start'])
def send_welcome(message):
    glottobot.reply_to(message, 
                       f'Hi! This is a bot that can help you to get general info about your requested language from typological databases. Bases currently available are WALS, Phoible, Grambank, and Glottolog.\n\nSend me a language you want to learn more about:')
    glottobot.register_next_step_handler(message, take_language)


@glottobot.message_handler(func=lambda message: message.text not in {'phonetics', 'morphology', 'syntax', 'lexicon'})
def take_language(message):
    language_name = message.text.title()
    language = Language(language_name)
    chat_id = message.chat.id
    users[chat_id] = language
    glottobot.send_message(chat_id, 
                           f'Ваш язык {language.name}? я пока очень тупой бот. Тем не менее выбирай, че ты бы хотел узнать о языке, личинка лингвиста (с)')
    if language not in {'not-moksha'}:
        choose_domain(message)


def choose_domain(message):
    chat_id = message.chat.id
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_phonetics = telebot.types.KeyboardButton(text='phonetics')
    keyboard.add(button_phonetics)
    button_morphology = telebot.types.KeyboardButton(text='morphology')
    keyboard.add(button_morphology)
    button_syntax = telebot.types.KeyboardButton(text='syntax')
    keyboard.add(button_syntax)
    button_lexicon = telebot.types.KeyboardButton(text='lexicon')
    keyboard.add(button_lexicon)
    glottobot.send_message(chat_id, '',
                           reply_markup=keyboard)


@glottobot.message_handler(func=lambda message: message.text == 'phonetics')
def phonetics(message):
    chat_id = message.chat.id
    language = users[chat_id]
    glottobot.send_message(chat_id, f'WALS data: \n\n{language.wals_extract("phonetics")}')
    glottobot.send_message(chat_id, f'PHOIBLE data: \n\n{language.phoible_extract("phonetics")}')
    

@glottobot.message_handler(func=lambda message: message.text == 'morphology')
def morphology(message):
    chat_id = message.chat.id
    language = users[chat_id]
    glottobot.send_message(chat_id, 
                           f'WALS data: \n\n{language.wals_extract("morphology")}')
    glottobot.send_message(chat_id, 
                           f'You can also check out {language.is_data_available} of the {language.name} language. For a new language just type its name')
    if glottobot.message_handler == 'choose_language':
        glottobot.register_next_step_handler(message, take_language)

@glottobot.message_handler(func=lambda message: message.text == 'syntax')
def syntax(message):
    chat_id = message.chat.id
    language = users[message.chat.id]
    glottobot.send_message(chat_id, 
                           f'WALS data: \n\n{language.wals_extract("syntax")}')


@glottobot.message_handler(func=lambda message: message.text == 'lexicon')
def lexicon(message):
    chat_id = message.chat.id
    language = users[chat_id]
    glottobot.send_message(chat_id, 
                           f'WALS data: \n\n{language.wals_extract("lexicon")}')

@glottobot.message_handler(commands=['anecdote'])
def anecdote(message):
    glottobot.reply_to(message, 'When the inventor of the USB died and he was being buried, at first he was ')

class Language:

    def __init__(self, name):
        self.name = name

    def is_data_available(self):
        pass

    def phoible_extract(self):
        pass

    def wals_extract(self, user_field):
        pass

    def grambank_extract(self):
        pass

    def glottolog_extract(self):
        pass
    

if __name__ == '__main__':
    glottobot.infinity_polling()