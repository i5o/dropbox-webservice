# Copyright (C) 2014, Ignacio Rodriguez <ignacio@sugarlabs.org>
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

import json
import os
import logging
import sys
from gi.repository import GObject, GConf
from sugar3 import env

DROPBOX_API = os.path.join(env.get_profile_path(), 'extensions', 'webservice')
sys.path.append(DROPBOX_API)

from gi.repository import Gtk
from gi.repository import WebKit

from jarabe.webservice import accountsmanager
from cpsection.webaccount.web_service import WebService
from dropbox import session

APP_KEY = 'ey24mzrpiyv5rzf'
APP_SECRET = 'd0kh09zn6hv58hg'
ACCESS_TYPE = 'app_folder'
TOKEN_KEY = "/desktop/sugar/collaboration/dropbox_token"
SUBMIT_URL = "www.dropbox.com/1/oauth/authorize_submit"


class WebService(WebService):

    def __init__(self):
        self._account = accountsmanager.get_account('sugardropbox')
        self._url = None
        self._sess = None
        self._request_token = None

    def get_icon_name(self):
        return 'sugardropbox'

    def config_service_cb(self, widget, event, container):
        wkv = WebKit.WebView()
        url = self._get_auth_url()
        wkv.load_uri(url)
        logging.debug(url)
        wkv.grab_focus()
        wkv.connect('navigation-policy-decision-requested',
                    self._nav_policy_cb)

        for c in container.get_children():
            container.remove(c)

        scrolled = Gtk.ScrolledWindow()
        scrolled.add(wkv)

        container.add(scrolled)
        container.show_all()

    def _get_auth_url(self):
        self._sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)
        self._request_token = self._sess.obtain_request_token()
        self._url = self._sess.build_authorize_url(self._request_token)
        return self._url

    def _nav_policy_cb(self, view, frame, req, action, param):
        uri = req.get_uri()
        if uri is None:
            return

        if uri.endswith(SUBMIT_URL):
            # Wait 3 seconds
            def internal_cb():
                access_token = self._sess.obtain_access_token(
                    self._request_token)
                keys = [access_token.key, access_token.secret]
                data = json.dumps(keys)
                self._save_dropbox_token(data)
            GObject.timeout_add(3000, internal_cb)

    def _save_dropbox_token(self, access_token):
        client = GConf.Client.get_default()
        client.set_string(TOKEN_KEY, access_token)


def get_service():
    return WebService()
