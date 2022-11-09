import telebot
import requests
import random
from bs4 import BeautifulSoup as bs
from decouple import config
from telebot import types
bot = telebot.TeleBot(config("TOKEN_BOT"))

URL = 'https://resheto.net/raznosti/75-motiviruyushchie-tsitaty'

def parser(url):
    r = requests.get(url)
    soup = bs(r.text, 'html.parser')
    phrases = soup.find_all('p', class_='notey')
    return [c.text for c in phrases]

list_of_phrases = parser(URL)
random.shuffle(list_of_phrases)


@bot.message_handler(commands=['start', 'начать', 'Здравствуйте'])
def start_answer(message):
    mess = f"Добро пожаловать, {message.from_user.first_name} {message.from_user.last_name}! \nЭтот бот умеет отправлять цитаты и афоризмы. \nДля этого вам нужно отправить цифры от 0 до 9"
    bot.send_message(message.chat.id, mess)


@bot.message_handler(content_types=['text'])
def phrase(message):
    if message.text == "Привет":
        bot.send_message(message.chat.id, "Привет, хочешь почитать Великие слова?")
    elif message.text == "Да":
        bot.send_message(message.chat.id, "Тогда отправь мне любую цифру от 0 до 9")
    elif message.text == "Нет":
        bot.send_message(message.chat.id, "Тогда иди делом занимайся )) \nВернешься сюда когда нужна будет мотивация")
    elif message.text.lower() in '0123456789':
        bot.send_message(message.chat.id, list_of_phrases[0])
        del list_of_phrases[0]
    elif message.text == "Спасибо":
        bot.send_message(message.chat.id, "Обращайся")
    else:
        photo = open("download.jpeg", 'rb')
        bot.send_photo(message.chat.id, photo)
        bot.send_message(message.chat.id, "Следуй правилам иначе я ничего не пойму. Хоть ты то понимаешь что я всего лишь бот.")


bot.polling(none_stop=True)
