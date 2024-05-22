from src.file_manager import FileManager
from src.kanji_links_writer import KanjiLinksWriter
from src.style.bcolors import bcolors

class Setup():

    counter = int(1)

    def __init__(self) -> None:
        KanjiLinksWriter()
        self.full_links_list = self.read_links_txt()
        if input(bcolors.WARNING + "Run from saved state files? Y/N: " + bcolors.ENDC) == 'N':
            FileManager().create_all_csv_files()
            FileManager().create_log_txt()
            self.save_counter_state(counter=1)
        self.counter = self.load_counter_state()
        """ if self.counter >= len(self.full_links_list):
            self.save_counter_state(counter=1)
            self.counter = self.load_counter_state() """
        self.number_of_runs = int(input(bcolors.WARNING + "Insert the number of runs to be made (insert 0 to run until the end): " + bcolors.ENDC))
        try:
            if self.counter + self.number_of_runs <= len(self.full_links_list):
                self.links_list = self.full_links_list[(self.counter - 1) : (self.counter + self.number_of_runs - 1)]
            else:
                self.links_list = self.full_links_list[(self.counter-1):]
        except:
            print(bcolors.FAIL + "ERROR OCCURED WITH NUMBER OF RUNS. SETTING DEFAULT TO 10" + bcolors.ENDC)
            self.links_list = self.full_links_list[(self.counter - 1) : (self.counter + 9)]


            
    def read_links_txt(self) -> list:
        while True:
            try:
                links_file = open(file ='bin/links.txt', encoding = 'UTF-8', mode = 'r')
                return links_file.read().split('\n')
            except PermissionError:
                print(bcolors.WARNING + "PERMISSION ERROR OCURRED!!!!" + bcolors.ENDC)
                continue
    
    def save_counter_state(self, counter : int):
        while True:
            try:
                counter_state = open(file='bin/counter.txt', encoding= 'UTF-8', mode='w')
                counter_state.write(str(counter))
                counter_state.close()
                break
            except PermissionError: 
                print(bcolors.WARNING + "PERMISSION ERROR OCURRED!!!!" + bcolors.ENDC)
                continue

    def load_counter_state(self) -> int:
        while True:
            try:
                counter_state = open(file='bin/counter.txt', encoding= 'UTF-8', mode='r')
                counter = int(counter_state.read())
                counter_state.close()
                return counter
            except PermissionError:
                print(bcolors.WARNING + "PERMISSION ERROR OCURRED!!!!" + bcolors.ENDC)
                continue