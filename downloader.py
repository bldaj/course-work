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


def save_xml(name, xml_content):
    with open('CVEs/XMLs/{0}'.format(name), 'wb') as f:
        print('Saving archive content: {0}\n'.format(name))
        f.write(xml_content)


def read_archive(name):
    with gzip.open('CVEs/Archives/{0}.gz'.format(name), 'rb') as f:
        print('Reading archive: {0}'.format(name + '.gz'))
        return f.read()


def save_archive(name, content):
    with open('CVEs/Archives/{0}.gz'.format(name), 'wb') as f:
        print('Saving archive: {0}'.format(name + '.gz'))
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


def download_and_unzip_cve_file(name: str):
    xml_base_link = settings.get('links', {}).get('xml_base_link', 'https://nvd.nist.gov/feeds/xml/cve/2.0/nvdcve-2.0-')
    xml_ending_link = settings.get('links', {}).get('xml_ending_link', '.xml.gz')

    cve_file_name = cve_prefix + name

    if is_updated_on_nvd(cve_file_id=name):
        print('Downloading {0} file'.format(cve_file_name))

        url = xml_base_link + name + xml_ending_link

        save_archive(name=cve_file_name, content=requests.get(url).content)
        save_xml(name=cve_file_name, xml_content=read_archive(name=cve_file_name))
    else:
        print("File {0} wasn't modified".format(cve_file_name))


def download_and_unzip_cve_files():
    current_year = datetime.today().year

    # download by year
    for year in range(2002, current_year + 1):
        download_and_unzip_cve_file(name=str(year))

    # download recent and modified files
    for name in ['recent', 'modified']:
        download_and_unzip_cve_file(name=name)


def main():
    begin_time = time.time()
    print('Downloader started')

    create_directory_structure()
    download_and_unzip_cve_files()

    print('Summary time: {0}'.format(time.time() - begin_time))


if __name__ == '__main__':
    main()
