from src.kanji_links_writer import KanjiLinksWriter
from src.kanji_information_fetcher import KanjiInformationFetcher
from src.information_organizer import InformationOrganizer
from src.file_manager import FileManager
import datetime
import numpy as np
from src.style.bcolors import bcolors

def read_links_txt() -> list:
    links_file = open(file ='links.txt', encoding = 'UTF-8', mode = 'r')
    return links_file.read().split('\n')

def write_kanji_general_info(data : InformationOrganizer) -> tuple:
    FileManager().write_entry('data/kanjigeneralinfo.csv', data.general_information_list)
    return FileManager().entry_was_successfull(data.kanji, 'data/kanjigeneralinfo.csv', 1)

def write_kanji_info_list(kanji : str, file: str, data_list : list) -> tuple:
    for entry in data_list:
        FileManager().write_entry(file, entry)
    return FileManager().entry_was_successfull(kanji, file, len(data_list))

def delete_previous_written_entries(controls_list : list):
    for control in controls_list:
        FileManager().delete_the_last_x_rows_of_file(control[0], control[1])

def write_all_infos(data : InformationOrganizer) -> bool:
    controls_list = list()
    general_control = write_kanji_general_info(data)
    controls_list.append(['data/kanjigeneralinfo.csv', general_control[1]])
    if general_control[0] == 1:
        delete_previous_written_entries(controls_list)
        return True
    readings_control = write_kanji_info_list(data.kanji, 'data/kanjireadings.csv', data.readings_list)
    controls_list.append(['data/kanjireadings.csv', readings_control[1]])
    if readings_control[0] == 1:
        delete_previous_written_entries(controls_list)
        return True
    meanings_control = write_kanji_info_list(data.kanji, 'data/kanjimeanings.csv', data.meanings_list)
    controls_list.append(['data/kanjimeanings.csv', meanings_control[1]])
    if meanings_control[0] == 1:
        delete_previous_written_entries(controls_list)
        return True
    numeration_control = write_kanji_info_list(data.kanji, 'data/kanjidictionarynumbers.csv', data.kanji_dictionary_number_list)
    controls_list.append(['data/kanjidictionarynumbers.csv', numeration_control[1]])
    if numeration_control[0] == 1:
        delete_previous_written_entries(controls_list)
        return True
    code_control = write_kanji_info_list(data.kanji, 'data/kanjicodes.csv', data.kanji_code_list)
    controls_list.append(['data/kanjicodes.csv', code_control[1]])
    if code_control[0] == 1:
        delete_previous_written_entries(controls_list)
        return True
    bushu_control = write_kanji_info_list(data.kanji, 'data/kanjibushu.csv', data.kanji_bushu_list)
    controls_list.append(['data/kanjibushu.csv', bushu_control[1]])
    if bushu_control[0] == 1:
        delete_previous_written_entries(controls_list)
        return True
    variant_form_control = write_kanji_info_list(data.kanji, 'data/kanjivariant.csv', data.variant_forms_list)
    controls_list.append(['data/kanjivariant.csv', variant_form_control[1]])
    if variant_form_control[0] == 1:
        delete_previous_written_entries(controls_list)
        return True
    name_readings_control = write_kanji_info_list(data.kanji, 'data/kanjinamereadings.csv', data.name_readings_list)
    controls_list.append(['data/kanjinamereadings.csv', name_readings_control[1]])
    if name_readings_control[0] == 1:
        delete_previous_written_entries(controls_list)
        return True
    kousei_control = write_kanji_info_list(data.kanji, 'data/kanjikousei.csv', data.kanjikousei_list)
    controls_list.append(['data/kanjikousei.csv', kousei_control[1]])
    if kousei_control[0] == 1:
        delete_previous_written_entries(controls_list)
        return True
    bunrui_control = write_kanji_info_list(data.kanji, 'data/kanjibunrui.csv', data.bunrui_list)
    controls_list.append(['data/kanjibunrui.csv', bunrui_control[1]])
    if bunrui_control[0] == 1:
        delete_previous_written_entries(controls_list)
        return True
    shubetsu_control = write_kanji_info_list(data.kanji, 'data/kanjishubetsu.csv', data.shubetsu_list)
    controls_list.append(['data/kanjishubetsu.csv', shubetsu_control[1]])
    if shubetsu_control[0] == 1:
        delete_previous_written_entries(controls_list)
        return True
    return False

def main():
    time_list = list()
    counter = int(1)
    FileManager().create_all_csv_files()
    FileManager().create_log_txt()
    KanjiLinksWriter()
    links_list = read_links_txt()
    for link in links_list:
        needs_reprocessing = False
        while True:
            current_time = datetime.datetime.now()
            if counter%100 == 0 or counter == 1:
                print(bcolors.OKGREEN + "Run number: " + str(counter) + "/" + str(len(links_list)) + " " + str(round(100*counter/len(links_list), 2)) + "%, URL: " + link + bcolors.ENDC)
            info_list = KanjiInformationFetcher(url = link).fetch_result()
            data = InformationOrganizer(information_list = info_list)
            if data.kanji == '': continue
            needs_reprocessing = write_all_infos(data)
            time_list.append(datetime.datetime.now() - current_time)
            if counter%100 == 0 or counter == 1:
                print("Estimated time for conclusion: ", str(np.mean(time_list)*(len(links_list)-counter)))
            if needs_reprocessing:
                needs_reprocessing = False 
                error_url = "ERROR IN Run number: " + str(counter) + ", URL: " + link+ "\n"
                print(bcolors.FAIL + error_url + bcolors.ENDC)
                FileManager().write_in_log_txt(error_url)
                continue
            counter += 1
            break

if __name__ == '__main__':
    main()