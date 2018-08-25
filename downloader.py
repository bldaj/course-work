import os
import gzip
import time
from datetime import datetime

import requests

import ts_db
from utils import unify_datetime
from settings import settings

ts_file = settings.get('files', {}).get('ts_file', 'timestamps.json')
cve_prefix = settings.get('files', {}).get('cve_prefix', 'CVE-')


def create_directory_structure():
    if not os.path.exists('CVEs'):
        os.mkdir('CVEs')

    if not os.path.exists('CVEs/Archives'):
        os.mkdir('CVEs/Archives')

    if not os.path.exists('CVEs/XMLs'):
        os.mkdir('CVEs/XMLs')


#         # reading archive
#         with gzip.open('CVEs/Archives/%s.gz' % name, 'rb') as f:
#             print('Reading archive: %s' % name + '.gz')
#             xml_content = f.read()
#
#         # saving archive content (xml doc)
#         with open('CVEs/XMLs/%s' % name, 'wb') as f:
#             print('Saving archive content: %s\n' % name)
#             f.write(xml_content)


def save_archive(name, content):
    with open('CVEs/Archives/%s.gz' % name, 'wb') as f:
        print('Saving archive: %s' % name + '.gz')
        f.write(content)


def create_meta_link(cve_file: str):
    meta_base_link = settings.get('links', {}).get(
        'meta_base_link',
        'https://nvd.nist.gov/feeds/xml/cve/trans/es/nvdcve-'
    )
    meta_ending_link = settings.get('links', {}).get('meta_ending_link', 'trans.meta')

    return meta_base_link + str(cve_file) + meta_ending_link


def get_meta_ts_from_nvd(cve_file: str):
    meta_ts = unify_datetime(datetime.now())

    splitted_content = requests.get(create_meta_link(cve_file)).text.split('\n')

    for content in splitted_content:
        if 'lastModifiedDate' in content:
            meta_ts = content.replace('lastModifiedDate:', '').replace('\r', '')
            return unify_datetime(meta_ts)

    return meta_ts


def is_updated_on_nvd(cve_file_id: str):
    meta_ts = get_meta_ts_from_nvd(cve_file_id)

    cve_file_id = cve_prefix + cve_file_id

    ts_from_db = ts_db.get_ts(cve_file_id=cve_file_id)

    if ts_from_db is None:
        ts_db.insert_ts(cve_file_id=cve_file_id, ts_value=meta_ts)
        return True
    else:
        if meta_ts > ts_from_db:
            return True
        else:
            return False


def download_archives():
    current_year = datetime.today().year

    xml_base_link = settings.get('links', {}).get('xml_base_link', 'https://nvd.nist.gov/feeds/xml/cve/2.0/nvdcve-2.0-')
    xml_ending_link = settings.get('links', {}).get('xml_ending_link', '.xml.gz')

    # download by year
    for year in range(2002, current_year + 1):
        cve_file_name = cve_prefix + str(year)

        if is_updated_on_nvd(cve_file_id=str(year)):
            print('Download {0} file'.format(cve_file_name))

            url = xml_base_link + str(year) + xml_ending_link

            save_archive(name=cve_file_name, content=requests.get(url).content)
        else:
            print("File {0} wasn't modified".format(cve_file_name))

    # download recent and modified files
    for name in ['recent', 'modified']:
        cve_file_name = cve_prefix + str(name)

        if is_updated_on_nvd(cve_file_id=name):
            print('Download {0} file'.format(cve_file_name))

            url = xml_base_link + str(name) + xml_ending_link

            save_archive(name=cve_file_name, content=requests.get(url).content)


def main():
    begin_time = time.time()

    create_directory_structure()
    download_archives()

    print('Summary time: {0}'.format(time.time() - begin_time))


if __name__ == '__main__':
    main()
