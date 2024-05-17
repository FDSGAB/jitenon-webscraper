import requests
from bs4 import BeautifulSoup

visited_url_list = list()
to_visit_links = list()

homepage_url = "https://kanji.jitenon.jp"

to_visit_links.append(homepage_url)



while True:
    if len(to_visit_links) > 0:
        print(to_visit_links[0])
        while True:
            try: 
                web_page = requests.get(to_visit_links[0])
                break
            except: pass
        visited_url_list.append(to_visit_links[0])
        to_visit_links.remove(to_visit_links[0])
        soup = BeautifulSoup(web_page.content, "html.parser")
        links = soup.find_all('a')
        for link in links:
            try:
                if link['href'] not in visited_url_list and (link['href'][0:7] == 'http://' or link['href'][0:8] == 'https://'):
                    to_visit_links.append(link['href'])
            except: continue
    else:
        break


f = open("all_links.txt", "w")
f.write("\n".join(visited_url_list))
f.close()

print(len(visited_url_list))

