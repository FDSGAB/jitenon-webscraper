# jitenon-webscraper
 Web scraper of kanji information from https://kanji.jitenon.jp




 ### Logic Behind the kanji links:
 Scrapping all the site links and avaliating which ones are kanji pages would be extremely time and processing consuming. With that in mind, trying to look for a pattern in the url logic seemed like a better idea and it was.
 
 The logic behind is showed below:

 - The url contains a unique number that refers to a unique kanji just before the '.html' part.
 - The kanjis are separated in sets of 500 kanji at the start.
 - When a set ends, the letter after the word "kanji" in the url is changed to the next letter in alphabetical order and a new set of 500 starts.
 - The first letter would be 'a', however, it is absent from the url. From 'b' onwards, the letter is added.
 - When the letter 'y' is reached, the following kanji are not separeted in sets anymore and go until the most recent added.

The following draft tries to exemplify the logic:
 ```bash
https://kanji.jitenon.jp/kanji/001.html -> https://kanji.jitenon.jp/kanji/500.html 001 - 500 (would be letter 'a' after "kanji")
https://kanji.jitenon.jp/kanjib/501.html -> https://kanji.jitenon.jp/kanjib/1000.html 501 - 1000 (letter 'b' after "kanji")
https://kanji.jitenon.jp/kanjic/1001.html -> https://kanji.jitenon.jp/kanjic/1500.html 1001 - 1500 (letter 'c' after "kanji")
https://kanji.jitenon.jp/kanjid/1501.html -> https://kanji.jitenon.jp/kanjid/2000.html 1501 - 2000 (letter 'd' after "kanji")
. and
. so
. on
https://kanji.jitenon.jp/kanjiy/12001.html -> https://kanji.jitenon.jp/kanjib/XXXXX.html 12001 - XXXXX (letter 'y' after "kanji")
 ```
