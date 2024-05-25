import requests
from bs4 import BeautifulSoup

class WordInformationFetcher():
    information_list = list()
    headers= {'user-agent':
          'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0',
          'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
          'accept-language': 'ja,pt-BR;q=0.9,pt;q=0.8,en-US;q=0.7,en;q=0.6'}


    def __init__(self, url : str) -> None:
        self.url = url
        self.information_list = list()
        self.get_page_info()
        self.fetch_all_information()

    def get_page_info(self):
        page = requests.get(url = self.url, headers = self.headers, timeout = 10)
        self.soup = BeautifulSoup(page.content, "html.parser")

    def fetch_information_from_table(self, content : BeautifulSoup):
      table_of_contents_rows = content.find("div", {'class':'word_box'}).find('ul').find_all('li')
      for row in table_of_contents_rows:
          word = row.find('span', {'class':'word'}).get_text()
          yomi = row.find('span', {'class':'yomi'}).get_text()[1:-1]
          try: meaning = row.find('p').get_text()
          except: meaning = 'NULL'
          self.information_list.append(['言葉', word + '◦' + yomi + '◦' + meaning])

    def next_page(self, content : BeautifulSoup):
      self.url = content.find("div", {'class':'pagination2'}).find("div", {'class':'next'}).find('a')['href']
      self.get_page_info()

    def fetch_all_information(self):
      while True:
        self.fetch_information_from_table(content = self.soup)
        #print(self.soup.find("div", {'class':'pagination2'}).find("div", {'class':'next'}).find('a'))
        if self.soup.find("div", {'class':'pagination2'}).find("div", {'class':'next'}).find('a') == None:
          break
        self.next_page(content = self.soup)

    def fetch_result(self) -> list:
        return self.information_list