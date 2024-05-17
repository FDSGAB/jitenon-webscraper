from src.kanji_information_fetcher import KanjiInformationFetcher


class InformationOrganizer():

    kanji = str()
    name_readings_list = list()
    meanings_list = list()
    readings_list = list()
    variant_forms_list =list()
    bunrui_list = list()
    shubetsu_list = list()
    kanjikousei_list = list()
    kanji_dictionary_number_list = list()
    kanji_code_list = list()
    kanji_bushu_list = list()

    def __init__(self, information_list : list) -> None:
        self.information_list= information_list
        self.kanji = str()
        self.kanji_code_list = list()
        self.kanji_dictionary_number_list = list()
        self.kanjikousei_list = list()
        self.kanji_bushu_list = list()
        self.name_readings_list = list()
        self.meanings_list = list()
        self.readings_list = list()
        self.variant_forms_list =list()
        self.bunrui_list = list()
        self.shubetsu_list = list()
        self.general_information_list = [
                                            'NULL', #'漢字',                                                                
                                            'NULL', #'画数',                                
                                            'NULL', #'成り立ち',                             
                                            'NULL', #'学年',                                 
                                            'NULL', #'漢字検定', 
                                            'NULL', #'JIS水準', 
                                            'NULL', #'漢字について', 
                                            'NULL', #'補足'
                                            'NULL', #'URL'
                                        ]
        self.information_lists_builder()
    

    def information_lists_builder(self):
        for information in self.information_list:
            self.subject_switch(subject = information[0], content  = information[1])

    def subject_switch(self, subject : str, content : str):
        if subject == '漢字':
            self.kanji = content
            self.general_information_list[0] = content
        elif subject == '部首':
            self.kanji_bushu_list.append([self.kanji, content[:2], content[3:len(content)-1]])
        elif subject == '画数':
            self.general_information_list[1] = content
            """ self.kakusuu_parts_discriminator(content)
            self.general_information_list[3] = content[:self.opening_index]
            self.general_information_list[4] = content[self.opening_index+2:self.plus_index]
            self.general_information_list[5] = content[self.plus_index+1:self.closing_index] """
        elif subject == '成り立ち':
            self.general_information_list[2] = content
        elif subject == '学年':
            self.general_information_list[3] = content
        elif subject == '漢字検定':
            self.general_information_list[4] = content
        elif subject == 'JIS水準':
            self.general_information_list[5] = content
        elif subject == '漢字について':
            self.general_information_list[6] = "".join(content.split('\n'))[4:]
        elif subject in ['Unicode', 'JIS X 0213', 'Shift_JIS-2004', 'MJ文字図形名', '戸籍統一文字番号', '住基ネット統一文字コード']:
            extra_code_content = self.verify_extra_code_content(content)
            if self.start == -1:
                self.kanji_code_list.append([self.kanji, subject, content, extra_code_content])
            else:
                self.kanji_code_list.append([self.kanji, subject, content[:self.start], extra_code_content])
        elif subject in ['大漢和辞典', '日本語漢字辞典', '新大字典', '大字源', '大漢語林']:
            self.kanji_dictionary_number_list.append([self.kanji, subject, content])
        elif subject == '補足':
            if content == 'NULL':
                self.general_information_list[7] = content
            else:
                self.general_information_list[7] = content[3:]
        elif subject == 'URL':
            self.general_information_list[8] = content
        elif subject == '名乗り読み':
            self.name_readings_list.append([self.kanji, content])
        elif subject == '漢字構成':
            self.kanjikousei_list.append([self.kanji, content])
        elif subject == '意味':
            additional_content = self.find_additional_content(subject, content)
            self.meanings_list.append([self.kanji, content[self.additional_content_end+1:], additional_content[0]])
        elif subject in ['音読み', '訓読み']:
            content_list = self.reading_content_parser(subject, content)
            self.readings_list.append([self.kanji, subject[0],  content_list[0], content_list[1], content_list[2][0], content_list[2][1]])
        elif subject == '種別':
            content = content.split(' / ')
            for entry in content:
                self.shubetsu_list.append([self.kanji, entry])
        elif subject == '分類':
            content = content.split(' / ')
            for entry in content:
                self.bunrui_list.append([self.kanji, entry])
        elif subject == '異体字':
            content = list(content)
            for entry in content:
                self.variant_forms_list.append([self.kanji, entry])
        else: print("SUBJECT " + subject + " NOT ACCOUNTED FOR!!!!!!!!!!")


    def kakusuu_parts_discriminator(self, content : str):
        self.opening_index = -1
        self.closing_index = -1
        self.plus_index = -1
        for i in range(0,len(content),1):
            if content[i] == '（':
                self.opening_index = i
            if content[i] == '）':
                self.closing_index = i
            if content[i] == '＋':
                self.plus_index = i
    
    def reading_content_parser(self, subject: str, reading_content : str) -> list:
        additional_content = self.find_additional_content(subject, reading_content)
        reading = reading_content[self.additional_content_end+1:]
        if self.reading_has_okurigana(reading):
            okurigana = self.find_okurigana(reading)
            reading = reading[:self.okurigana_start]
        else:
            okurigana = 'NULL'
        return [reading, okurigana, additional_content]
    
    def additional_content_exists(self, content : str) -> bool:
        self.additional_content_start = -1
        self.additional_content_end = -1
        for i in range(0,len(content),1):
            if content[i] == '◦' and self.additional_content_start == -1:
                self.additional_content_start = i
                continue
            if content[i] == '◦' and self.additional_content_start != -1 and self.additional_content_end == -1:
                self.additional_content_end = i
                return True
        return False
    
    def find_additional_content(self,subject: str, content : str) -> tuple:
        if subject in ['音読み', '訓読み']:
            if self.additional_content_exists(content):
                additional_content = content[self.additional_content_start + 1: self.additional_content_end]
                if additional_content != '表外読み':  
                    return (additional_content, '表内読み')
                if additional_content == '表外読み':
                    return ('NULL', '表外読み')
            else: return ('NULL','NULL')
        if subject == '意味':
            if self.additional_content_exists(content):
                return (content[self.additional_content_start + 1: self.additional_content_end], 'NULL')
            else: return ('NULL','NULL')

    def reading_has_okurigana(self, content : str) -> bool:
        self.okurigana_start = -1
        self.okurigana_end = -1
        for i in range(0,len(content),1):
            if content[i] == '（' and self.okurigana_start == -1:
                self.okurigana_start = i
            if content[i] == '）' and self.okurigana_end == -1:
                self.okurigana_end = i
        if self.okurigana_end != -1 and self.okurigana_start != -1: return True
        return False
    
    def find_okurigana(self, reading : str) -> str:
        return reading[self.okurigana_start+1:self.okurigana_end]
    
    def verify_extra_code_content(self, content : str) -> str:
        self.start = -1
        self.end = -1
        for i in range(0,len(content),1):
            if content[i] == '（' and self.start == -1:
                self.start = i
            if content[i] == '）' and self.end == -1:
                self.end = i
        if self.end != -1 and self.start != -1: return content[self.start+1: self.end]
        return 'NULL'




if __name__ == '__main__':
    information_list = KanjiInformationFetcher(url = "https://kanji.jitenon.jp/kanji/001.html").fetch_result()
    InformationOrganizer(information_list)