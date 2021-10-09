#! /usr/bin/env python
"""
Set up DNS records for mailserver.

Usage:

    ./mail-setup-dns.py [ACTION...]

Possible actions are:

    create-mx-record
    create-spf-record
    create-dkim-record          depends on: "./mail-setup.sh config dkim"
    create-dmarc-record
    list-records

See https://docker-mailserver.github.io/docker-mailserver/edge/config/best-practices/dkim/
for more information.
"""

import re
import sys
from configparser import ConfigParser
from lexicon.cli import logger, generate_list_table_result
from lexicon.config import ConfigResolver
from lexicon.providers import netcup

DOMAINS = ('coldfix.de', 'coldfix.eu', 'fireflake.de', 'fireflake.eu')
CREDENTIALS_FILE = 'var/letsencrypt/netcup_credentials.ini'


def read_ini(filename, section='top'):
    with open(filename) as f:
        config = ConfigParser()
        config.read_string('[top]\n' + f.read())
        return config[section]


def parse_dkim_record(lines):
    content = ''.join([
        re.search(r'"(.*)"', line).group(1)
        for line in lines
    ])
    return ('TXT', 'mail._domainkey', content)



def dns_client(domain, credentials):
    return netcup.Provider(ConfigResolver().with_dict({
        'domain': domain,
        'provider_name': 'netcup',
        'netcup': {
            'auth_customer_id':   credentials['dns_netcup_customer_id'],
            'auth_api_key':       credentials['dns_netcup_api_key'],
            'auth_api_password':  credentials['dns_netcup_api_password'],
        }
    }))


def main(actions):
    credentials = read_ini(CREDENTIALS_FILE)
    for domain in DOMAINS:
        print("Domain:", domain)
        provider = dns_client(domain, credentials)
        provider.authenticate()

        for action in actions:
            if action == 'create-mx-record':
                provider.create_record('MX', '@', '@')

            elif action == 'create-spf-record':
                provider.create_record('TXT', '@', 'v=spf1 mx ~all')

            elif action == 'create-dkim-record':
                with open(f'var/mail/conf/opendkim/keys/{domain}/mail.txt') as f:
                    rtype, name, content = parse_dkim_record(f)

                print("Creating DKIM record:", name, rtype, repr(content))
                provider.create_record(rtype, name, content)

            elif action == 'create-dmarc-record':
                rtype = 'TXT'
                name = '_dmarc'
                content = \
                    f'v=DMARC1; p=none; rua=mailto:dmarc.report@{domain}; ' \
                    f'ruf=mailto:dmarc.report@{domain}; sp=none; ri=86400'

                print("Creating DMARC record:", name, rtype, repr(content))
                provider.create_record(rtype, name, content)

            elif action == 'list-records':
                records = provider.list_records()
                output = generate_list_table_result(logger, records)
                print(output)

            else:
                print(f"Unknown action: {action!r}")
        print()


if __name__ == '__main__':
    main(sys.argv[1:])
