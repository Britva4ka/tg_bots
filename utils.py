import requests
from lxml import html
from PIL import Image, ImageDraw, ImageFont
import textwrap
import random
from bs4 import BeautifulSoup

def get_anecdote():
    page = requests.get('https://anekdotov.net/anekdot/')
    body = html.fromstring(page.content)
    anecdote_divs = body.xpath('//div[@class="anekdot"]')
    result = []
    for div in anecdote_divs:
        p_elements = div.xpath('.//p')
        div_text = ''.join([p.text for p in p_elements if p.text])
        result.append(div_text)
    return result


def get_compliment():
    page = requests.get('https://gilber.one/komplimenty-devushke.html')
    body = html.fromstring(page.content)
    li_elements = [elem[0].lower() + elem[1:] for elem in body.xpath('//li/text()') if elem.strip()]
    return li_elements


def draw_text(text):
    # размеры картинки
    width = 800
    height = 400
    # создаем новую картинку с голубым фоном
    image = Image.new('RGB', (width, height), (135, 206, 250))
    # создаем объект ImageDraw для рисования на картинке
    draw = ImageDraw.Draw(image)
    # устанавливаем начальный размер шрифта
    font_size = 25
    # увеличиваем размер шрифта, пока текст не заполнит картинку достаточно плотно
    while True:
        # устанавливаем шрифт
        font = ImageFont.truetype('arial.ttf', font_size)
        # разбиваем текст на строки с помощью метода textwrap.wrap()
        lines = textwrap.wrap(text, width=int(0.8*width/font_size))
        # проверяем, заполняет ли текст картинку достаточно плотно
        if all(font.getsize(line)[0] < 0.8*width for line in lines) and font.getsize(max(lines, key=len))[1] < 0.8*height:
            break
        # увеличиваем размер шрифта и повторяем цикл
        font_size += 1
    # рисуем текст по центру картинки
    y_text = (height - font_size * len(lines)) / 2
    for line in lines:
        line_width, line_height = draw.textsize(line, font=font)
        x_text = (width - line_width) / 2
        draw.text((x_text, y_text), line, font=font, fill=(255, 20, 147))
        y_text += line_height
    # возвращаем картинку как объект Image
    return image





