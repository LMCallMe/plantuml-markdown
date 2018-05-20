#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : download-deps.py
# Author            : lmcallme <l.m.zhongguo@gmial.com>
# Date              : 18.05.2018
# Last Modified Date: 18.05.2018
# Last Modified By  : lmcallme <l.m.zhongguo@gmial.com>

"""****************************************************************************
Download 3rd part, and export to external dir
****************************************************************************"""

from __future__ import print_function

import os
#import zipfile
#import shutil
import sys
import traceback
#import distutils
#import fileinput
#import json

from optparse import OptionParser
#from time import time
#from sys import stdout
#from distutils.errors import DistutilsError
#from distutils.dir_util import copy_tree, remove_tree


def download_file(url, path, desc, size=None):
    from tqdm import tqdm
    import requests

    response = requests.get(url, stream=True)

    with open(path, "wb") as handle:
        size = size/1024 if size else size
        for data in tqdm(response.iter_content(1024), desc=desc, unit="KB", total=size):
            handle.write(data)


def install_files():
    pass


def main():
    workpath = os.path.dirname(os.path.realpath(__file__))
    #external_path = os.path.join(workpath, "external")
    external_path = os.path.join(workpath, "tmp")

    if not os.path.exists(external_path):
        os.makedirs(external_path)

    parser = OptionParser()
    parser.add_option('-r', '--remove-download',
                      action="store", type="string", dest='remove_downloaded', default=None,
                      help="Whether to remove downloaded zip file, 'yes' or 'no'")

    parser.add_option("-f", "--force-update",
                      action="store_true", dest="force_update", default=False,
                      help="Whether to force update the third party libraries")

    parser.add_option("-d", "--download-only",
                      action="store_true", dest="download_only", default=False,
                      help="Only download zip file of the third party libraries, will not extract it")

    (opts, args) = parser.parse_args()

    print("=======================================================")

    download_list = [
        {
            "name": "plantuml",
            "url": "https://codeload.github.com/plantuml/plantuml/zip/v1.2018.5",
            "file_name": "plantuml.zip",
            "size": 7634010
        },
    ]
    for elem in download_list:
        path = os.path.join(external_path, elem['file_name'])
        if os.path.exists(path):
            info = os.stat(path)
            if info.st_size == elem['size']:
                continue
        print("Download " + elem['file_name'])
        download_file(elem['url'], path, elem['name'], elem['size'])


# -------------- main --------------
if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
