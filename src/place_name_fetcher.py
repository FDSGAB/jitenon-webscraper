import requests
from bs4 import BeautifulSoup

class PlaceNameFetcher():
    information_list = list()
    headers= {'user-agent':
          'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0',
          'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
          'accept-language': 'ja,pt-BR;q=0.9,pt;q=0.8,en-US;q=0.7,en;q=0.6'}


    def __init__(self, url : str) -> None:
        self.url = url
        self.information_list = list()
        self.get_page_info()
        self.fetch_information_from_table(content = self.soup)

    def get_page_info(self):
        page = requests.get(url = self.url, headers = self.headers, timeout = 10)
        self.soup = BeautifulSoup(page.content, "html.parser")

    def fetch_information_from_table(self, content : BeautifulSoup):
        try:
            table_of_contents_rows = content.find("div", {'id':'content'}).find("div", {'class':'area_list_all'}).find("div", {'class':'word_box'}).find('ul').find_all('li')
            for row in table_of_contents_rows:
                place_name = row.find("a").find('span', {'class':'word'}).get_text()
                area_name = row.find("a").find('span', {'class':'yomi'}).get_text()[1:-1]
                yomi = row.find("a").find('p', {'class':'data'}).get_text()
                self.information_list.append(['市区町村', place_name + '◦' + area_name + '◦' + yomi])
        except: pass
        try:
            table_of_contents_rows = content.find("div", {'id':'content'}).find_all("div", {'class':'area_list_all'})[1]
            table_of_contents_rows = table_of_contents_rows.find("div", {'class':'word_box'}).find('ul').find_all('li')
            for row in table_of_contents_rows:
                place_name = row.find("a").find('span', {'class':'word'}).get_text()
                area_name = row.find("a").find('span', {'class':'yomi'}).get_text()[1:-1]
                yomi = row.find("a").find('p', {'class':'data'}).get_text()
                self.information_list.append(['町域名', place_name + '◦' + area_name + '◦' + yomi])
        except: pass

    def fetch_result(self) -> list:
        return self.information_list