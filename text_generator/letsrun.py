from bs4 import BeautifulSoup
import requests
from time import sleep
playFile = open('letsrun_1.txt', 'a')
for i in range(4):
    pg_num = i + 1
    req_url ="http://www.letsrun.com/forum/flat_read.php?thread=3549309&page=" + str(pg_num)
    sleep(20)
    res = requests.get(req_url)
    soup = BeautifulSoup(res.content, "html.parser")
    for links in soup.find_all('span', {'id': "intelliTXT"}):
        playFile.write(links.text)
        playFile.write(' ')
    

