import requests
import time
from bs4 import BeautifulSoup
import re
import json

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0'
}


def collect_data():
    url = 'https://www.skechers.ru/catalog/muzhchinam/obuv/?f-promotion%3Aglobalpromo=true&f-ra=size_44%2Csize_45'
    response = requests.get(url=url, headers=headers)

    with open('index.html', 'w') as file:
        file.write(response.text)

    time.sleep(5)

    with open('index.html') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    pages_count = int(soup.find_all('a', class_="pager__item")[-2].text)
    url = f'https://www.skechers.ru/catalog/muzhchinam/obuv/?f-promotion%3Aglobalpromo=true&f-ra=size_44%2Csize_45&pages={pages_count}'
    response = requests.get(url=url, headers=headers)
    with open('index_all_pages.html', 'w') as file:
        file.write(response.text)

    with open('index_all_pages.html') as file:
        soup = BeautifulSoup(file, 'lxml')

    shoes_items = soup.find_all('div', class_="catalog__item")

    data = []
    for shoes_item in shoes_items:
        shoes_title = shoes_item.find('a', class_='product-small-card__title').text
        shoes_url = 'https://www.skechers.ru' + \
                    shoes_item.find('a', class_="product-small-card__img-container").get('href')
        shoes_new_price = shoes_item.find('div', class_="product-small-card__old-price")\
            .find_previous_sibling().text.replace('₽', '').strip()
        shoes_old_price = shoes_item.find('div', class_="product-small-card__old-price")\
            .text.replace('₽', '').strip()
        shoes_discount = shoes_item.find('div', class_="product-small-card__discount")\
            .text.replace('-', '')

        try:
            shoes_reviews = shoes_item.find('a', class_="rating-summary__rating-label")\
                .text
        except:
            shoes_reviews = 'Нет отзывов'

        if re.search('^Кроссовки', shoes_title):
            shoes_category = 'Кроссовки'
        elif re.search('^Ботинки', shoes_title):
            shoes_category = 'Ботинки'
        elif re.search('^Полуботинки', shoes_title):
            shoes_category = 'Полуботинки'
        elif re.search('^Слипоны', shoes_title):
            shoes_category = 'Слипоны'
        elif re.search('^Кеды', shoes_title):
            shoes_category = 'Кеды'
        elif re.search('^Клоги', shoes_title):
            shoes_category = 'Клоги'
        else:
            shoes_category = 'Другое'
        # try:
        #     shoes_image = shoes_item.find('img').get('src')
        # except:
        #     shoes_image = 'Нет картинки'
        # print(shoes_title, shoes_new_price, shoes_old_price, shoes_discount, shoes_reviews,
        #       shoes_url, '\n', shoes_image)
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


def main():
    collect_data()


if __name__ == '__main__':
    main()
