# Copyright (c) 2014 Martin Abente Lahaye. - tch@sugarlabs.org
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA

import json
import logging

from tornado.web import RequestHandler

from .errors import StoreError
from .decorators import authorize


class ReportHandler(RequestHandler):

    def initialize(self, datastore, api_key):
        self._datastore = datastore
        self._api_key = api_key

    @authorize
    def post(self):
        try:
            self._datastore.store(json.loads(self.request.body))
            self.set_status(200)
        except ValueError:
            self.set_status(415)
        except StoreError:
            self.set_status(400)
        except Exception as error:
            logging.error(error)
            self.set_status(500)
        self.finish()
