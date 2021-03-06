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

import time


class Report(object):

    USER = 0
    TIMES = 1
    TRAFFIC = 2
    DEVICE = 3

    @staticmethod
    def parse(data):
        ''' convert from transport format to SQL format '''
        now = int(time.time())
        times = []
        traffic = []
        devices = []

        user = data[Report.USER]
        entries = data[Report.TIMES]
        for package in entries.keys():
            for entry in entries[package]:
                times.append([user] + [package] + entry + [now])

        for entry in data[Report.TRAFFIC]:
            traffic.append([user] + entry + [now])

        if data[Report.DEVICE]:
            devices.append([user] + data[Report.DEVICE] + [now])

        return times, traffic, devices
