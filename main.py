import requests
from bs4 import BeautifulSoup
import json

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0'
}


def collect_data(shoes_type):
    url = f'https://www.sportmaster.ru/catalog/brendy/skechers/muzhskaya_obuv/?f-ware_grp=ware_grp_{shoes_type}&f-ra=size_44,size_45&f-promotion:globalpromo=true'
    response = requests.get(url=url, headers=headers)
    # with open('index.html') as file:
    #     src = file.read()
    soup = BeautifulSoup(response.text, 'lxml')
    try:
        shoes_items = soup.find('div', class_="sm-product-grid--size-xs") \
            .find_all('div', class_='sm-product-card__info')

        data = []
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
            # print(shoes_title, shoes_new_price, shoes_old_price, shoes_discount, shoes_reviews, '\n', shoes_url)
    except Exception:
        with open('result.json', 'w') as file:
            json.dump('', file, indent=4, ensure_ascii=False)


def main():
    collect_data(shoes_type='krossovki')


if __name__ == '__main__':
    main()
