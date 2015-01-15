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

import MySQLdb

from .errors import StoreError
from .report import Report


class DataStore(object):

    QUERY_TIMES = 'INSERT INTO times '\
                  '(uid, package, started, duration, stored) '\
                  'values (%s, %s, %s, %s, %s) '\
                  'ON DUPLICATE KEY UPDATE '\
                  'duration = VALUES(duration), '\
                  'stored = VALUES(stored)'

    QUERY_TRAFFIC = 'INSERT INTO traffic '\
                    '(uid, started, received, transmitted, stored) '\
                    'values (%s, %s, %s, %s, %s) '\
                    'ON DUPLICATE KEY UPDATE '\
                    'received = VALUES(received), '\
                    'transmitted = VALUES(transmitted), '\
                    'stored = VALUES(stored)'

    QUERY_DEVICES = 'INSERT INTO devices '\
                    '(uid, model, build, system, kernel, stored) '\
                    'values (%s, %s, %s, %s, %s, %s) '\
                    'ON DUPLICATE KEY UPDATE '\
                    'model = VALUES(model), '\
                    'build = VALUES(build), '\
                    'system = VALUES(system), '\
                    'kernel = VALUES(kernel), '\
                    'stored = VALUES(stored)'

    def __init__(self, host, port, username, password, database):
        self._connection = MySQLdb.connect(host=host,
                                           port=port,
                                           user=username,
                                           passwd=password,
                                           db=database)

    def store(self, data):
        times, traffic, devices = Report.parse(data)
        self._execute_write([(self.QUERY_TIMES, times),
                             (self.QUERY_TRAFFIC, traffic),
                             (self.QUERY_DEVICES, devices)])

    def _execute_write(self, queries):
        self._connection.ping(True)
        try:
            self._connection.begin()
            cursor = self._connection.cursor()
            for query, params in queries:
                cursor.executemany(query, params)
            self._connection.commit()
        except Exception as error:
            print error
            self._connection.rollback()
            raise StoreError(error)
        finally:
            cursor.close()

    def __del__(self):
        if hasattr(self, '_connection') and self._connection is not None:
            self._connection.close()
