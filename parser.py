import requests
from lxml import html

page = requests.get("https://web.nvd.nist.gov/view/vuln/search-results?query=&search_type=all&cves=on")
tree = html.fromstring(page.content)

hrefs = tree.xpath('//dt/a')

for href in hrefs:
    print(href.get("href"))
