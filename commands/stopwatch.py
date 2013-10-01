# Copyright (C) 2013 Fox Wilson, Peter Foley, Srijay Kasturi, Samuel Damashek and James Forcier
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import time
from datetime import timedelta
from helpers.command import Command


def create_sw(cursor):
    cursor.execute("INSERT INTO stopwatches(time) VALUES(?)", (time.time(),))
    return "Created new stopwatch. ID: %d" % cursor.lastrowid


def check_sw_valid(sw):
    if not sw:
        return "You need to pass a stopwatch ID to !stopwatch get"
    if not sw.isdigit():
        return "Invalid ID!"
    return "OK"


def get_elapsed(cursor, sw):
    ok = check_sw_valid(sw)
    if ok != "OK":
        return ok
    query_result = cursor.execute("SELECT elapsed,time,active FROM stopwatches WHERE id=?", (int(sw[0]),)).fetchone()
    if query_result is None:
        return "No stopwatch exists with that ID!"
    elapsed = query_result[0]
    etime = 0
    active = "Paused "
    if query_result[2] == 1:
        etime = time.time() - query_result[1]
        active = "Active "
    etime += float(elapsed)
    return active + str(timedelta(seconds=etime))


def stop_stopwatch(cursor, sw):
    ok = check_sw_valid(sw)
    if ok != "OK":
        return ok
    query_result = cursor.execute("SELECT elapsed,time,active FROM stopwatches WHERE id=?", (int(sw[0]),)).fetchone()
    if query_result is None:
        return "No stopwatch exists with that ID!"
    if query_result[2] != 1:
        return "That stopwatch is already disabled!"
    elapsed = query_result[0]
    etime = time.time() - query_result[1]
    etime += float(elapsed)
    cursor.execute("UPDATE stopwatches SET elapsed=?,active=0 WHERE id=?", (etime, int(sw[0])))
    return "Stopwatch stopped!"


def stopwatch_resume(cursor, sw):
    ok = check_sw_valid(sw)
    if ok != "OK":
        return ok
    query_result = cursor.execute("SELECT elapsed,time,active FROM stopwatches WHERE id=?", (int(sw[0]),)).fetchone()
    if query_result is None:
        return "No stopwatch exists with that ID!"
    if query_result[2] != 0:
        return "That stopwatch is not paused!"
    cursor.execute("UPDATE stopwatches SET active=1,time=? WHERE id=?", (time.time(), int(sw[0])))
    return "Stopwatch resumed!"


@Command(['stopwatch', 'sw'], ['db'])
def cmd(send, msg, args):
    """Start/stops/resume/get stopwatch
    Syntax: !stopwatch <start|stop|resume|get>
    """

    command = msg.split()[0]
    msg = msg.split()[1:]
    cursor = args['db']
    if command == "start":
        send(create_sw(cursor))
    elif command == "get":
        send(get_elapsed(cursor, msg))
    elif command == "stop":
        send(stop_stopwatch(cursor, msg))
    elif command == "resume":
        send(stopwatch_resume(cursor, msg))