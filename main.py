from src.kanji_information_fetcher import KanjiInformationFetcher
from src.information_organizer import InformationOrganizer
from src.file_manager import FileManager
from src.setup import Setup
import datetime
import numpy as np
from src.style.bcolors import bcolors
from src.entry_controller import EntryController

def main():
    start_time = datetime.datetime.now()
    print(bcolors.OKCYAN + "START TIME: " +  str(start_time) + bcolors.ENDC)
    setup = Setup()
    time_list = list()
    counter = setup.counter
    links_list = setup.links_list
    for link in links_list:
        needs_reprocessing = False
        while True:
            run_start = datetime.datetime.now()
            if setup.counter%10 == 0:
                print(bcolors.OKGREEN + "Custom run: " + str(setup.counter-counter+1) + "/" + str(len(setup.links_list)-counter+1) + " " + str(round(100*setup.counter/(len(setup.links_list)-counter), 2)) + "%, URL: " + link + bcolors.ENDC)
                print(bcolors.OKGREEN + "Until Completion: " + str(setup.counter) + "/" + str(len(setup.full_links_list)) + " " + str(round(100*setup.counter/len(setup.full_links_list), 2)) + "%, URL: " + link + bcolors.ENDC)
            info_list = KanjiInformationFetcher(url = link).fetch_result()
            data = InformationOrganizer(information_list = info_list)
            if data.kanji == '': continue
            Controller = EntryController(data)
            needs_reprocessing = Controller.write_all_infos()
            time_list.append(datetime.datetime.now() - run_start)
            if setup.counter%10 == 0:
                print("Estimated time for conclusion: ", str(np.mean(time_list)*(len(links_list)-setup.counter)))
            if needs_reprocessing:
                needs_reprocessing = False 
                error_url = "ERROR IN Run number: " + str(setup.counter) + ", URL: " + link+ "\n"
                print(bcolors.FAIL + error_url + bcolors.ENDC)
                FileManager().write_in_log_txt(error_url)
                continue
            setup.counter += 1
            break
    setup.save_counter_state(setup.counter)
    end_time = datetime.datetime.now()
    print(bcolors.OKCYAN + "END TIME: " + str(end_time) + bcolors.ENDC)
    print(bcolors.OKGREEN + "TOTAL TIME: ", str(end_time-start_time) + bcolors.ENDC)

if __name__ == '__main__':
    main()