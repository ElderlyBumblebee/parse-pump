import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time


base_url = "https://arosna.com/shop/folder/zapasnyye-chasti-uzly-detali-k-nasosam-k-1k-2k-gorizontalnym-tsentrobezhnym-konsolnym-vodyanym/p/{}"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/140.0.0.0 Safari/537.36"
}

data = []


# Проходим по 5 страницам
for page in range(1, 6):

    url = base_url.format(page)

    print(f"Парсим страницу {page}: {url}")

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Ошибка на странице {page}: {response.status_code}")
        continue

    soup = BeautifulSoup(response.text, "html.parser")

    products = soup.find_all(
        "form",
        class_="shop2-product-item"
    )

    print(f"Найдено товаров: {len(products)}")

    for product in products:

        # Название
        name_element = product.find("div", class_="product-name")
        name = name_element.get_text(strip=True) if name_element else ""

        # Ссылка
        link = ""
        if name_element and name_element.find("a"):
            link = name_element.find("a").get("href", "")
            link = urljoin(url, link)

        # Артикул
        article = ""
        article_element = product.find("div", class_="product-article")

        if article_element:
            span = article_element.find("span")

            if span:
                article = span.next_sibling.strip()

        # Цена
        price = ""
        price_element = product.find("div", class_="price-current")

        if price_element:
            strong = price_element.find("strong")

            if strong:
                price = strong.get_text(strip=True)

        # Добавляем товар
        data.append({
            "Название": name,
            "Артикул": article,
            "Цена": price,
            "Ссылка": link,
            "Страница": page
        })

    # Небольшая пауза между запросами
    time.sleep(1)


# Создаём DataFrame
df = pd.DataFrame(data)

print()
print(f"Всего товаров: {len(df)}")

# Сохраняем Excel
df.to_excel("товары.xlsx", index=False)

print("Готово! Файл сохранён: товары.xlsx")