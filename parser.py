import requests
from lxml import html

page = requests.get("https://web.nvd.nist.gov/view/vuln/search-results?query=&search_type=all&cves=on")
doc = html.fromstring(page.content)

links = []
info = []


def get_cve_links(doc, links):
    hrefs = doc.xpath('//dt/a')

    for href in hrefs:
        links.append(href.get("href"))

    return links


def get_cve_info(links, info):
    base_url = "https://web.nvd.nist.gov/view/vuln/"

    for link in links:
        url = base_url + link

        page = requests.get(url)
        doc = html.fromstring(page.content)

        overview = doc.xpath('//h4[text()="Overview"]/following-sibling::p/text()')
        info.append(overview)

    return info


links = get_cve_links(doc, links)
info = get_cve_info(links, info)
print(info)
