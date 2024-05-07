import telebot
from telebot import types
from aiogram.types import (ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup,
                           InlineKeyboardButton)

glottobot = telebot.TeleBot('6968053374:AAFnvlfo95Bvfn7IzPPSHWI6keFEoFFiiBU')


@glottobot.message_handler(commands=['start'])
def send_welcome(message):
    if message.text == "/start":
        glottobot.reply_to(message, "Hi! This is a bot that can help you to get general info about your requested "
                                "language from typological databases. Bases currently available are WALS, Phoible, "
                                "Grambank, Glottolog and Ethnologue.\n\nSend me a language you want to "
                                "learn more about:")


@glottobot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message != "phonetics" or "morphology" or "syntax" or "lexicon":
        user_language_reply = message.text
        markup = types.ReplyKeyboardMarkup()
        button1 = types.KeyboardButton("phonetics")
        button2 = types.KeyboardButton("morphology")
        button3 = types.KeyboardButton("syntax")
        button4 = types.KeyboardButton("lexicon")
        markup.add(button1)
        markup.add(button2)
        markup.add(button3)
        markup.add(button4)
        glottobot.send_message(message.chat.id, "Now choose the language field you would like to learn about:".format(message.from_user), reply_markup=markup)
    elif message == "phonetics" or "morphology" or "syntax" or "lexicon":
        #here is the space to insert our code that gets info

glottobot.infinity_polling()
