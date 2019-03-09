"""DNS Authenticator for Loopia."""

import logging
import xmlrpc.client

import zope.interface

from certbot import errors
from certbot import interfaces
from certbot.plugins import dns_common


logger = logging.getLogger(__name__)


@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(dns_common.DNSAuthenticator):
    """DNS Authenticator for Loopia

    This Authenticator uses the Loopia API to fulfill a dns-01 challenge.
    """

    description = 'Obtain certs using a DNS TXT record (if you are using Loopia for DNS).'

    def __init__(self, *args, **kwargs):
        super(Authenticator, self).__init__(*args, **kwargs)
        self.credentials = None

    @classmethod
    def add_parser_arguments(cls, add):
        super(Authenticator, cls).add_parser_arguments(add)
        add('credentials', help='Loopia API credentials INI file.')

    def more_info(self):
        return 'This plugin configures a DNS TXT record to respond to a dns-01 challenge using the DigitalOcean API.'

    def _setup_credentials(self):
        self.credentials = self._configure_credentials(
            'credentials',
            'Loopia credentials INI file',
            {
                'username': 'API username for Loopia account',
                'password': 'API password for Loopia account',
            }
        )

    def _perform(self, domain, validation_name, validation):
        self._get_loopia_client().add_txt_record(domain, validation_name, validation)

    def _cleanup(self, domain, validation_name, validation):
        self._get_loopia_client().del_txt_record(domain, validation_name, validation)

    def _get_loopia_client(self):
        return _LoopiaClient(
            self.credentials.conf('username'),
            self.credentials.conf('password'))


class _LoopiaClient:
    """
    Encapsulates all communication with the Loopia API.
    """

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.client = xmlrpc.client.ServerProxy(
            'https://api.loopia.se/RPCSERV', encoding='utf-8')

    def add_zone_record(self, domain, subdomain, record):
        return self._call('addZoneRecord', domain, subdomain, record)

    def get_zone_records(self, domain, subdomain):
        return self._call('getZoneRecords', domain, subdomain)

    def remove_zone_record(self, domain, subdomain, record_id):
        return self._call('removeZoneRecord', domain, subdomain, record_id)

    def remove_subdomain(self, domain, subdomain):
        return self._call('removeSubdomain', domain, subdomain)

    def get_domains(self):
        return self._call('getDomains')

    def _call(self, method, *args):
        method = getattr(self.client, method)
        response = method(self.username, self.password, *args)
        self._check_for_error(response)
        return response

    @staticmethod
    def _check_for_error(response):
        if isinstance(response, list) and len(response) == 1:
            response = response[0]
        if isinstance(response, str) and response != 'OK':
            raise LoopiaError(response)

    def add_txt_record(self, domain_name, record_name, record_content):
        try:
            domain = self._find_domain(domain_name)
        except LoopiaError as e:
            msg = 'Error finding base domain: {}'.format(e)
            logger.debug(msg)
            raise errors.PluginError(msg)

        subdomain = self._calculate_subdomain(domain, record_name)
        record = self._build_txt_record(record_content)

        try:
            self.add_zone_record(domain, subdomain, record)
            logger.debug('Successfully added TXT record')
        except LoopiaError as e:
            msg = 'Error adding TXT record: {}'.format(e)
            logger.debug(msg)
            raise errors.PluginError(msg)

    def del_txt_record(self, domain_name, record_name, record_content):
        try:
            domain = self._find_domain(domain_name)
        except LoopiaError as e:
            logger.debug('Error finding base domain: %s', e)
            return

        subdomain = self._calculate_subdomain(domain, record_name)

        try:
            domain_records = self.get_zone_records(domain, subdomain)
        except LoopiaError as e:
            logger.debug('Error getting DNS records: %s', e)
            return

        for record in domain_records:
            if record['type'] != 'TXT' or record['rdata'] != record_content:
                continue
            try:
                record_id = record['record_id']
                logger.debug('Removing TXT record %s', record_id)
                self.remove_zone_record(domain, subdomain, record_id)
            except LoopiaError as e:
                logger.warning('Error deleting TXT record %s: %s', record_id, e)

        try:
            if not self.get_zone_records(domain, subdomain):
                self.remove_subdomain(domain, subdomain)
        except LoopiaError as e:
            logger.debug('Error cleaning up subdomain %s: %s', subdomain, e)

    def _find_domain(self, domain_name):
        domain_name_guesses = dns_common.base_domain_name_guesses(domain_name)
        domain_names = {domain['domain'] for domain in self.get_domains()}

        for guess in domain_name_guesses:
            if guess in domain_names:
                logger.debug('Found base domain for %s using name %s', domain_name, guess)
                return guess

        raise errors.PluginError('Unable to determine base domain for {} using names: {}.'
                                 .format(domain_name, domain_name_guesses))

    @staticmethod
    def _calculate_subdomain(base_domain, record_name):
        return record_name[:-len(base_domain)-1]

    @staticmethod
    def _build_txt_record(content):
        return {'type': 'TXT', 'ttl': 30, 'rdata': content, 'priority': 0}


class LoopiaError(Exception):
    pass
