import requests
from bs4 import BeautifulSoup as soup
from PIL import Image
import os
from io import BytesIO


class Rune:
    """
    Rune class gets user input (input is a LoL champion) and creates a new png file on user desktop with runes to
    champion.
    """

    def __init__(self):
        self.to_avoid = [' i ', 'willump', '\'', '4', '.', '&', ',', ' ']
        self.runes = []
        self.positions = [(50, 100), (200, 150), (50, 200), (50, 300), (50, 400), (50, 500), (200, 250), (200, 350),
                          (400, 500), (400, 550), (400, 600)]
        self.path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') + "\\runes.png"

    def get_champion(self):
        champion = str(input('Podaj bohatera: ').strip().lower())
        # formatting input
        for ch in self.to_avoid:
            if ch == self.to_avoid[3]:
                champion = champion.replace(ch, 'iv')
            if ch in champion:
                champion = champion.replace(ch, '')

        url = f'https://eune.op.gg/champion/{champion}/statistics'
        self.page = requests.get(url)
    def parse_page(self):
        self.html = soup(self.page.content, 'html.parser')
        # table with necessary data
        tbody = self.html.find('tbody', class_="tabItem ChampionKeystoneRune-1")
        tr = tbody.find('tr')

        self.main_runes = tr.find_all('div', class_='perk-page__item--active')
        self.optional_runes = tr.find_all('img', class_='active tip')

    def get_images(self):
        main_runes = self.html.find_all('div', class_="perk-page__item perk-page__item--mark")

        # adding main paths of runes to rune list
        self.runes.append(f'https:{str(main_runes[0].find("img").get("src"))}')
        self.runes.append(f'https:{str(main_runes[1].find("img").get("src"))}')

        # adding main runes to rune list
        for img in self.main_runes:
            self.runes.append(f"https:{img.find('img').get('src')}")

        # adding optional runes to rune list
        for img in self.optional_runes:
            self.runes.append(f"https:{img.get('src')}")

    def print_runes_on_desktop(self):
        # creating a background to paste runes img's
        bg = Image.new('RGBA', (700, 700), (0, 0, 0, 1))
        # pasting runes to background
        counter = 0
        for link in self.runes:
            content = requests.get(link).content
            if counter <= 7:
                img = Image.open(BytesIO(content)).resize((75, 75))
                bg.paste(img, self.positions[counter])
            else:
                img = Image.open(BytesIO(content))
                bg.paste(img, self.positions[counter])
            counter += 1

            bg.save(self.path, quality=100)
