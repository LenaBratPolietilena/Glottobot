"""
The glottobotocode module contains the code of telegram bot called Glottolog.
It aggregates all the data from other modules that process databases and gives it out in readable way to the telegram bot.
"""

import telebot
import WALS
import phoible
import glottolog
import Grambank
import warnings
import strsimpy
import pandas as pd
from telebot import types
from strsimpy.jaro_winkler import JaroWinkler

# to ignore some minor warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# the initializer of the bot
glottobot = telebot.TeleBot('6968053374:AAFnvlfo95Bvfn7IzPPSHWI6keFEoFFiiBU')

# dictionary that later will set one-to-one correspondence between user and the language she has chosen
users = {}


@glottobot.message_handler(commands=['start'])
def send_welcome(message):
    """
    The function send_welcome shows the welcome message and instruction of using the bot.
    """
    
    glottobot.reply_to(message, 
                       f'Hi! This is a bot that can help you to get general info about your requested language from typological databases. Bases currently available are WALS, Phoible, Grambank, and Glottolog.\nSend me a language you want to learn more about:')
    glottobot.register_next_step_handler(message, take_language)


@glottobot.message_handler(func=lambda message: message.text not in {'phonetics', 'morphology', 'syntax', 'lexicon', 'phonological inventory description', 'potential languages', 'typology&dialects', '/start', '/help', '/anecdote'})
def take_language(message):
    """
    The function take_language takes user's language and set it as the value of users-dictionary (key: chat_id).
    Then it shows the available domains of the language using .is_data_available() method of class Language. 
    """
    
    language_name = message.text.title()
    language = Language(language_name)
    chat_id = message.chat.id
    users[chat_id] = language
    glottobot.send_message(chat_id,
                           'Loading available domains...')
    glottobot.send_message(chat_id, 
                           f"You have chosen the {language.name} language, the available domains are: {language.is_data_available()}. If there is no data on the language available, try to click Potential Languages button")
    choose_domain(message)


def choose_domain(message):
    """
    The function choose_domain creates keyboard with buttons: phonetics, morphology, syntax, lexicon, typology&dialects and potential languages.
    """
    
    chat_id = message.chat.id
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button_phonetics = telebot.types.KeyboardButton(text='phonetics')
    keyboard.add(button_phonetics)
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
    """
    The function phonetics collects the data about the phonetics of the user's language (WALS and PHOIBLE data is used).
    """
    
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
                           f'For a new language just type its name or choose another domain')


@glottobot.message_handler(func=lambda message: message.text == 'morphology')
def morphology(message):
    """
    The function morphology collects the data about the morphology of the user's language (WALS and Grambank data is used).
    """
    
    chat_id = message.chat.id
    language = users[chat_id]
    glottobot.send_message(chat_id, 
                           f'WALS data: \n{language.wals_extract(chat_id, "morphology")}')
    glottobot.send_message(chat_id, 
                           'Loading Grambank...')
    glottobot.send_message(chat_id, 
                           f'Grambank data: \n{language.grambank_extract(chat_id, "morphology")}')
    glottobot.send_message(chat_id, 
                           f'For a new language just type its name or choose another domain')


@glottobot.message_handler(func=lambda message: message.text == 'syntax')
def syntax(message):
    """
    The function syntax collects the data about the syntax of the user's language (WALS and Grambank data is used).
    """
    
    chat_id = message.chat.id
    language = users[message.chat.id]
    glottobot.send_message(chat_id, 
                           f'WALS data: \n{language.wals_extract(chat_id, "syntax")}')
    glottobot.send_message(chat_id, 
                           'Loading Grambank...')
    glottobot.send_message(chat_id, 
                           f'Grambank data: \n{language.grambank_extract(chat_id, "syntax")}')
    glottobot.send_message(chat_id, 
                           f'For a new language just type its name or choose another domain')


@glottobot.message_handler(func=lambda message: message.text == 'lexicon')
def lexicon(message):
    """
    The function lexicon collects the data about the lexicon of the user's language (WALS and Grambank data is used).
    """
    
    chat_id = message.chat.id
    language = users[chat_id]
    glottobot.send_message(chat_id, 
                           f'WALS data: \n{language.wals_extract(chat_id, "lexicon")}')
    glottobot.send_message(chat_id, 
                           'Loading Grambank...')
    glottobot.send_message(chat_id, 
                           f'Grambank data: \n{language.grambank_extract(chat_id, "lexicon")}')
    glottobot.send_message(chat_id, 
                           f'For a new language just type its name or choose another domain')


@glottobot.message_handler(func=lambda message: message.text == 'typology&dialects')
def typology_dialects(message):
    """
    The function typology_dialects collects the data about the typology_dialects of the user's language (Glottolog data is used).
    """
    
    chat_id = message.chat.id
    language = users[chat_id]
    glottobot.send_message(chat_id, 
                           f'Glottolog data: \n\n{language.glottolog_extract()}')
    glottobot.send_message(chat_id, 
                           f'For a new language just type its name or choose another domain')


@glottobot.message_handler(func=lambda message: message.text == 'potential languages')
def potential_languages(message):
    """
    The function potential_languages finds out some (around dozen) of the potential names of languages the user might have meant.
    It uses method twin_languages() of class Language.
    """
    
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
        """
        The function is_data_available finds out whether the data on the user's language is available or not.
        It uses specific functions from phoible.py, WALS.py, Grambank.py, glottolog.py files.
        """
        
        available_domains = []
        available_domains.append('typology&dialects') if glottolog.is_available(self.name) else None
        available_domains.append('phonetics') if phoible.is_available(self.name) else None
        available_domains.extend(WALS.get_field(self.name).split(', '))
        available_domains.extend(Grambank.get_field(self.name).split(', '))
        if available_domains != ['', '']:
            return ', '.join(x for x in list(set(available_domains)))
        return 'None'

    def phoible_extract(self):
        """
        The function phoible_extract collects the data from PHOIBLE using the phoible.py file.
        """
        
        phoible_output = phoible.get_info(self.name)
        if phoible_output == 0:
            return f'Unfortunately, {self.name} is not found in PHOIBLE database'
        return phoible_output

    def wals_extract(self, chat_id, user_field):
        """
        The function wals_extract collects the data from WALS using the WALS.py file.
        """
        
        wals_output = WALS.get_info(self.name, user_field)
        if wals_output == 0:
            return f'Unfortunately, {self.name} is not found in WALS database'
        return wals_output
    
    def grambank_extract(self, chat_id, user_field):
        """
        The function grambank_extract collects the data from grambank using the Grambank.py file.
        """
        
        grambank_output = Grambank.get_the_wisdom_of_grambank(self.name, user_field)
        if grambank_output == 0:
            return f'Unfortunately, Grambank can offer no knowledge concerning {self.name}.'
        return grambank_output

    def glottolog_extract(self):
        """
        The function glottolog_extract collects the data from glottolog using the glottolog.py file.
        """
        
        glottolog_output = glottolog.glottolog_info(self.name)
        if glottolog_output  == 0:
            return f'Unfortunately, {self.name} is not found in Glottolog database'
        return glottolog_output 

    def twin_languages(self):
        """
        The function twin_languages finds out some (around dozen) of the potential names of languages the user might have meant.
        It uses strsimpy library and Jaro-Winklers metrics to calculate the distanse between two strings - the language given and the potential option. 
        """
        
        jarowinkler = JaroWinkler()
        best_twin_languages = []
        subsequent_language_names = []
        file_in = pd.read_csv("https://raw.githubusercontent.com/LenaBratPolietilena/Glottobot/main/languages.txt", sep='\t', header=None)
        file_in = pd.DataFrame(file_in)
        file_in = file_in.values.tolist()
        for language in map(str, file_in[0]):
            if language in self.name or self.name in language:
                subsequent_language_names.append(language.rstrip('\n'))
            jws = jarowinkler.similarity(self.name, language)
            best_twin_languages.append((language.rstrip('\n'), jws))
        return (', '.join(j for j in list(set(list(map(lambda x: x[0], sorted(best_twin_languages, key=lambda pair: (-pair[1]))[:10])) + subsequent_language_names))))


if __name__ == '__main__':
    glottobot.infinity_polling()
