from lxml import etree
import json
import time


def create_tag_dict(root):
    tag_dict = {}

    tag_dict['entry'] = '{%s}entry' % root.nsmap[None]

    tag_dict['cpe-lang:fact-ref'] = '{%s}fact-ref' % root.nsmap['cpe-lang']

    tag_dict['cvss:score'] = '{%s}score' % root.nsmap['cvss']
    tag_dict['cvss:access-vector'] = '{%s}access-vector' % root.nsmap['cvss']
    tag_dict['cvss:access-complexity'] = '{%s}access-complexity' % root.nsmap['cvss']
    tag_dict['cvss:authentication'] = '{%s}authentication' % root.nsmap['cvss']
    tag_dict['cvss:confidentiality-impact'] = '{%s}confidentiality-impact' % root.nsmap['cvss']
    tag_dict['cvss:integrity-impact'] = '{%s}integrity-impact' % root.nsmap['cvss']
    tag_dict['cvss:availability-impact'] = '{%s}availability-impact' % root.nsmap['cvss']
    tag_dict['cvss:source'] = '{%s}source' % root.nsmap['cvss']
    tag_dict['cvss:generated-on-datetime'] = '{%s}generated-on-datetime' % root.nsmap['cvss']

    tag_dict['vuln:cwe'] = '{%s}cwe' % root.nsmap['vuln'] # id
    tag_dict['vuln:summary'] = '{%s}summary' % root.nsmap['vuln']

    return tag_dict


def create_json_doc(root, tag_dict):
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

    for entry in root.iter(tag_dict['entry']):
        data['cve-id'] = entry.get('id')

        for fact_ref in entry.iter(tag_dict['cpe-lang:fact-ref']):
            data['cpe-lang:fact-ref'] = fact_ref.get('name')

        for cvss_score in entry.iter(tag_dict['cvss:score']):
            data['cvss']['score'] = cvss_score.text

        for access_vector in entry.iter(tag_dict['cvss:access-vector']):
            data['cvss']['access-vector'] = access_vector.text

        for access_complexity in entry.iter(tag_dict['cvss:access-complexity']):
            data['cvss']['access-complexity'] = access_complexity.text

        for authentication in entry.iter(tag_dict['cvss:authentication']):
            data['cvss']['authentication'] = authentication.text

        for confidentiality_impact in entry.iter(tag_dict['cvss:confidentiality-impact']):
            data['cvss']['confidentiality-impact'] = confidentiality_impact.text

        for integrity_impact in entry.iter(tag_dict['cvss:integrity-impact']):
            data['cvss']['integrity-impact'] = integrity_impact.text

        for availability_impact in entry.iter(tag_dict['cvss:availability-impact']):
            data['cvss']['availability-impact'] = availability_impact.text

        for source in entry.iter(tag_dict['cvss:source']):
            data['cvss']['source'] = source.text

        for generated_on_datetime in entry.iter(tag_dict['cvss:generated-on-datetime']):
            data['cvss']['generated-on-datetime'] = generated_on_datetime.text

        for cwe_id in entry.iter(tag_dict['vuln:cwe']):
            data['cwe']['cwe-id'] = cwe_id.get('id')

        for summary in entry.iter(tag_dict['vuln:summary']):
            data['cwe']['summary'] = summary.text

        with open('nvd.json', 'a') as f:
            json.dump(data, f, indent=4, separators=(',', ': '))


begin_time = time.time()

root = etree.parse('xml').getroot()
tag_dict = create_tag_dict(root)

create_json_doc(root, tag_dict)

end_time = time.time()

print(end_time - begin_time)
