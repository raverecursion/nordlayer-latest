#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import re
import hashlib
import subprocess
import os

def get_latest_version():
    url = 'https://help.nordlayer.com/docs/linux'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
                      'AppleWebKit/537.36 (KHTML, like Gecko) ' +
                      'Chrome/58.0.3029.110 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Ensure we notice bad responses
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table of contents or the first header containing the version
    toc = soup.find('nav', {'aria-label': 'Table of contents'})
    if toc:
        # Extract the first link text from the table of contents
        first_link = toc.find('a')
        if first_link:
            text = first_link.get_text(strip=True)
            match = re.search(r'Linux\s+(\d+\.\d+\.\d+)', text)
            if match:
                return match.group(1)
    else:
        # Fallback to find headers in the content
        headers = soup.find_all(['h1', 'h2'])
        for header in headers:
            text = header.get_text(strip=True)
            match = re.search(r'Linux\s+(\d+\.\d+\.\d+)', text)
            if match:
                return match.group(1)
    return None

def update_pkgbuild(version):
    # Update the PKGBUILD file
    with open('PKGBUILD', 'r') as f:
        pkgbuild = f.read()

    pkgbuild = re.sub(r'^pkgver=.*$', f'pkgver={version}', pkgbuild, flags=re.MULTILINE)
    pkgbuild = re.sub(r'^pkgrel=.*$', 'pkgrel=1', pkgbuild, flags=re.MULTILINE)
    pkgbuild = re.sub(
        r'^source=\(".*"\)$',
        f'source=("https://downloads.nordlayer.com/linux/latest/debian/pool/main/nordlayer_{version}_amd64.deb")',
        pkgbuild,
        flags=re.MULTILINE
    )
    pkgbuild = re.sub(r"^sha512sums=\('.*'\)$", "sha512sums=('SKIP')", pkgbuild, flags=re.MULTILINE)

    with open('PKGBUILD', 'w') as f:
        f.write(pkgbuild)

    print('PKGBUILD updated with the latest version.')

def download_deb(version):
    # Download the .deb file
    url = f"https://downloads.nordlayer.com/linux/latest/debian/pool/main/nordlayer_{version}_amd64.deb"
    filename = f"nordlayer_{version}_amd64.deb"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
                      'AppleWebKit/537.36 (KHTML, like Gecko) ' +
                      'Chrome/58.0.3029.110 Safari/537.36'
    }
    response = requests.get(url, headers=headers, stream=True)
    response.raise_for_status()
    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"Downloaded {filename}")
    return filename

def calculate_checksum(filename):
    sha512 = hashlib.sha512()
    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha512.update(chunk)
    return sha512.hexdigest()

def update_checksum(checksum):
    # Update the checksum in the PKGBUILD
    with open('PKGBUILD', 'r') as f:
        pkgbuild = f.read()

    pkgbuild = re.sub(r"^sha512sums=\('.*'\)$", f"sha512sums=('{checksum}')", pkgbuild, flags=re.MULTILINE)

    with open('PKGBUILD', 'w') as f:
        f.write(pkgbuild)

    print('Checksum updated in PKGBUILD.')

def update_srcinfo():
    # Regenerate .SRCINFO
    subprocess.run(['makepkg', '--printsrcinfo'], stdout=open('.SRCINFO', 'w'))
    print('.SRCINFO updated.')

def clean_up(filename):
    if os.path.exists(filename):
        os.remove(filename)
        print(f"Removed temporary file {filename}")

if __name__ == '__main__':
    latest_version = get_latest_version()
    if latest_version:
        print(f'Latest version: {latest_version}')
        update_pkgbuild(latest_version)
        deb_filename = download_deb(latest_version)
        checksum = calculate_checksum(deb_filename)
        update_checksum(checksum)
        update_srcinfo()
        clean_up(deb_filename)
        print('All updates completed successfully.')
    else:
        print('Could not find the latest version. Please check the website or update the script.')
