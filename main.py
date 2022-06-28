import requests
from bs4 import BeautifulSoup
import json

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0'
}


def collect_data(shoes_type):
    url = f'https://www.skechers.ru/catalog/muzhchinam/obuv/?f-promotion%3Aglobalpromo=true&f-ware_grp=ware_grp_{shoes_type}&f-ra=size_44%2Csize_45'
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
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
        # try:
        #     shoes_image = shoes_item.find('img').get('src')
        # except:
        #     shoes_image = 'Нет картинки'
        # print(shoes_title, shoes_new_price, shoes_old_price, shoes_discount, shoes_reviews,
        #       shoes_url, '\n', shoes_image)
        data.append(
            {
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
    collect_data(shoes_type='krossovki')


if __name__ == '__main__':
    main()
