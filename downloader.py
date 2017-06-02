import requests
import gzip
import time


links_dict = {
    'CVE-Modified': 'https://static.nvd.nist.gov/feeds/xml/cve/nvdcve-2.0-Modified.xml.gz',
    'CVE-Recent': 'https://static.nvd.nist.gov/feeds/xml/cve/nvdcve-2.0-Recent.xml.gz',
    'CVE-2002': 'https://static.nvd.nist.gov/feeds/xml/cve/nvdcve-2.0-2002.xml.gz',
    'CVE-2003': 'https://static.nvd.nist.gov/feeds/xml/cve/nvdcve-2.0-2003.xml.gz',
    'CVE-2004': 'https://static.nvd.nist.gov/feeds/xml/cve/nvdcve-2.0-2004.xml.gz',
    'CVE-2005': 'https://static.nvd.nist.gov/feeds/xml/cve/nvdcve-2.0-2005.xml.gz',
    'CVE-2006': 'https://static.nvd.nist.gov/feeds/xml/cve/nvdcve-2.0-2006.xml.gz',
    'CVE-2007': 'https://static.nvd.nist.gov/feeds/xml/cve/nvdcve-2.0-2007.xml.gz',
    'CVE-2008': 'https://static.nvd.nist.gov/feeds/xml/cve/nvdcve-2.0-2008.xml.gz',
    'CVE-2009': 'https://static.nvd.nist.gov/feeds/xml/cve/nvdcve-2.0-2009.xml.gz',
    'CVE-2010': 'https://static.nvd.nist.gov/feeds/xml/cve/nvdcve-2.0-2010.xml.gz',
    'CVE-2011': 'https://static.nvd.nist.gov/feeds/xml/cve/nvdcve-2.0-2011.xml.gz',
    'CVE-2012': 'https://static.nvd.nist.gov/feeds/xml/cve/nvdcve-2.0-2012.xml.gz',
    'CVE-2013': 'https://static.nvd.nist.gov/feeds/xml/cve/nvdcve-2.0-2013.xml.gz',
    'CVE-2014': 'https://static.nvd.nist.gov/feeds/xml/cve/nvdcve-2.0-2014.xml.gz',
    'CVE-2015': 'https://static.nvd.nist.gov/feeds/xml/cve/nvdcve-2.0-2015.xml.gz',
    'CVE-2016': 'https://static.nvd.nist.gov/feeds/xml/cve/nvdcve-2.0-2016.xml.gz',
    'CVE-2017': 'https://static.nvd.nist.gov/feeds/xml/cve/nvdcve-2.0-2017.xml.gz'
}


def download_xml_archive(links_dict):
    for name, url in links_dict.items():
        page = requests.get(url)

        # saving archive
        with open('CVEs/Archives/%s.gz' % name, 'wb') as f:
            f.write(page.content)

        # reading archive
        with gzip.open('CVEs/Archives/%s.gz' % name, 'rb') as f:
            xml_content = f.read()

        # saving archive content (xml doc)
        with open('CVEs/XMLs/%s' % name, 'wb') as f:
            f.write(xml_content)


begin_time = time.time()

download_xml_archive(links_dict)

end_time = time.time()

print(end_time - begin_time)
