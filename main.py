import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup, ResultSet
import requests

class ParsedDecks:
    def __init__(self):
        self.decks: list[dict] = []
        
    def get_top_10(self) -> list[dict]:
        return sorted(self.decks, key=lambda d: d["percent"], reverse=True)[:10] 
    
    def append(self, deck:dict):
        self.decks.append(deck)
        
def scrap() -> list[dict]:
    parsed_decks = ParsedDecks()
    mtg_top8 = requests.get("https://www.mtgtop8.com/format?f=MO&meta=54&a=")
    soup = BeautifulSoup(mtg_top8.text, "html.parser")
    decks: list[ResultSet] = soup.findAll("div", attrs={"class":"hover_tr"})
    for deck in decks[18:]:
        img = deck.findAll("img", limit=1)
        text = deck.text.split("\n")[4:7]
        parsed_decks.append(
            {
                "name": text[0],
                "percent": float(text[2][:-2]),
                "image": "https://www.mtgtop8.com" + str(img[0]['src'])
            }
        )
    return parsed_decks.get_top_10()

def plot(decks: list[dict]) -> None:
    decks.reverse()
    print(plot)
    height = 0.8
    percent = [d["percent"] for d in decks]
    name = [d["name"] for d in decks]
    plt.figure(figsize=(15,15))
    color = ['tomato', 'tomato', 'tomato', 'tomato', 'khaki', 'khaki', 'khaki', 'springgreen', 'springgreen', 'springgreen']
    plt.barh(
        y=name, 
        width=percent, 
        color=color,
        height=height, 
        align='center'
    )
    plt.ylim(-0.5, 10 - 0.5)
    plt.rcParams["figure.figsize"] = [15, 15]
    plt.title('Top 10 Modern Decks', fontsize=30)
    plt.xlabel('Meta Percentage', fontsize=20)
    plt.savefig('mtg_bar.jpg', transparent=True)

if __name__ == "__main__":
    plot(scrap())