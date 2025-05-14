# Авторы скрипта: jrius & Grigory Tebenkov
# t.me/lcapybarov & t.me/dcapybarov

import requests
import time
import random
from PIL import Image, ImageDraw, ImageFont

BASE_URL = "https://pixelbattle.exfil-dev.ru"
LOGIN_ENDPOINT = "/api/auth.php?action=login"
PLACE_ENDPOINT = "/api/canvas.php?action=place"

USERNAME = "" # - Укажите Ваш username
PASSWORD = "123123" # - Укажите Ваш пароль от аккаунта

DEFAULT_DELAY = 2.10

def generate_random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return f"#{r:02x}{g:02x}{b:02x}"


def parse_color(color_input):
    if color_input == "#0":
        return None
    elif color_input.startswith("#") and len(color_input) == 7:
        return color_input.lower()
    else:
        raise ValueError("Неверный формат цвета. Используйте HEX (#FF0000) или #0 для случайных цветов")

def main():
    print("=== Настройка пиксель-бота ===")
    START_X = int(input("Введите координату X для начала текста: "))
    START_Y = int(input("Введите координату Y для начала текста: "))
    TEXT = input("Введите текст сообщения: ")

    while True:
        color_input = input("Введите цвет (HEX #RRGGBB или #0 для случайных цветов): ")
        try:
            COLOR = parse_color(color_input)
            break
        except ValueError as e:
            print(f"Ошибка: {e}. Попробуйте снова.")

    delay_input = input(f"Введите задержку между пикселями (по умолчанию {DEFAULT_DELAY}): ")
    DELAY = float(delay_input) if delay_input else DEFAULT_DELAY

    session = requests.Session()
    resp = session.post(BASE_URL + LOGIN_ENDPOINT, json={
        "username": USERNAME,
        "password": PASSWORD
    })

    if not resp.ok or "user" not in resp.json():
        print("❌ Ошибка входа:", resp.text)
        exit()

    print("✅ Успешный вход!")

    def get_text_pixels(text, font_size=10):
        font = ImageFont.load_default()
        image = Image.new("1", (500, 100))
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), text, font=font, fill=1)
        pixels = image.load()
        coords = []
        for y in range(image.height):
            for x in range(image.width):
                if pixels[x, y] == 1:
                    coords.append((x, y))
        return coords

    text_pixels = get_text_pixels(TEXT)
    print(f"🔢 Найдено {len(text_pixels)} пикселей для текста.")

    for index, (dx, dy) in enumerate(text_pixels):
        x = START_X + dx
        y = START_Y + dy

        current_color = generate_random_color() if COLOR is None else COLOR

        response = session.post(BASE_URL + PLACE_ENDPOINT, json={
            "x": x,
            "y": y,
            "color": current_color
        })

        if response.ok:
            print(f"✅ [{index + 1}/{len(text_pixels)}] Пиксель поставлен на ({x}, {y}) цвет {current_color}")
        else:
            print(f"❌ [{index + 1}] Ошибка на ({x}, {y}): {response.text}")

        time.sleep(DELAY)

if __name__ == "__main__":
    main()