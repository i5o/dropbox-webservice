"""
Obtengo la key publica y la privada.
"""
from dropbox import client, rest, session
APP_KEY = 'ey24mzrpiyv5rzf'
APP_SECRET = 'd0kh09zn6hv58hg'
ACCESS_TYPE = 'app_folder'

def get_keys():
    sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)
    request_token = sess.obtain_request_token()
    url = sess.build_authorize_url(request_token)
     
    # Make the user sign in and authorize this token
    print "url:", url
    print "Please visit this website and press the 'Allow' button, then hit 'Enter' here."
    raw_input()

    access_token = sess.obtain_access_token(request_token)
    key = access_token.key
    secret = access_token.secret   
    return key, secret
