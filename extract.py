from bs4 import BeautifulSoup
from pprint import pprint


with open('index_old.html', 'r') as f:
    soup = BeautifulSoup(f, 'html.parser')

tables = soup.find_all('table')
print(len(tables))

data = []
for table in tables:
    print(table['class'][0])
    #pprint(table)
    cols = table.find('thead').findChildren()
    for c in cols:
        print(c.text)

    headers = [header.text for header in table.find_all("th")]
    results = [{headers[i]: cell for i, cell in enumerate(row.find_all("td"))}
               for row in table.find_all("tr")]
    data.append(results)

# with open('tables.html', 'w') as f:

pprint(data)