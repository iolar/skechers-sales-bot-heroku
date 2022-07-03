import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hlink
import json
import time

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

    with open('data.json') as file:
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
