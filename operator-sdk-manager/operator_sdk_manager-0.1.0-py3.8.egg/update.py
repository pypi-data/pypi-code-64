#!/usr/bin/env python
import requests
import json
import hashlib
import tarfile
import io
import os
import os.path
import lastversion

from operator_sdk_manager.util import make_logger


logger = make_logger()


def operator_sdk_update(directory: str = os.path.expanduser('~/.operator-sdk'),
                        path: str = os.path.expanduser('~/.local/bin')) -> str:
    """
    Update the operator-sdk binary
    """
    return lastversion.latest('operator-framework/operator-sdk')

    tarball_name = 'crc-linux-amd64.tar.xz'
    urls = {
        'sum': f'{mirror}/sha256sum.txt',
        'release_info': f'{mirror}/release-info.json',
        'crc': f'{mirror}/{tarball_name}'
    }

    sums = requests.get(urls['sum']).text
    crc_sum = [
        line.split(' ')[0] for line in sums.split('\n')
        if line.endswith(tarball_name)
    ][0]
    logger.debug(f'Identified release checksum {crc_sum}')

    version = json.loads(
        requests.get(urls['release_info']).text
    ).get('version').get('crcVersion')
    logger.debug(f'Identified release version {version}')

    dirs = {
        'untar': f'{directory}/crc-linux-{version}-amd64',
        'crc': f'{directory}/crc-linux-{version}-amd64/crc',
        'symlink': f'{path}/crc',
    }

    if os.path.isdir(dirs['untar']):
        logger.info(f'crc {version} is already downloaded')
    else:
        logger.info(f'Downloading and validating crc {version}')
        crc = requests.get(urls['crc']).content
        sha = hashlib.sha256()
        sha.update(crc)
        if sha.hexdigest() == crc_sum:
            logger.debug('Hashes match')
        else:
            logger.error("Hashes don't match")
            exit(1)

        logger.info(f'Extracting {tarball_name} to {directory}')
        if not os.path.isdir(directory):
            os.mkdir(directory)
        crc_file = io.BytesIO(crc)
        with tarfile.open(fileobj=crc_file) as tar:
            tar.extractall(path=directory)

    if not os.path.isdir(path):
        os.mkdir(path)
    if os.path.islink(dirs['symlink']):
        symlink_inode = os.stat(dirs['symlink']).st_ino
        crc_inode = os.stat(dirs['crc']).st_ino

        if symlink_inode == crc_inode:
            logger.debug(f'crc {version} is already symlinked into {path}')
        else:
            logger.debug(f'Updating crc symlink to {version} in {path}')
            os.remove(dirs['symlink'])
            os.symlink(dirs['crc'], dirs['symlink'])
    else:
        logger.debug(f'Adding crc symlink to {version} in {path}')
        os.symlink(dirs['crc'], dirs['symlink'])

    return version
