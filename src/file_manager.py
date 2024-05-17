import pandas as pd
from src.style.bcolors import bcolors
import csv

class FileManager():

    firstrow_dictionary = {
                            'data/kanjireadings.csv' : ['漢字','音訓','読み', '送り仮名', '学年', '表内読み'],
                            'data/kanjigeneralinfo.csv' : ['漢字', '画数', '成り立ち', '学年', '漢字検定', 'JIS水準', '漢字について', '補足'],
                            'data/kanjimeanings.csv' : ['漢字', '意味', 'その他'],
                            'data/kanjivariant.csv' : ['漢字', '異体字'],
                            'data/kanjikousei.csv' : ['漢字', '漢字構成'],
                            'data/kanjinamereadings.csv' : ['漢字', '名乗り訓'],
                            'data/kanjicodes.csv' : ['漢字', '文字コード', 'コード', 'その他'],
                            'data/kanjidictionarynumbers.csv' : ['漢字', '辞典', '検字番号'],
                            'data/kanjibushu.csv' : ['漢字', '部首', '部首の読み方'],
                            'data/kanjibunrui.csv' :['漢字', '分類'],
                            'data/kanjishubetsu.csv' :['漢字', '種別'],
                        }

    def create_csv_file(self, file_name : str, firstrow : list):
        with open(file_name, encoding='UTF-8', mode='w') as readings_file:
            readings_writer = csv.writer(readings_file, delimiter=',', quotechar='"', lineterminator='\n')
            readings_writer.writerow(firstrow)
            readings_file.close()

    def create_all_csv_files(self):
        for file in self.firstrow_dictionary.items():
            self.create_csv_file(file[0], file[1])


    def write_entry(self, file_name : str, line : list):
        while True:
            try:
                with open(file_name, encoding='UTF-8', mode='a') as file:
                    writer = csv.writer(file, delimiter=',', quotechar='"', lineterminator='\n')
                    writer.writerow(line)
                    file.close()
                    break
            except PermissionError:
                print(bcolors.WARNING + "PERMISSION ERROR OCURRED!!!!" + bcolors.ENDC)
                continue


    def delete_the_last_x_rows_of_file(self, file_string : str, x : int):
        if x <= 0: return
        file = open(file_string, encoding='UTF-8', mode = "r")
        lines = file.readlines()
        lines = lines[:-x]
        file.close()
        file = open(file_string, encoding='UTF-8', mode = "w")
        file.writelines(lines)
        file.close()

    def create_log_txt(self):
        file = open('log/log.txt', encoding='UTF-8', mode = "w")
        file.write("LOG:\n")
        file.close()

    def write_in_log_txt(self, string : str):
        file = open('log/log.txt', encoding='UTF-8', mode = "a")
        file.write(string)
        file.close()

    def entry_was_successfull(self, kanji : str, file_name : str, number_of_entries_found : int) -> tuple:
        info = pd.read_csv(file_name, encoding='UTF-8', delimiter=',', index_col = False, usecols=[0]) 
        entries_in_file = info["漢字"].loc[info["漢字"] == kanji].count()
        if entries_in_file == number_of_entries_found: return (0, entries_in_file)
        if entries_in_file != number_of_entries_found: 
            error_string = "Error in " + kanji + " found in: " + file_name + "\nEntries in csv: " + str(entries_in_file) + "\nEntries found: " + str(number_of_entries_found) + "\n"
            print(bcolors.FAIL + error_string + bcolors.ENDC)
            self.write_in_log_txt(error_string)
            return (1, entries_in_file)
