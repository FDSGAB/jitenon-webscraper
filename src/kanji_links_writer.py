from src.current_kanji_count import CurrentKanjiCount
import string

class KanjiLinksWriter():
       
    link_first_part = 'https://kanji.jitenon.jp/kanji'
    link_last_part = '.html'
    counter = 0
    

    def __init__(self) -> None:
        self.entries = CurrentKanjiCount().get_count()
        self.link_list = list()
        self.alphabet_list = list(string.ascii_lowercase)
        self.create_link_strings()
        self.write_links_in_txt()
    
    
    def create_link_strings(self):
        for letter in self.alphabet_list:
            self.counter = self.counter + 1
            while True:               
                counter_string =  self.counter_string_creator()
                letter_string = self.letter_string_creator(letter=letter)
                link_middle_part = letter_string + '/' + counter_string
                self.link_list.append(self.link_first_part + link_middle_part + self.link_last_part)
                if (self.counter % 500 == 0 and letter != 'y') or (letter == 'y' and  self.counter == self.entries): break
                self.counter = self.counter + 1
            if self.counter == self.entries: break

    def write_links_in_txt(self):
        links_file = open("links.txt", "w")
        links_file.write("\n".join(self.link_list))
        links_file.close()


    def counter_string_creator(self) -> str:
        if self.counter < 10: return '00' + str(self.counter)
        elif self.counter < 100: return '0' + str(self.counter)
        else: return str(self.counter)

    def letter_string_creator(self, letter : str) -> str:
        if letter == 'a': return ''
        else: return letter