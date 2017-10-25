import os
import requests
import gzip
import time


links_dict = {
    'CVE-Modified': 'https://static.nvd.nist.gov/feeds/xml/cve/2.0/nvdcve-2.0-modified.xml.gz',
    'CVE-Recent': 'https://static.nvd.nist.gov/feeds/xml/cve/2.0/nvdcve-2.0-recent.xml.gz',
    'CVE-2002': 'https://static.nvd.nist.gov/feeds/xml/cve/2.0/nvdcve-2.0-2002.xml.gz',
    'CVE-2003': 'https://static.nvd.nist.gov/feeds/xml/cve/2.0/nvdcve-2.0-2003.xml.gz',
    'CVE-2004': 'https://static.nvd.nist.gov/feeds/xml/cve/2.0/nvdcve-2.0-2004.xml.gz',
    'CVE-2005': 'https://static.nvd.nist.gov/feeds/xml/cve/2.0/nvdcve-2.0-2005.xml.gz',
    'CVE-2006': 'https://static.nvd.nist.gov/feeds/xml/cve/2.0/nvdcve-2.0-2006.xml.gz',
    'CVE-2007': 'https://static.nvd.nist.gov/feeds/xml/cve/2.0/nvdcve-2.0-2007.xml.gz',
    'CVE-2008': 'https://static.nvd.nist.gov/feeds/xml/cve/2.0/nvdcve-2.0-2008.xml.gz',
    'CVE-2009': 'https://static.nvd.nist.gov/feeds/xml/cve/2.0/nvdcve-2.0-2009.xml.gz',
    'CVE-2010': 'https://static.nvd.nist.gov/feeds/xml/cve/2.0/nvdcve-2.0-2010.xml.gz',
    'CVE-2011': 'https://static.nvd.nist.gov/feeds/xml/cve/2.0/nvdcve-2.0-2011.xml.gz',
    'CVE-2012': 'https://static.nvd.nist.gov/feeds/xml/cve/2.0/nvdcve-2.0-2012.xml.gz',
    'CVE-2013': 'https://static.nvd.nist.gov/feeds/xml/cve/2.0/nvdcve-2.0-2013.xml.gz',
    'CVE-2014': 'https://static.nvd.nist.gov/feeds/xml/cve/2.0/nvdcve-2.0-2014.xml.gz',
    'CVE-2015': 'https://static.nvd.nist.gov/feeds/xml/cve/2.0/nvdcve-2.0-2015.xml.gz',
    'CVE-2016': 'https://static.nvd.nist.gov/feeds/xml/cve/2.0/nvdcve-2.0-2016.xml.gz',
    'CVE-2017': 'https://static.nvd.nist.gov/feeds/xml/cve/2.0/nvdcve-2.0-2017.xml.gz'
}


def create_direcory_structure():
    if not os.path.exists('CVEs'):
        os.mkdir('CVEs')

    if not os.path.exists('CVEs/Archives'):
        os.mkdir('CVEs/Archives')

    if not os.path.exists('CVEs/XMLs'):
        os.mkdir('CVEs/XMLs')

    if not os.path.exists('CVEs/JSONs'):
        os.mkdir('CVEs/JSONs')


def download_xml_archive(links_dict):
    for name, url in links_dict.items():
        print('Request to: %s' % name)
        page = requests.get(url)

        # saving archive
        with open('CVEs/Archives/%s.gz' % name, 'wb') as f:
            print('Saving archive: %s' % name + '.gz')
            f.write(page.content)

        # reading archive
        with gzip.open('CVEs/Archives/%s.gz' % name, 'rb') as f:
            print('Reading archive: %s' % name + '.gz')
            xml_content = f.read()

        # saving archive content (xml doc)
        with open('CVEs/XMLs/%s' % name, 'wb') as f:
            print('Saving archive content: %s\n' % name)
            f.write(xml_content)


begin_time = time.time()

create_direcory_structure()
download_xml_archive(links_dict)

end_time = time.time()

print('Summary time: %s' % (end_time - begin_time))
