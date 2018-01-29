import requests
import time

def request_scrape(url):
    for i in range(50, 201, 1):
        page = url + "&page={}".format(i)
        headers = {'Accept': 'application/json'}
        print(page)
        res = requests.get(page, headers=headers)
        if res.status_code != 200:
            continue
        with open('outputfile_pg{}.json'.format(i), 'w', encoding='utf-8') as outfile:
            outfile.write(res.text)
        time.sleep(3)
            
request_scrape('https://www.kickstarter.com/discover/advanced?state=successful&woe_id=0&raised=2&sort=most_funded&seed=2528569')
