import json
import csv

with open('kickstart200.tsv', 'w', encoding='utf-8', newline='') as fp:
    writer = csv.writer(fp, delimiter='\t')
    writer.writerow(['id', 'name', 'blurb', 'category', 'goal', 'pledged','backers', 'fx_rate'])

for i in range(1, 200, 1):
    with open('outputfile_pg{}.json'.format(i), 'r', encoding='utf-8') as f:
        data = json.load(f)
    projs = data['projects']
    for item in projs:
        with open('kickstart200.tsv', 'a', encoding='utf-8', newline='') as fp:
            writer = csv.writer(fp, delimiter='\t')
            blurb = item['blurb'].replace('\n', ' ')
            blurb = blurb.replace('\r\n', ' ')
            blurb = blurb.replace('\r', ' ')
            name = item['name']
            goal = item['goal']
            fx_rate = item['static_usd_rate']
            print(blurb)
            writer.writerow([item['id'], name , blurb,
                             item['category']['name'],goal, item['usd_pledged'], item['backers_count'], ux_rate])
