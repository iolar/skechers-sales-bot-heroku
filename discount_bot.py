import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hlink
from main import collect_data
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


async def show_data(message: types.Message):
    with open('result.json') as file:
        data = json.load(file)

    if len(data) != 0:
        for index, item in enumerate(data):
            card = f"{hlink(item.get('Название'), item.get('Ссылка'))}\n" \
                f"{hbold('Старая цена: ')} {(item.get('Старая цена'))}\n" \
                f"{hbold('Цена со скидкой -')}{hbold(item.get('Скидка'))}:  {(item.get('Цена со скидкой'))} 🔥\n" \
                f"{hbold('Количество отзывов: ')} {(item.get('Количество отзывов'))}"

            await message.answer(card)

            if index % 20 == 0:
                time.sleep(3)

    else:
        await message.answer('В данной категории отсутствуют товары для отображения 😕')


@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ["Кроссовки", "Ботинки", "Полуботинки",
                     "Слипоны", "Кеды", "Клоги"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer('Мужская обувь размера 44-45 со скидкой в интернет-магазине Skechers',
                         reply_markup=keyboard)


@dp.message_handler(Text(equals='Кроссовки'))
async def get_discounts_running_shoes(message: types.Message):
    await message.answer('Пожалуйста, подождите... Собираю информацию с сайта...')

    collect_data(shoes_type='krossovki')

    await show_data(message)


@dp.message_handler(Text(equals='Ботинки'))
async def get_discounts_boots(message: types.Message):
    await message.answer('Пожалуйста, подождите... Собираю информацию с сайта...')

    collect_data(shoes_type='botinki')

    await show_data(message)


@dp.message_handler(Text(equals='Полуботинки'))
async def get_discounts_low_shoes(message: types.Message):
    await message.answer('Пожалуйста, подождите... Собираю информацию с сайта...')

    collect_data(shoes_type='polubotinki')

    await show_data(message)


@dp.message_handler(Text(equals='Слипоны'))
async def get_discounts_slipOns(message: types.Message):
    await message.answer('Пожалуйста, подождите... Собираю информацию с сайта...')

    collect_data(shoes_type='slipony')

    await show_data(message)


@dp.message_handler(Text(equals='Кеды'))
async def get_discounts_sneakers(message: types.Message):
    await message.answer('Пожалуйста, подождите... Собираю информацию с сайта...')

    collect_data(shoes_type='kedy')

    await show_data(message)


@dp.message_handler(Text(equals='Клоги'))
async def get_discounts_clogs(message: types.Message):
    await message.answer('Пожалуйста, подождите... Собираю информацию с сайта...')

    collect_data(shoes_type='klogi')

    await show_data(message)


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
