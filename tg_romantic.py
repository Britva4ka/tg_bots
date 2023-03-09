import telebot
import utils
import json
import random
from telebot import types
bot = telebot.TeleBot("5790549079:AAF-bFp8rgOtuOAph0Qj1VPmL_3zoPy_IS0")
compliments = utils.get_compliment()
with open('romantic_bot_users.json', 'r') as f:
    user_data = json.load(f)
if user_data:
    for user in user_data:
        user_data[user]['comp_indexes'] = []
with open('romantic_bot_users.json', 'w') as f:
    json.dump(user_data, f)


@bot.message_handler(commands=['start'])
def start_handler(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Комплиментик ❤️')
    btn2 = types.KeyboardButton('Поменять имя ❤️')
    keyboard.add(btn1, btn2)
    name = message.from_user.first_name
    user_id = message.from_user.id
    user_name = message.from_user.username
    bot.send_message(chat_id=message.chat.id, text=f"Привет {name}, я Бот-Романтик и могу делать тебе комплименты", reply_markup=keyboard)
    with open('romantic_bot_users.json', 'r') as f:
        data = json.load(f)
    if user_id not in data:
        data.update({user_id: {'user_name': user_name, 'name': name, 'comp_indexes': []}})
    with open('romantic_bot_users.json', 'w') as f:
        json.dump(data, f)


@bot.message_handler(commands=['refresh'])
def refresh_handler(message):
    user_id = message.from_user.id
    with open('romantic_bot_users.json', 'r') as f:
        data = json.load(f)
        data[user_id]['comp_indexes'] = []
    with open('romantic_bot_users.json', 'w') as f:
        json.dump(data, f)
    bot.reply_to(message, "Успешно! Будешь утопать в моих комплиментах :)")


@bot.message_handler(content_types=['text'])
def handle_button_click(message):
    if message.text == 'Комплиментик ❤️':
        user_id = message.from_user.id
        with open('romantic_bot_users.json', 'r') as f:
            data = json.load(f)
        print(type(data))
        print(user_id in data)
        if len(data[user_id]['comp_indexes']) < len(compliments):
            compliment_index = None
            compliment = None
            while compliment_index not in data[user_id]['comp_indexes']:
                compliment = random.choice(compliments)
                compliment_index = compliments.index(compliment)
            full_compliment = data[user_id]['name'] + ', ' + compliment
            image = utils.draw_text(full_compliment)
            data[user_id]['comp_indexes'].append(compliment_index)
            with open('romantic_bot_users.json', 'w') as f:
                json.dump(data, f)
            bot.send_photo(message.chat.id, image)
        else:
            bot.send_message(message.chat.id, text="АШАЛЕТЬ! Комплиментики закончились!!!\n"
                                                                "(Напиши /refresh и комплиментики обновятся)")
    elif message.text == 'Поменять имя ❤️':
        bot.send_message(message.chat.id, text="Введи свое имя, зайчик :)")
        bot.register_next_step_handler(message, process_name)


def process_name(message):
    user_id = message.from_user.id
    name = message.text
    with open('romantic_bot_users.json', 'r') as f:
        data = json.load(f)
    data[user_id]['name'] = name
    with open('romantic_bot_users.json', 'w') as f:
        json.dump(data, f)
    bot.send_message(chat_id=message.chat.id, text="Приятно познакомиться, " + name)


if __name__ == "__main__":
    bot.polling(none_stop=True)
