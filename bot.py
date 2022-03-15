import telebot
from telebot.types import InputMediaPhoto
from hotels_api import get_hotels

bot = telebot.TeleBot('5270883666:AAFZio9rJZxTUrTN4f0INzbKeU1Wl1z7RS8')


@bot.message_handler(content_types=['text'])
def get_town_from_user(message):
    if message.text == '/hotels':
        bot.send_message(message.from_user.id, "Введите город")
        bot.register_next_step_handler(message, hotels)  # следующий шаг – функция get_name
    else:
        bot.send_message(message.from_user.id, 'Напиши /help')


def hotels(message):
    town = message.text
    channel_id = message.from_user.id
    bot.send_message(message.from_user.id, 'Ищем отели...')

    for hotel in get_hotels(town):
        text = f'Name: {hotel["hotel_name"]}, Rating: {hotel["hotel_rating"]}'
        media_group = []
        for i in range(len(hotel['hotel_images'])):
            media_group.append(InputMediaPhoto(hotel['hotel_images'][i], caption=text if i == 0 else ''))
        bot.send_media_group(chat_id=channel_id, media=media_group)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
