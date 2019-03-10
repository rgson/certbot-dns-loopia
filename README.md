# Loopia DNS Authenticator for Certbot

The Loopia DNS Authenticator plugin for Certbot automates the process of
completing a `dns-01` challenge by creating, and subsequently removing, TXT
records using the Loopia DNS API.


## Usage

The plugin is enabled by passing the `--dns-loopia` option to `certbot`.
For details, refer to [Certbot's documentation](https://certbot.eff.org/docs/using.html#dns-plugins).

Examples:

```sh
# Obtaining a certificate for example.com
certbot certonly -d example.com \
  --certbot-dns-loopia:dns-loopia \
  --certbot-dns-loopia:dns-loopia-credentials ~/.secrets/certbot/loopia.ini
```

```sh
# Obtaining a wildcard certificate for example.com and setting it up for Apache
certbot -d example.com -d '*.example.com' \
  --server 'https://acme-v02.api.letsencrypt.org/directory' \
  -i apache -a certbot-dns-loopia:dns-loopia \
  --certbot-dns-loopia:dns-loopia-credentials ~/.secrets/certbot/loopia.ini
```

### Arguments

- `--certbot-dns-loopia:dns-loopia-credentials`:
  Loopia API credentials INI file. (Required)

- `--certbot-dns-loopia:dns-loopia-propagation-seconds`:
  The number of seconds to wait for DNS to propagate before asking the ACME
  server to verify the DNS record. (Default: 10)


### Credentials

Use of this plugin requires a configuration file containing Loopia API
credentials, obtained from the Loopia control panel. The path to this file can
be provided using the `--certbot-dns-loopia:dns-loopia-credentials` command-line
argument.

Example:

```ini
certbot_dns_loopia:dns_loopia_username = bob@loopiaapi
certbot_dns_loopia:dns_loopia_password = mCaof9jCfImg6yxA
```

The API credentials must have permission to perform the following API calls:
- `getDomains` to find the domain to which the record should be added.
- `addZoneRecord` to add the DNS verification record.
- `getZoneRecords` to find the added record.
- `removeZoneRecord` to remove the added record.
- `removeSubdomain` to remove any automatically created subdomains.


## Installation

The plugin can be installed using `setuptools`:

```sh
python setup.py install
```
