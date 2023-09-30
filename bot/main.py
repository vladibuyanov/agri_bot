from telebot import types

from configuration import bot

from data_core.data import ApiData
from constants import main_constants
# from data_core.grafs import create_graf


@bot.message_handler(commands=['start'])
def start_message(message):
    start_message_text = 'Údaje prevzaté z web-page Central European Commission'

    # Creating keyboard buttons
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    wheat = types.KeyboardButton(main_constants.psenica)
    maize = types.KeyboardButton(main_constants.kukurica)
    rapeseed = types.KeyboardButton(main_constants.raps)
    # wheat_price_chart = types.KeyboardButton('Pšenica graf')
    # maize_price_chart = types.KeyboardButton('Kukurica graf')
    # rapeseed_price_chart = types.KeyboardButton('Raps graf')

    markup.add(wheat, maize, rapeseed)

    # Start message
    bot.send_message(message.chat.id, start_message_text, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def callback(message):
    api_data = ApiData()
    error_message = 'Nerozumiem. Použite tlačidlá'

    if message.chat.type == 'private':
        input_message_validation = api_data.validation_of_incoming_data(message.text)

        if input_message_validation:
            request_processing = len(input_message_validation)
            if request_processing == 1:
                result = api_data.data_processing(input_message_validation[0])
                bot.send_message(message.chat.id, f'Cena: {result} €\n')
            # if request_processing == 2:
            #     product = input_message_validation[0]
            #     graf = create_graf(product)
            #
            #     bot.send_photo(message.chat.id, graf)
        else:
            bot.send_message(message.chat.id, error_message)

