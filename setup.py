#!/usr/bin/env python

from setuptools import setup, find_packages

version = '1.0.0'

setup(
    name='certbot-dns-loopia',
    version=version,
    description='Loopia DNS Authenticator for Certbot',
    long_description=open('README.md').read(),
    url='https://www.github.com/rgson/certbot-dns-loopia',
    author='Robin Gustafsson',
    author_email='robin@rgson.se',
    packages=find_packages(),
    install_requires=open('requirements.txt').readlines(),
    entry_points={
        'certbot.plugins': [
            'dns-loopia = certbot_dns_loopia.dns_loopia:Authenticator',
        ],
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Plugins',
        'Intended Audience :: System Administrators',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python',
        'Topic :: Internet :: Name Service (DNS)',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Security',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Networking',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],
)
