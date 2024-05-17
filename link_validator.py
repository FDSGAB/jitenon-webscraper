import requests


try:
    page = requests.get('https://kanji.jitenon.jp/kanji/501.html')
    if page.status_code != 200:
        print("Warning")
except:
    input("Error found at:")