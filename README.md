# Loopia DNS Authenticator for Certbot

The Loopia DNS Authenticator plugin for Certbot automates the process of
completing a `dns-01` challenge by creating, and subsequently removing, TXT
records using the Loopia DNS API.


## Usage

The plugin is enabled by passing the `--dns-loopia` option to `certbot`.
For details, refer to [Certbot's documentation](https://certbot.eff.org/docs/using.html#dns-plugins).

Example:

```sh
certbot certonly -d example.com \
  --dns-loopia --dns-loopia-credentials ~/.secrets/certbot/loopia.ini
```

### Arguments

- `--dns-loopia-credentials`:
  Loopia API credentials INI file. (Required)

- `--dns-loopia-propagation-seconds`:
  The number of seconds to wait for DNS to propagate before asking the ACME
  server to verify the DNS record. (Default: 10)


### Credentials

Use of this plugin requires a configuration file containing Loopia API
credentials, obtained from the Loopia control panel. The path to this file can
be provided using the `--dns-loopia-credentials` command-line argument.

Example:

```ini
dns_loopia_username = bob@loopiaapi
dns_loopia_password = mCaof9jCfImg6yxA
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
