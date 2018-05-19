import time
from pymongo import MongoClient
from lxml import etree

client = MongoClient()
db = client.CVE

# client.drop_database('CVE')

xml_names = ['CVE-Modified', 'CVE-Recent',
             'CVE-2002', 'CVE-2003',
             'CVE-2004', 'CVE-2005',
             'CVE-2006', 'CVE-2007',
             'CVE-2008', 'CVE-2009',
             'CVE-2010', 'CVE-2011',
             'CVE-2012', 'CVE-2013',
             'CVE-2014', 'CVE-2015',
             'CVE-2016', 'CVE-2017',
             'CVE-2018']


def create_namespaces_dict(root):
    tag_dict = {'entry': '{%s}entry' % root.nsmap[None], 'cpe-lang:fact-ref': '{%s}fact-ref' % root.nsmap['cpe-lang'],
                'cvss:score': '{%s}score' % root.nsmap['cvss'],
                'cvss:access-vector': '{%s}access-vector' % root.nsmap['cvss'],
                'cvss:access-complexity': '{%s}access-complexity' % root.nsmap['cvss'],
                'cvss:authentication': '{%s}authentication' % root.nsmap['cvss'],
                'cvss:confidentiality-impact': '{%s}confidentiality-impact' % root.nsmap['cvss'],
                'cvss:integrity-impact': '{%s}integrity-impact' % root.nsmap['cvss'],
                'cvss:availability-impact': '{%s}availability-impact' % root.nsmap['cvss'],
                'cvss:source': '{%s}source' % root.nsmap['cvss'],
                'cvss:generated-on-datetime': '{%s}generated-on-datetime' % root.nsmap['cvss'],
                'vuln:cwe': '{%s}cwe' % root.nsmap['vuln'], 'vuln:summary': '{%s}summary' % root.nsmap['vuln']}

    return tag_dict


def prepare_data_for_xml_entry(entry, namespaces_dict):
    data = {'cve-id': None,
            'cpe-lang:fact-ref': None,
            'cvss':
                {
                    'score': None,
                    'access-vector': None,
                    'access-complexity': None,
                    'authentication': None,
                    'confidentiality-impact': None,
                    'integrity-impact': None,
                    'availability-impact': None,
                    'source': None,
                    'generated-on-datetime': None
                },
            'cwe':
                {
                    'cwe-id': None,
                    'summary': None
                }
            }

    data['cve-id'] = entry.get('id')

    for fact_ref in entry.iter(namespaces_dict['cpe-lang:fact-ref']):
        data['cpe-lang:fact-ref'] = fact_ref.get('name')

    for cvss_score in entry.iter(namespaces_dict['cvss:score']):
        data['cvss']['score'] = cvss_score.text

    for access_vector in entry.iter(namespaces_dict['cvss:access-vector']):
        data['cvss']['access-vector'] = access_vector.text

    for access_complexity in entry.iter(namespaces_dict['cvss:access-complexity']):
        data['cvss']['access-complexity'] = access_complexity.text

    for authentication in entry.iter(namespaces_dict['cvss:authentication']):
        data['cvss']['authentication'] = authentication.text

    for confidentiality_impact in entry.iter(namespaces_dict['cvss:confidentiality-impact']):
        data['cvss']['confidentiality-impact'] = confidentiality_impact.text

    for integrity_impact in entry.iter(namespaces_dict['cvss:integrity-impact']):
        data['cvss']['integrity-impact'] = integrity_impact.text

    for availability_impact in entry.iter(namespaces_dict['cvss:availability-impact']):
        data['cvss']['availability-impact'] = availability_impact.text

    for source in entry.iter(namespaces_dict['cvss:source']):
        data['cvss']['source'] = source.text

    for generated_on_datetime in entry.iter(namespaces_dict['cvss:generated-on-datetime']):
        data['cvss']['generated-on-datetime'] = generated_on_datetime.text

    for cwe_id in entry.iter(namespaces_dict['vuln:cwe']):
        data['cwe']['cwe-id'] = cwe_id.get('id')

    for summary in entry.iter(namespaces_dict['vuln:summary']):
        data['cwe']['summary'] = summary.text

    return data


def parse_xml_doc(name):
    root = etree.parse('CVEs/XMLs/%s' % name).getroot()
    namespaces_dict = create_namespaces_dict(root)
    collection = db['%s' % name]

    for entry in root.iter(namespaces_dict['entry']):
        data = prepare_data_for_xml_entry(entry, namespaces_dict)
        collection.insert_one(data)


def write_data_to_mongoDB():
    for xml_name in xml_names:
        print('Working on: %s' % xml_name)
        parse_xml_doc(xml_name)


if __name__ == '__main__':
    begin_time = time.time()

    write_data_to_mongoDB()

    print('Summary time: %s' % (time.time() - begin_time))
