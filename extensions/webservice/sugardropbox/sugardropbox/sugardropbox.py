# Copyright (c) 2014 Ignacio Rodriguez <ignacio@sugarlabs.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import json
from sugar3 import env
from gi.repository import GObject
from gi.repository import GConf
from gettext import gettext as _

DROPBOX_API = os.path.join(env.get_profile_path(), 'extensions', 'webservice')
sys.path.append(DROPBOX_API)

from dropbox import client, session
gconf_client = GConf.Client.get_default()

APP_KEY = 'ey24mzrpiyv5rzf'
APP_SECRET = 'd0kh09zn6hv58hg'
ACCESS_TYPE = 'app_folder'
TOKEN_KEY = "/desktop/sugar/collaboration/dropbox_token"


# Copied from grestful code
def asynchronous(method):
    """ Convenience wrapper for GObject.idle_add. """
    def _async(*args, **kwargs):
        GObject.idle_add(method, *args, **kwargs)
    return _async


class Upload(GObject.GObject):

    __gsignals__ = {
        'upload-finished': (GObject.SignalFlags.RUN_FIRST, None,
                            ([str])),
        'upload-error': (GObject.SignalFlags.RUN_FIRST, None,
                         ([str])),
    }

    def __init__(self):
        GObject.GObject.__init__(self)

    @asynchronous
    def upload(self, path, title, token):
        try:
            sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)
            keys = self._get_keys()
            sess.set_token(keys[0], keys[1])

            d_client = client.DropboxClient(sess)
            extension = os.path.splitext(path)[1]
            dropbox_path = "/" + title + extension
            d_client.put_file(dropbox_path, open(path))

            share_link = d_client.share(dropbox_path, short_url=True)
            self.emit('upload-finished', share_link['url'])
        except Exception as e:
            self.emit(
                'upload-error',
                _('Error (%s), please update your dropbox token in Control Panel.') %
                e)
            return False

    def _get_keys(self):
        data = gconf_client.get_string(TOKEN_KEY)
        try:
            keys = json.loads(data)
        except:
            keys = None

        return keys
