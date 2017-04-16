import requests
import gzip
from lxml import html


url = 'https://static.nvd.nist.gov/feeds/xml/cve/nvdcve-2.0-2002.xml.gz'
page = requests.get(url)
doc = html.fromstring(page.content)

# saving archive
with open('xml.gz', 'wb') as f:
    f.write(page.content)

# reading archive
with gzip.open('xml.gz', 'rb') as f:
    xml_content = f.read()

# saving archive content (xml doc)
with open('xml', 'wb') as f:
    f.write(xml_content)