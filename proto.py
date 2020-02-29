import telebot
import config
import random

from telebot import types
# test variant for DB project bot
bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    '''
    this functions create reply to user by start command
    with sticker and massage
    Moreover, function creates keyboard with two buttons 
    '''
    sti = open('welcome.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)

    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("🎲 Random fact about Artur")
    item2 = types.KeyboardButton("😊 How it`s going?")

    markup.add(item1, item2)

    bot.send_message(message.chat.id, "Welcome to the club buddy, {0.first_name}!\nI am - <b>{1.first_name}</b>, bot created for fun.".format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def lalala(message):
    '''
    this function creates reaction to the text sended to this bot
    '''
    if message.chat.type == 'private':
        if message.text == '🎲 Random fact about Artur':
            bot.send_message(message.chat.id, str(random.choice(['Artur is best in the world', 'Artur is best in solar system', 'Artur is best in KPI', 'Artur is best in KM-72', 'Artur loves his PS4', 'Artur finished school #250', 'Artur loves to sleep a lot'])))
        elif message.text == '😊 How it`s going?':

            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Nice!", callback_data='good')
            item2 = types.InlineKeyboardButton("So so...", callback_data='bad')

            markup.add(item1, item2)

            bot.send_message(message.chat.id, 'Good, and how are you?', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'I have no reply 😢')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    '''
    this function implements inline callbacks
    thats mean that this function works with keybord in chat messages
    '''
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'That`s good 😊')
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Sorry😢')

            # remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="😊 How it`s going?", reply_markup=None)

            # show alert
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Operation succesful!!")

    except Exception as e:
        print(repr(e))


# RUN
bot.polling(none_stop=True)
