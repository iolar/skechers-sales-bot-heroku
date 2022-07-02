import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hlink
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta
import locale

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0'
}
locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")
cur_time = datetime.now(timezone(timedelta(hours=7))).strftime('%a %#d %b %Y %#H:%M')


def fetch_data():
    url = f'https://www.sportmaster.ru/catalog/brendy/skechers/muzhskaya_obuv/?f-ra=size_44,size_45&f-promotion:globalpromo=true'
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    shoes_items = soup.find('div', class_="sm-product-grid--size-xs") \
        .find_all('div', class_='sm-product-card__info')

    data = [{
        'datetime': cur_time
    }]
    for shoes_item in shoes_items:
        shoes_title = shoes_item.find('div', class_="sm-text-text-14").find('a').text.strip()
        shoes_url = 'https://www.sportmaster.ru' + \
                    shoes_item.find('div', class_="sm-text-text-14").find('a').get('href')
        shoes_new_price = int(shoes_item.find('span', class_="sm-amount_default") \
                              .find('span').find('span').text.replace(' ', '').replace('₽', ''))
        shoes_old_price = int(shoes_item.find('span', class_="sm-amount_old") \
                              .find('span').find('span').text.replace(' ', '').replace('₽', ''))
        shoes_discount = round(((shoes_old_price - shoes_new_price) / shoes_old_price) * 100)

        try:
            shoes_reviews = shoes_item.find('div', class_="feedback__rating-wrapper")\
                .find('span').text.strip()
        except:
            shoes_reviews = 'нет отзывов'

        if shoes_title.startswith('Кроссовки'):
            shoes_category = 'Кроссовки'
        elif shoes_title.startswith('Ботинки'):
            shoes_category = 'Ботинки'
        elif shoes_title.startswith('Полуботинки'):
            shoes_category = 'Полуботинки'
        elif shoes_title.startswith('Слипоны'):
            shoes_category = 'Слипоны'
        elif shoes_title.startswith('Кеды'):
            shoes_category = 'Кеды'
        elif shoes_title.startswith('Сандалии'):
            shoes_category = 'Сандалии'
        else:
            shoes_category = 'Другое'

        data.append(
            {
                "Категория": shoes_category,
                "Название": shoes_title,
                "Ссылка":  shoes_url,
                "Цена со скидкой": shoes_new_price,
                "Старая цена": shoes_old_price,
                "Скидка": shoes_discount,
                "Количество отзывов": shoes_reviews
            }
        )
        with open('result.json', 'w') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)


TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')

# webhook settings
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT', default=8000)


async def on_startup(dispatcher):
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


async def on_shutdown(dispatcher):
    await bot.delete_webhook()


async def show_data(message: types.Message, shoes_type):
    await message.answer('Одну секундочку... ')

    with open('result.json') as file:
        data = json.load(file)

    shoes_category = [x for x in data if x.get("Категория") == shoes_type]

    if len(shoes_category) != 0:
        for index, item in enumerate(shoes_category):
            card = f"{hlink(item.get('Название'), item.get('Ссылка'))}\n" \
                   f"{hbold('Старая цена: ')} {(item.get('Старая цена'))}\n" \
                   f"{hbold('Цена со скидкой ')}{hbold(item.get('Скидка'))}% :  {(item.get('Цена со скидкой'))} 🔥\n" \
                   f"{hbold('Количество отзывов: ')} {(item.get('Количество отзывов'))}"

            await message.answer(card)

            if index % 20 == 0:
                time.sleep(3)

    else:
        await message.answer('В данной категории отсутствуют товары для отображения 😕')

    await message.answer(f'Информация собрана с сайта: {hbold(data[0].get("datetime"))}')


@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ["Кроссовки", "Ботинки", "Полуботинки",
                     "Слипоны", "Кеды", "Сандалии"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer('Мужская обувь брэнда Skechers размера 44-45 со скидкой в интернет-магазине Спортмастер',
                         reply_markup=keyboard)


@dp.message_handler(Text(equals=("Кроссовки", "Ботинки", "Полуботинки",
                                 "Слипоны", "Кеды", "Сандалии")))
async def get_discounts(message: types.Message):
    await show_data(message, message.text)


@dp.message_handler()
async def get_discounts(message: types.Message):
    await message.answer("Не надо мне ничего писать, я - глупый бот, и умею только показывать скидки на обувь 😔\n"
                         "Лучше просто разверните меню внизу и нажмите на кнопочку с категорией обуви 😉")


def main():
    executor.start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )


if __name__ == '__main__':
    main()
