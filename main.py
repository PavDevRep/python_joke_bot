import requests  # для запроса данных
import random  # сортирует массив в рандомном порядке
import telebot  # для обращения к телеграмм боту
from bs4 import BeautifulSoup as sp  # для парсинга по html

URL = "https://anekdotov.net/anekdot/"  # сайт откуда будет идти парсинг
API_KEY = ""  # ключ для парсинга

# функция парсер


def parser(url):
    req = requests.get(url)  # берется html
    soup = sp(req.text, "html.parser")  # парсется от туда текст
    # собирает все теги с кламмои анекдот
    anekdots = soup.find_all('div', class_="anekdot")

    return [c.text for c in anekdots]


list_of_jokes = parser(URL)  # список все шуток
random.shuffle(list_of_jokes)  # рандомно перемешать анекдоты

bot = telebot.TeleBot(API_KEY)  # подключаем API ключ для бота

# Обработчик сообщщений


@bot.message_handler(commands=['start'])  # проверить сообщения
def hello(message):
    bot.send_message(
        message.chat.id, "Привет! чтобы посмеяться введите любую цифру от 0 до 9")


@bot.message_handler(content_types=['text'])
def jokes(message):
    if message.text.lower() in '0123456789':
        bot.send_message(
            message.chat.id, list_of_jokes[0])  # отправляем шутку
        del list_of_jokes[0]  # удаляем шутку
    else:
        bot.send_message(
            message.chat.id, "Введите любую цифру! От 0 до 9")


# Вечный цикл с обновлением сообщений
bot.polling()
