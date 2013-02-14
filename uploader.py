#!/usr/bin/python

import logging
import os
import glob
import json

from dropbox import client, rest, session

from wsgi import settings

LOCK_FILE="/tmp/uploader.lock"

def upload_file(file_name,key,secret):
    sess = session.DropboxSession(settings.DROPBOX_KEY, settings.DROPBOX_SECRET, settings.DROPBOX_ACCESS_TYPE)
    sess.set_token(key, secret)

    myclient = client.DropboxClient(sess)

    bigFile = open(file_name, 'rb')
    logging.info("Start upload file: %s" % file_name)
    size=os.path.getsize(file_name)
    uploader = myclient.get_chunked_uploader(bigFile, size)
    while uploader.offset < size:
       try:
            upload = uploader.upload_chunked()
       except rest.ErrorResponse, e:
            # perform error handling and retry logic
            logging.error("Error upload file: %d %s" % (e.errno, e.strerror))
            pass
    uploader.finish(os.path.basename(file_name))
    logging.info("Finish upload file: %s" % file_name)
    bigFile.close()

def json_from_file(file_name):
    file_content = open(file_name, 'r').read()
    return json.loads(file_content)

def get_filename_from_downloaded_json(json):
    file_name = os.path.join(settings.DOWNLOAD_DIR, '%s.%s' % (json.get("id"), json.get("ext")))
    return (json.get("id"),file_name)

def check_file_downloaded(file_name_tuple):
    return os.path.exists(file_name_tuple[1])

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s\t%(levelname)s\t%(message)s', level=logging.DEBUG, filename='/tmp/uploader.log')
    if not os.path.exists(LOCK_FILE):
        logging.info("Start upload")
        try:
            f = open(LOCK_FILE, "w")
        except IOError,e:
            logging.error("Failed create lock file")
            return
        # jobs_files = glob.glob(os.path.join(settings.JOB_DIR, '*.job'))
        json_files = glob.glob(os.path.join(settings.DOWNLOAD_DIR, '*.json'))
        filenames = [ get_filename_from_downloaded_json(json_from_file(file)) for file in json_files]
        downloded_files = filter(check_file_downloaded,filenames)
        logging.info("Found %d file for upload" % len(downloded_files))
        for file in downloded_files:
            jobs_files = glob.glob(os.path.join(settings.JOB_DIR, '*_%s.job' % file[0]))
            logging.info("Upload `%s` for %d jobs" %(file[0],len(jobs_files)))
            for job_file in jobs_files:
                job = json_from_file(job_file)
                upload_file(file[1],job.get("access_token_key"),job.get("access_token_secret"))
                os.remove(job_file)
                logging.info("Remove job file: %s" % job_file)
            os.remove(file[1])
            logging.info("Remove video file: %s" % file[1])
            os.remove(file[1]+".info.json")
            logging.info("Remove video meta file: %s" % file[1]+".info.json")
        os.remove(LOCK_FILE)
        logging.info("End upload")