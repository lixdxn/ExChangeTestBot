import telebot
from currency_converter import CurrencyConverter, RateNotFoundError
from telebot import types


bot = telebot.TeleBot(token='7891751036:AAFrKNdBnHWp7LYuUXroqVO1YVzEFlIUhbE')
currency = CurrencyConverter()
amount = 0

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hi! Enter the amount to convert.')
    bot.register_next_step_handler(message, summ)

def summ(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'The amount must be greater than 0. Please enter the amount again.')
        bot.register_next_step_handler(message, summ)
        return

    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('USD / EUR', callback_data='usd/eur')
        btn2 = types.InlineKeyboardButton('EUR / USD', callback_data='eur/usd')
        btn3 = types.InlineKeyboardButton('GBP / USD', callback_data='gbp/usd')
        btn4 = types.InlineKeyboardButton('USD / GBP', callback_data='usd/gbp')
        btn5 = types.InlineKeyboardButton('EUR / GBP', callback_data='eur/gbp')
        btn6 = types.InlineKeyboardButton('GBP / EUR', callback_data='gbp/eur')
        btn7 = types.InlineKeyboardButton('Other Value ', callback_data='else')
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
        bot.send_message(message.chat.id, 'Select a currency pain: ', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'The message format is incorrect. Please enter an amount again.')
        bot.register_next_step_handler(message, summ)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != 'else':
        values = call.data.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f'Result: {round(res, 2)}.\nMaybe you want to check another amount?')
        bot.register_next_step_handler(call.message, summ)
    else:
        bot.send_message(call.message.chat.id, 'Enter a pair of values separated by the "/" sign.')
        bot.register_next_step_handler(call.message, my_currency)

def my_currency(message):
    try:
        values = message.text.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f'Result: {round(res, 2)}.\nMaybe you want to check another amount?')
        bot.register_next_step_handler(message, summ)
    except RateNotFoundError:
        bot.send_message(message.chat.id, f'The currency pair {message.text.upper()} is not in the database. Please try again.')
        bot.register_next_step_handler(message, my_currency)
    except ValueError as ve:
        bot.send_message(message.chat.id, f'{ve}. Please try again.')
        bot.register_next_step_handler(message, my_currency)
    except Exception:
        bot.send_message(message.chat.id, 'An error occurred. Please enter the pair again.')
        bot.register_next_step_handler(message, my_currency)

bot.polling(none_stop=True)










