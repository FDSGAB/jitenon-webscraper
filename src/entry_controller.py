from src.information_organizer import InformationOrganizer
from src.file_manager import FileManager

class EntryController():


    def __init__(self, data : InformationOrganizer) -> None: 
        self.data = data

    def write_kanji_general_info(self, data : InformationOrganizer) -> tuple:
        FileManager().write_entry('data/kanjigeneralinfo.csv', data.general_information_list)
        return FileManager().entry_was_successfull(data.kanji, 'data/kanjigeneralinfo.csv', 1)

    def write_kanji_info_list(self, kanji : str, file: str, data_list : list) -> tuple:
        for entry in data_list:
            FileManager().write_entry(file, entry)
        return FileManager().entry_was_successfull(kanji, file, len(data_list))

    def delete_previous_written_entries(self, controls_list : list):
        for control in controls_list:
            FileManager().delete_the_last_x_rows_of_file(control[0], control[1])

    def write_all_infos(self) -> bool:
        data = self.data
        self.controls_list = list()
        general_control = self.write_kanji_general_info(data)
        self.controls_list.append(['data/kanjigeneralinfo.csv', general_control[1]])
        if general_control[0] == 1:
            self.delete_previous_written_entries(self.controls_list)
            return True
        readings_control = self.write_kanji_info_list(data.kanji, 'data/kanjireadings.csv', data.readings_list)
        self.controls_list.append(['data/kanjireadings.csv', readings_control[1]])
        if readings_control[0] == 1:
            self.delete_previous_written_entries(self.controls_list)
            return True
        meanings_control = self.write_kanji_info_list(data.kanji, 'data/kanjimeanings.csv', data.meanings_list)
        self.controls_list.append(['data/kanjimeanings.csv', meanings_control[1]])
        if meanings_control[0] == 1:
            self.delete_previous_written_entries(self.controls_list)
            return True
        numeration_control = self.write_kanji_info_list(data.kanji, 'data/kanjidictionarynumbers.csv', data.kanji_dictionary_number_list)
        self.controls_list.append(['data/kanjidictionarynumbers.csv', numeration_control[1]])
        if numeration_control[0] == 1:
            self.delete_previous_written_entries(self.controls_list)
            return True
        code_control = self.write_kanji_info_list(data.kanji, 'data/kanjicodes.csv', data.kanji_code_list)
        self.controls_list.append(['data/kanjicodes.csv', code_control[1]])
        if code_control[0] == 1:
            self.delete_previous_written_entries(self.controls_list)
            return True
        bushu_control = self.write_kanji_info_list(data.kanji, 'data/kanjibushu.csv', data.kanji_bushu_list)
        self.controls_list.append(['data/kanjibushu.csv', bushu_control[1]])
        if bushu_control[0] == 1:
            self.delete_previous_written_entries(self.controls_list)
            return True
        variant_form_control = self.write_kanji_info_list(data.kanji, 'data/kanjivariant.csv', data.variant_forms_list)
        self.controls_list.append(['data/kanjivariant.csv', variant_form_control[1]])
        if variant_form_control[0] == 1:
            self.delete_previous_written_entries(self.controls_list)
            return True
        name_readings_control = self.write_kanji_info_list(data.kanji, 'data/kanjinamereadings.csv', data.name_readings_list)
        self.controls_list.append(['data/kanjinamereadings.csv', name_readings_control[1]])
        if name_readings_control[0] == 1:
            self.delete_previous_written_entries(self.controls_list)
            return True
        kousei_control = self.write_kanji_info_list(data.kanji, 'data/kanjikousei.csv', data.kanjikousei_list)
        self.controls_list.append(['data/kanjikousei.csv', kousei_control[1]])
        if kousei_control[0] == 1:
            self.delete_previous_written_entries(self.controls_list)
            return True
        bunrui_control = self.write_kanji_info_list(data.kanji, 'data/kanjibunrui.csv', data.bunrui_list)
        self.controls_list.append(['data/kanjibunrui.csv', bunrui_control[1]])
        if bunrui_control[0] == 1:
            self.delete_previous_written_entries(self.controls_list)
            return True
        shubetsu_control = self.write_kanji_info_list(data.kanji, 'data/kanjishubetsu.csv', data.shubetsu_list)
        self.controls_list.append(['data/kanjishubetsu.csv', shubetsu_control[1]])
        if shubetsu_control[0] == 1:
            self.delete_previous_written_entries(self.controls_list)
            return True
        name_control = self.write_kanji_info_list(data.kanji, 'data/namae.csv', data.names_list)
        self.controls_list.append(['data/namae.csv', name_control[1]])
        if name_control[0] == 1:
            self.delete_previous_written_entries(self.controls_list)
            return True
        last_name_control = self.write_kanji_info_list(data.kanji, 'data/myouji.csv', data.last_names_list)
        self.controls_list.append(['data/myouji.csv', last_name_control[1]])
        if last_name_control[0] == 1:
            self.delete_previous_written_entries(self.controls_list)
            return True
        contained_in_control = self.write_kanji_info_list(data.kanji, 'data/containedin.csv', data.contained_in_list)
        self.controls_list.append(['data/containedin.csv', contained_in_control[1]])
        if contained_in_control[0] == 1:
            self.delete_previous_written_entries(self.controls_list)
            return True
        addable_control = self.write_kanji_info_list(data.kanji, 'data/addableparts.csv', data.addable_parts_list)
        self.controls_list.append(['data/addableparts.csv', addable_control[1]])
        if addable_control[0] == 1:
            self.delete_previous_written_entries(self.controls_list)
            return True
        nandoku_control = self.write_kanji_info_list(data.kanji, 'data/nandoku.csv', data.nandoku_list)
        self.controls_list.append(['data/nandoku.csv', nandoku_control[1]])
        if nandoku_control[0] == 1:
            self.delete_previous_written_entries(self.controls_list)
            return True
        jouyou_control = self.write_kanji_info_list(data.kanji, 'data/jouyou.csv', data.jouyou_list)
        self.controls_list.append(['data/jouyou.csv', jouyou_control[1]])
        if jouyou_control[0] == 1:
            self.delete_previous_written_entries(self.controls_list)
            return True
        chimei_control = self.write_kanji_info_list(data.kanji, 'data/chimei.csv', data.chimei_list)
        self.controls_list.append(['data/chimei.csv', chimei_control[1]])
        if chimei_control[0] == 1:
            self.delete_previous_written_entries(self.controls_list)
            return True
        word_control = self.write_kanji_info_list(data.kanji, 'data/kotoba.csv', data.word_list)
        self.controls_list.append(['data/kotoba.csv', word_control[1]])
        if word_control[0] == 1:
            self.delete_previous_written_entries(self.controls_list)
            return True
        yoji_control = self.write_kanji_info_list(data.kanji, 'data/yoji.csv', data.yoji_list)
        self.controls_list.append(['data/yoji.csv', yoji_control[1]])
        if yoji_control[0] == 1:
            self.delete_previous_written_entries(self.controls_list)
            return True
        kotozawa_control = self.write_kanji_info_list(data.kanji, 'data/kotozawa.csv', data.kotozawa_list)
        self.controls_list.append(['data/kotozawa.csv', kotozawa_control[1]])
        if kotozawa_control[0] == 1:
            self.delete_previous_written_entries(self.controls_list)
            return True
        return False