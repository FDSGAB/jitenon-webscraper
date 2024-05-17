import requests
from bs4 import BeautifulSoup

class CurrentKanjiCount():

    homepage_url = 'https://kanji.jitenon.jp'

    def get_count(self) -> int:
        page = requests.get(self.homepage_url)
        soup = BeautifulSoup(page.content, "html.parser")
        entries = soup.find('body').find("p", {'class':'textnum'}).find("span", {'class':'marker'}).text
        return int(entries)