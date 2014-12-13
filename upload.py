from dropbox import client, rest, session
from get_keys import get_keys
APP_KEY = 'ey24mzrpiyv5rzf'
APP_SECRET = 'd0kh09zn6hv58hg'
ACCESS_TYPE = 'app_folder'

sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)
keys = get_keys()
sess.set_token(keys[0], keys[1])
print keys[0], keys[1]

client = client.DropboxClient(sess)
file_name = "file.txt"
response = client.put_file("/" + file_name, open(file_name))
print "uploaded:", response
