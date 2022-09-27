from bs4 import BeautifulSoup
import os
import csv

if __name__ == '__main__':
    dirname = os.path.dirname(__file__)
    file = open(os.path.join(dirname, "usps.html"), "r")
    html_text = file.read()

    map = []
    soup = BeautifulSoup(html_text, "html.parser")
    row_span = 0
    standard_name = ""
    for idx, tr in enumerate(soup.select('#ep533076 > tr')):
        if idx == 0:
            continue
        if row_span == 0:
            row_span = int(tr.contents[0].attrs['rowspan']) if 'rowspan' in tr.contents[0].attrs else 1
            standard_name = tr.contents[0].contents[0].contents[0].contents[0]
            abbr = tr.contents[2].contents[0].contents[0].contents[0]
        else:
            abbr = tr.contents[0].contents[0].contents[0].contents[0]

        map.append({'Abbr': abbr, 'Full Name': standard_name})
        row_span -= 1
        if row_span == 0:
            standard_name = ""

    csv_columns = ['Abbr', 'Full Name']
    with open(os.path.join(dirname, "addr_mapping.csv"), 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in map:
            print (data)
            writer.writerow(data)
