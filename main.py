import asyncio

import requests
from bs4 import BeautifulSoup
from googletrans import Translator


async def translate(text):
    translator = Translator()
    result = await translator.translate(text, src="en", dest="ru")
    return result.text


# Создаём функцию, которая будет получать информацию
def get_english_words():
    url = "https://randomword.com/"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)

        # Создаём объект Soup
        soup = BeautifulSoup(response.content, "html.parser")
        # Получаем слово. text.strip удаляет все пробелы из результата
        english_words = soup.find("div", id="random_word").text.strip()
        # Переводим слово на русский
        translate_words = asyncio.run(translate(english_words))
        # Получаем описание слова
        word_definition = soup.find("div", id="random_word_definition").text.strip()
        # Переводим описание на русский
        translate_definition = asyncio.run(translate(word_definition))
        # Чтобы программа возвращала словарь
        return {
            "russian_words": translate_words.lower(),
            "word_definition": translate_definition
        }
    # Функция, которая сообщит об ошибке, но не остановит программу
    except:
        print("Произошла ошибка")


# Создаём функцию, которая будет делать саму игру
def word_game():
    print("Добро пожаловать в игру")
    while True:
        # Создаём функцию, чтобы использовать результат функции-словаря
        word_dict = get_english_words()
        word = word_dict.get("russian_words")
        word_definition = word_dict.get("word_definition")

        # Начинаем игру
        print(f"Значение слова - {word_definition}")
        user = input("Что это за слово? ")
        if user == word:
            print("Все верно!")
        else:
            print(f"Ответ неверный, было загадано это слово - {word}")

        # Создаём возможность закончить игру
        play_again = input("Хотите сыграть еще раз? y/n: ")
        if play_again != "y":
            print("Спасибо за игру!")
            break


word_game()
