#!/usr/bin/python

import os
import glob
import json
from subprocess import call

from wsgi import settings

LOCK_FILE="/tmp/downloader.lock"

def get_link_from_job(job_filename):
    f = open(job_filename, 'r')
    file_content = f.read()
    return json.loads(file_content).get("link")

if __name__ == '__main__':
    if not os.path.exists(LOCK_FILE):
        try:
            f = open(LOCK_FILE, "w")
        except IOError:
            pass
        files = glob.glob(os.path.join(settings.JOB_DIR, '*.job'))
        links = [get_link_from_job(file) for file in files]
        if not os.path.isdir(settings.DOWNLOAD_DIR):
            os.makedirs(settings.DOWNLOAD_DIR)
        path = "%s/%%(id)s.%%(ext)s" % settings.DOWNLOAD_DIR
        args=[os.path.join(os.environ['OPENSHIFT_REPO_DIR'],"youtube-dl.py"),"-qwc","--write-info-json","-o",path]
        args.extend(links)
        call(args)
        os.remove(LOCK_FILE)
