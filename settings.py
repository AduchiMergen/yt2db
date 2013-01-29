# Dropbox settings
DROPBOX_KEY = 'please, set proper value in settings_local.py'
DROPBOX_SECRET = 'please, set proper value in settings_local.py'
DROPBOX_ACCESS_TYPE = 'app_folder'
JOB_DIR = "./jobs"
DOWNLOAD_DIR = "./video"
# Default secret key for Flask session
SECRET_KEY = 'Wc\xfcM\xf6H\xdfN\xed\xc6\x9aJ\x05\xb1\xb5fF!\xa8\x94B\x86\xa0\x95'

try:
    from settings_local import *
except ImportError:
    pass
