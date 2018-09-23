#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""

    ~~~~~~~~~~~~~~~~~~


    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""
import time

import requests
import oss2
from qiniu import BucketManager, Auth

import settings


def get_file_from_qiniu():
    print("[*] Try to get file from qiniu bucket...")
    qiniu_bucket = BucketManager(auth=Auth(settings.QINIU_ACCESS_KEY, settings.QINIU_SECRET_KEY))
    ret, eof, info = qiniu_bucket.list(settings.QINIU_BUCKET_NAME)

    items = ret.get("items")
    if not items:
        print(ret)
        exit(1)

    # print(items)
    print("[*] Get file success, count: {}".format(len(items)))
    return items


def upload_file_to_oss(items):
    auth = oss2.Auth(settings.ALIYUN_ACCESS_KEY, settings.ALIYUN_SECRET_KEY)
    bucket = oss2.Bucket(auth, settings.ALIYUN_ENDPOINT, settings.ALIYUN_BUCKET_NAME)

    for item in items:
        filename = item.get("key")
        target_url = "{}{}".format(settings.QINIU_DOMAIN, filename)
        print("[*] Try to get file information from {}".format(target_url))
        resp = requests.get(target_url, timeout=30)
        if resp.status_code != 200:
            print("[x] Error while request {}".format(target_url))
            time.sleep(10)
            continue

        content = resp.content
        result = bucket.put_object(filename, content)
        print("[*] upload result: {}".format(result.status))
        time.sleep(10)


def main():
    files = get_file_from_qiniu()
    upload_file_to_oss(files)


if __name__ == '__main__':
    main()
