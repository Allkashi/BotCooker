import telebot
import requests
import re

bot = telebot.TeleBot('1845965662:AAGjbYR23lf0yzQEAA7qxyehnKizFndLQ9E')


RandomRecipeUrl = "https://api.spoonacular.com/recipes/random?apiKey=e54aa2990e914e15917196485f42a512"
RandomJoke = "https://api.spoonacular.com/food/jokes/random?apiKey=e54aa2990e914e15917196485f42a512"
GlyIndex = "https://api.spoonacular.com/food/ingredients/glycemicLoad?apiKey=e54aa2990e914e15917196485f42a512"
GuessPic = "https://api.spoonacular.com/food/images/classify?apiKey=e54aa2990e914e15917196485f42a512&imageUrl="


@bot.message_handler(content_types=['text', 'sticker'])
def get_text_messages(message):
    print(message.text, message.from_user.username)
    ingr = 'Ingredients:\n'
    inst = ''

    if message.text == "/random_recipe":
        res = requests.get(RandomRecipeUrl).json()
        bot.send_message(message.from_user.id, *[x['title'] for x in res['recipes']])
        bot.send_photo(message.from_user.id, *[x['image'] for x in res['recipes']])
        for x in res['recipes']:
            for y in x['analyzedInstructions']:
                for z in y['steps']:
                    for j in z['ingredients']:
                        if j['name'] in ingr:
                            continue
                        else:
                            ingr += j['name'] + '\n'
                break

        bot.send_message(message.from_user.id, ingr)

        for x in res['recipes']:
            inst = x['instructions']
        inst = re.sub('<[^>]+>', '', inst)
        bot.send_message(message.from_user.id, inst)
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Список команд:\n/food_joke\n/glycemic_index - запрос необходимо выполнять на латинице\n/guess_pic - необходимо отправить url ссылку на изображение\n/random_recipe\n/help\n ")
    elif message.text == "/start":
        bot.send_sticker(message.from_user.id, "https://i.ibb.co/KhX3FM7/sticker.webp")

    elif message.text == "/food_joke":
        res = requests.get(RandomJoke).json()
        bot.send_message(message.from_user.id, res['text'])

    elif message.text == "/glycemic_index":
        bot.send_message(message.from_user.id, 'Введите название продукта')
        bot.register_next_step_handler(message, get_gly)
    elif message.text == "/guess_pic":
        bot.send_message(message.from_user.id, 'Прикрепите ссылку на фото продукта, который необходимо распознать')
        bot.register_next_step_handler(message, guess_pic)
    else:
        bot.send_sticker(message.from_user.id, "https://i.ibb.co/mvP7D9V/stickerf.webp")
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Попробуй выбрать команду из списка или прочитать /help")


def get_gly(message):

    ingredients = {"ingredients": [message.text]}
    res = requests.post(GlyIndex, json=ingredients).json()
    for y in res['ingredients']:
        for z in y:
            if z == 'id':
                break
            else:
                bot.send_message(message.from_user.id, 'Упс. Не получилось определить гликемический индекс. Проверь правильность написания и попробуй снова.')
                return

    bot.send_message(message.from_user.id, 'Glycemic Index:')
    bot.send_message(message.from_user.id, *[x['glycemicIndex'] for x in res['ingredients']])


def guess_pic(message):

    pic = ''
    pic += GuessPic + message.text
    res = requests.get(pic).json()
    if res['status'] == 'failure':
        bot.send_message(message.from_user.id, 'Упс, не удалось определить, что изображено на картинке')
    else:
        bot.send_message(message.from_user.id, 'Category:')
        bot.send_message(message.from_user.id, res['category'])


bot.polling(none_stop=True, interval=0)
