import requests
from bs4 import BeautifulSoup
from src.contained_in_kanji_fetcher import ContainedInKanjiFetcher
from src.kotozawa_information_fetcher import KotozawaInformationFetcher
from src.last_name_information_fetcher import LastNameInformationFetcher
from src.name_information_fetcher import NameInformationFetcher
from src.place_name_fetcher import PlaceNameFetcher
from src.word_information_fetcher import WordInformationFetcher
from src.yoji_information_fetcher import YojiInformationFetcher


class KanjiInformationFetcher():

    information_list = list()
    headers= {'user-agent': 
          'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0',
          'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
          #'accept-encoding': 'gzip, deflate, br',
          'accept-language': 'ja,pt-BR;q=0.9,pt;q=0.8,en-US;q=0.7,en;q=0.6'}


    def __init__(self, url : str) -> None:
        self.url = url
        self.information_list = list()
        self.get_page_info()
        self.fetch_all_information()
        """ for element in self.information_list:
            print(element) """

    def fetch_result(self) -> list:
        return self.information_list

    def get_page_info(self):
        while True:
            try:
                page = requests.get(url = self.url, headers = self.headers, timeout = 10)
                if page.url == self.url:
                    break   
            except: pass 
        self.soup = BeautifulSoup(page.content, "html.parser")
    
    def fetch_information_from_list(self, content : BeautifulSoup, subject : str):
        list_rows = content.find_all('li')
        for row in list_rows:
            row_additional_info = str('')
            row_info = row.get_text()
            try: row_additional_info = '◦' + row.find('img')['alt'] + '◦'
            except: pass
            self.information_list.append([subject, row_additional_info + row_info])
        

    def fetch_informartion_from_content_table(self, content : BeautifulSoup):
        table_of_contents_rows = content.find_all('tr')
        for row in table_of_contents_rows:
            row_additional_info = str('')
            try: row_subject = row.find('th').get_text()
            except AttributeError: row_subject = last_row_subject
            try: row_additional_info = '◦' + row.find('td').find('img')['alt'] + '◦'
            except: pass
            try: row_info = row.find('td').get_text()
            except AttributeError: row_info = last_row_info
            last_row_subject = row_subject
            last_row_info = row_info
            self.information_list.append([row_subject, row_additional_info + row_info])


    def fetch_simple_string_from_content(self, content : BeautifulSoup, subject : str):
        content_string = "".join(("".join(content.get_text().strip().split('\n'))).split('\r'))
        self.information_list.append([subject, content_string])


    def fetch_all_information(self):
        self.fetch_kanji_basic_information()
        self.fetch_kanji_about_information()
        self.fetch_kanji_code_information()
        self.fetch_kanji_number_information()
        self.fetch_kanji_variant_information()
        self.fetch_kanji_kousei_information()
        self.fetch_kanji_namereadings_information()
        self.fetch_kanji_footnote_information()
        self.fetch_kanji_names_information()
        self.fetch_kanji_myouji_information()
        self.fetch_kanji_include_information()
        self.fetch_kanji_nandoku_information()
        self.fetch_kanji_joyohuhyo_information()
        self.fetch_kanji_chimei_information()
        self.fetch_kanji_word_information()
        self.fetch_kanji_yoji_information()
        self.fetch_kanji_kotozawa_information()
        self.information_list.append(['URL',self.url])
        

    def fetch_kanji_basic_information(self):
        general_content = self.soup.find('body').find("div", {'class':'search_data'}).find("div", {'class':'kanji_right'})
        kanji = general_content.find('h2').text[1:2]
        self.information_list.append(['漢字', kanji])
        general_content = general_content.find("table", {'class':'kanjirighttb'})
        self.fetch_informartion_from_content_table(general_content)

    def fetch_kanji_code_information(self):
        kanji_code_content = self.soup.find('body').find("div", {'class':'search_data'}).find("table", {'class':'moji_code'})
        self.fetch_informartion_from_content_table(kanji_code_content)

    def fetch_kanji_number_information(self):
        kanji_number_content = self.soup.find('body').find("div", {'class':'search_data'}).find("table", {'class':'keji_number'})
        self.fetch_informartion_from_content_table(kanji_number_content)

    def fetch_kanji_about_information(self):
        try:
            about_content = self.soup.find('body').find("div", {'class':'search_data'}).find("div", {'class':'kanji_about'}) 
            self.fetch_simple_string_from_content(about_content, subject = '漢字について')
        except AttributeError: self.information_list.append(['漢字について', 'NULL'])

    def fetch_kanji_variant_information(self):
        try:
            variant_kanji_content = self.soup.find('body').find("div", {'class':'search_data'}).find("div", {'class':'data_cont it_wrap2'})
            self.fetch_simple_string_from_content(variant_kanji_content, subject = '異体字')
        except AttributeError: pass

    def fetch_kanji_kousei_information(self):
        try:
            kanji_kousei_content = self.soup.find('body').find("div", {'class':'search_data'}).find("h2", {'id':'m_kousei'}).find_previous()
            self.fetch_information_from_list(kanji_kousei_content, subject = '漢字構成')
        except AttributeError: pass

    def fetch_kanji_namereadings_information(self):
        try:
            kanji_namereadings_content = self.soup.find('body').find("div", {'class':'search_data'}).find("h2", {'id':'m_name'}).find_previous() 
            self.fetch_information_from_list(kanji_namereadings_content, subject = '名乗り読み')
        except AttributeError: pass

    def fetch_kanji_nandoku_information(self):
        try:
            kanji_nandoku_content = self.soup.find('body').find("div", {'class':'search_data'}).find("h2", {'id':'m_nandoku'}).find_previous().find('ul', {'class':'row2'})
            self.fetch_information_from_list(kanji_nandoku_content, subject = '難読')
        except AttributeError: pass

    def fetch_kanji_joyohuhyo_information(self):
        try:
            kanji_joyohuhyo_content = self.soup.find('body').find("div", {'class':'search_data'}).find("h2", {'id':'m_joyohuhyo'}).find_previous().find('ul')
            self.fetch_information_from_list(kanji_joyohuhyo_content, subject = '常用漢字表付表の語')
        except AttributeError: pass
    
    def fetch_kanji_names_information(self):
        try:
            names_url = self.soup.find('body').find("div", {'class':'search_data'}).find("h2", {'id':'m_name_site'}).find_previous().find("a", {'class':'outside_link'})['href']
            name_informations_list = NameInformationFetcher(url = names_url).fetch_result() 
            for name_entry in name_informations_list:
                self.information_list.append(name_entry)
        except TypeError:
            name_content = self.soup.find('body').find("div", {'class':'search_data'}).find("h2", {'id':'m_name_site'}).find_previous().find('ul', {'class':'one_row'})  
            self.fetch_information_from_list(name_content, subject = '名前')
        except AttributeError: pass

    def fetch_kanji_include_information(self):
        try:
            kanji_include_content_url = self.soup.find('body').find("div", {'class':'search_data'}).find("h2", {'id':'m_include'}).find_previous().find("a", {'class':'outside_link'})['href']
            include_content_list = ContainedInKanjiFetcher(url = kanji_include_content_url).fetch_result() 
            for entry in include_content_list:
                self.information_list.append(entry)
        except TypeError:
            kanji_include_content = self.soup.find('body').find("div", {'class':'search_data'}).find("h2", {'id':'m_include'}).find_previous().find('ul', {'class':'one_row'}) 
            self.fetch_information_from_list(kanji_include_content, subject = '含む漢字')
        except AttributeError: pass

    
    def fetch_kanji_myouji_information(self): 
        try:
            last_names_url = self.soup.find('body').find("div", {'class':'search_data'}).find("h2", {'id':'m_myoji'}).find_previous().find("a", {'class':'outside_link'})['href']
            last_name_informations_list = LastNameInformationFetcher(url = last_names_url).fetch_result() 
            for last_name_entry in last_name_informations_list:
                self.information_list.append(last_name_entry)
        except TypeError:
            last_name_content = self.soup.find('body').find("div", {'class':'search_data'}).find("h2", {'id':'m_myoji'}).find_previous().find('ul', {'class':'one_row'})  
            self.fetch_information_from_list(last_name_content, subject = '名字')
        except AttributeError: pass

    def fetch_kanji_chimei_information(self):
        try:
            place_name_content_url = self.soup.find('body').find("div", {'class':'search_data'}).find("h2", {'id':'m_chimei'}).find_previous().find("a", {'class':'outside_link'})['href']
            place_name_list = PlaceNameFetcher(url = place_name_content_url).fetch_result() 
            for entry in place_name_list:
                self.information_list.append(entry)
        except TypeError:
            kanji_chimei_content = self.soup.find('body').find("div", {'class':'search_data'}).find("h2", {'id':'m_chimei'}).find_previous().find('ul', {'class':'one_row'})  
            self.fetch_information_from_list(kanji_chimei_content, subject = '地名')
        except AttributeError: pass


    def fetch_kanji_word_information(self):
        try:
            word_content_url = self.soup.find('body').find("div", {'class':'search_data'}).find("h2", {'id':'m_word'}).find_previous().find("a", {'class':'more_btn_long'})['href']
            word_name_list = WordInformationFetcher(url = word_content_url).fetch_result() 
            for entry in word_name_list:
                self.information_list.append(entry)
        except TypeError:
            kanji_word_content = self.soup.find('body').find("div", {'class':'search_data'}).find("h2", {'id':'m_word'}).find_previous().find('ul')   
            self.fetch_information_from_list2(kanji_word_content, subject = '言葉')
        except AttributeError: pass

    def fetch_kanji_yoji_information(self):
        try:
            yoji_content_url = self.soup.find('body').find("div", {'class':'search_data'}).find("h2", {'id':'m_yoji'}).find_previous().find("a", {'class':'more_btn_long'})['href']
            yoji_list = YojiInformationFetcher(url = yoji_content_url).fetch_result() 
            for entry in yoji_list:
                self.information_list.append(entry)
        except TypeError:
            kanji_yoji_content = self.soup.find('body').find("div", {'class':'search_data'}).find("h2", {'id':'m_yoji'}).find_previous().find('ul') 
            self.fetch_information_from_list2(kanji_yoji_content, subject = '四字熟語')
        except AttributeError: pass

    def fetch_kanji_kotozawa_information(self):
        try:
            kotozawa_content_url = self.soup.find('body').find("div", {'class':'search_data'}).find("h2", {'id':'m_kotowaza'}).find_previous().find("a", {'class':'more_btn_long'})['href']
            kotozawa_list = KotozawaInformationFetcher(url = kotozawa_content_url).fetch_result() 
            for entry in kotozawa_list:
                self.information_list.append(entry)
        except TypeError:
            kanji_kotozawa_content = self.soup.find('body').find("div", {'class':'search_data'}).find("h2", {'id':'m_kotowaza'}).find_previous().find('ul')  
            self.fetch_information_from_list2(kanji_kotozawa_content, subject = 'ことわざ')
        except AttributeError: pass

    def fetch_kanji_footnote_information(self):
        try:
            footnote_content = self.soup.find('body').find("div", {'class':'search_data'}).find("div", {'class':'hosoku_display'}).find('h3').find_previous()
            self.fetch_simple_string_from_content(footnote_content, subject = '補足')
        except AttributeError: self.information_list.append(['補足', 'NULL'])


    def fetch_information_from_list2(self, content : BeautifulSoup, subject : str):
        list_rows = content.find_all('li')
        for row in list_rows:
            try: meaning = row.find('a')['data-content']
            except: meaning = 'NULL'
            word = row.find('span', {'class':'word'}).get_text()
            yomi = row.find('span', {'class':'yomi'}).get_text()[1:-1]
            self.information_list.append([subject, word + '◦' + yomi + '◦' + meaning])

if __name__ == '__main__':
    test_url = "https://kanji.jitenon.jp/kanji/001.html"
    #test_url = "https://kanji.jitenon.jp/kanji/143.html"
    test_url = "https://kanji.jitenon.jp/kanjiy/28220.html"
    KanjiInformationFetcher(url=test_url)