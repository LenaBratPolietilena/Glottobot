

# в самом конце в class Language def twin_languages поменять файл с languages.txt на ссылку на этот файл из нашего репозитория! обнимаю



import telebot
import WALS
import phoible
import glottolog
import warnings
import strsimpy
from telebot import types
from strsimpy.jaro_winkler import JaroWinkler
from aiogram.types import (ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton)


warnings.simplefilter(action='ignore', category=FutureWarning)

glottobot = telebot.TeleBot('6968053374:AAFnvlfo95Bvfn7IzPPSHWI6keFEoFFiiBU')


users = {}


@glottobot.message_handler(commands=['start'])
def send_welcome(message):
    glottobot.reply_to(message, 
                       f'Hi! This is a bot that can help you to get general info about your requested language from typological databases. Bases currently available are WALS, Phoible, Grambank, and Glottolog.\n\nSend me a language you want to learn more about:')
    glottobot.register_next_step_handler(message, take_language)


@glottobot.message_handler(func=lambda message: message.text not in {'phonetics', 'morphology', 'syntax', 'lexicon', 'phonological inventory description', 'potential languages', '/start', '/anecdote'})
def take_language(message):
    language_name = message.text.title()
    language = Language(language_name)
    chat_id = message.chat.id
    users[chat_id] = language
    glottobot.send_message(chat_id, 
                           f"You have chosen the {language.name} language. If there is no data on the language available, try to click Potential Languages button")
    choose_domain(message)


def choose_domain(message):
    chat_id = message.chat.id
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button_phonetics = telebot.types.KeyboardButton(text='phonetics')
    keyboard.add(button_phonetics)
#    button_phonological_inventory_description = telebot.types.KeyboardButton(text='phonological inventory description')
#    keyboard.add(button_phonological_inventory_description)
    button_morphology = telebot.types.KeyboardButton(text='morphology')
    keyboard.add(button_morphology)
    button_syntax = telebot.types.KeyboardButton(text='syntax')
    keyboard.add(button_syntax)
    button_lexicon = telebot.types.KeyboardButton(text='lexicon')
    keyboard.add(button_lexicon)
    button_typology = telebot.types.KeyboardButton(text='typology&dialects')
    keyboard.add(button_typology)
    button_twin_languages = telebot.types.KeyboardButton(text='potential languages')
    keyboard.add(button_twin_languages)
    glottobot.send_message(chat_id, 
                           'Please, choose the specific domain of the language or look through some potential languages',
                           reply_markup=keyboard)


@glottobot.message_handler(func=lambda message: message.text == 'phonetics')
def phonetics(message):
    chat_id = message.chat.id
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    language = users[chat_id]
    glottobot.send_message(chat_id, 
                           f'WALS data: \n{language.wals_extract(chat_id, "phonetics")}')
    glottobot.send_message(chat_id, 
                           'Loading PHOIBLE...')
    glottobot.send_message(chat_id, 
                           f'{language.phoible_extract()}')
    glottobot.send_message(chat_id, 
                           f'You can also check out {language.is_data_available} of the {language.name} language. For a new language just type its name')


# @glottobot.message_handler(func=lambda message: message.text == 'phonological inventory description')
# def phonological_inventory_description(message):
#    chat_id = message.chat.id
#    language = users[chat_id]
#    glottobot.send_message(chat_id, 
#                           f'{language.phonological_inventory_extract()}')


@glottobot.message_handler(func=lambda message: message.text == 'morphology')
def morphology(message):
    chat_id = message.chat.id
    language = users[chat_id]
    glottobot.send_message(chat_id, 
                           f'WALS data: \n\n{language.wals_extract(chat_id, "morphology")}')
    glottobot.send_message(chat_id, 
                           f'You can also check out {language.is_data_available} of the {language.name} language. For a new language just type its name')


@glottobot.message_handler(func=lambda message: message.text == 'syntax')
def syntax(message):
    chat_id = message.chat.id
    language = users[message.chat.id]
    glottobot.send_message(chat_id, 
                           f'WALS data: \n\n{language.wals_extract(chat_id, "syntax")}')
    glottobot.send_message(chat_id, 
                           f'You can also check out {language.is_data_available} of the {language.name} language. For a new language just type its name')


@glottobot.message_handler(func=lambda message: message.text == 'lexicon')
def lexicon(message):
    chat_id = message.chat.id
    language = users[chat_id]
    glottobot.send_message(chat_id, 
                           f'WALS data: \n\n{language.wals_extract(chat_id, "lexicon")}')
    glottobot.send_message(chat_id, 
                           f'You can also check out {language.is_data_available} of the {language.name} language. For a new language just type its name')


@glottobot.message_handler(func=lambda message: message.text == 'typology&dialects')
def lexicon(message):
    chat_id = message.chat.id
    language = users[chat_id]
    glottobot.send_message(chat_id, 
                           f'Glottolog data: \n\n{language.glottolog_extract()}')
    glottobot.send_message(chat_id, 
                           f'You can also check out {language.is_data_available} of the {language.name} language. For a new language just type its name')


@glottobot.message_handler(func=lambda message: message.text == 'potential languages')
def lexicon(message):
    chat_id = message.chat.id
    language = users[chat_id]
    glottobot.send_message(chat_id, 
                           f"Here is some options you've probably wanted to enter: \n\n{language.twin_languages()}")


@glottobot.message_handler(commands=['anecdote'])
def anecdote(message):
    glottobot.reply_to(message, 
                       'When the inventor of the USB dies and he is being buried, at first he will be placed into grave, then lifted, turned upside down and then got down again.')


class Language:

    def __init__(self, name):
        self.name = name

    def is_data_available(self):
        available_domains = set()
        available_domains.append('typology&dialects') if glottolog.is_availble(self.name) else None
        available_domains.append('phonetics') if phoible.is_available(self.name) else None
        available_domains.extend(WALS.get_field(self.name).split(', '))
#        available_domains.extend(grambank.get_field(self.name).split(', '))
        return ', '.join(x for x in list(set(available_domains)))

    def phoible_extract(self):
        if phoible.get_info(self.name) == 0:
            return f'Unfortunately, {self.name} is not found in PHOIBLE database'
        return phoible.get_info(self.name)

    def phonological_inventory_extract(self):
        return phoible.get_features_info(self.name)

    def wals_extract(self, chat_id, user_field):
        if WALS.get_info(self.name, user_field) == 0:
            return f'Unfortunately, {self.name} is not found in WALS database'
        return WALS.get_info(self.name, user_field)
    
    def grambank_extract(self):
        pass

    def glottolog_extract(self):
        if glottolog.glottolog_info(self.name) == 0:
            return f'Unfortunately, {self.name} is not found in Glottolog database'
        return glottolog.glottolog_info(self.name)

    def twin_languages(self):
        jarowinkler = JaroWinkler()
        best_twin_languages = []
        subsequent_language_names = []
        with open("languages.txt") as file_in:
            for language in file_in:
                if language in self.name or self.name in language:
                    subsequent_language_names.append(language.rstrip('\n'))
                jws = jarowinkler.similarity(self.name, language)
                best_twin_languages.append((language.rstrip('\n'), jws))
            return ('\n'.join(j for j in list(set(list(map(lambda x: x[0], sorted(best_twin_languages, key=lambda pair: (-pair[1]))[:10])) + subsequent_language_names))))


if __name__ == '__main__':
    glottobot.infinity_polling()
