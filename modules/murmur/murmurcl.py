#!/usr/bin/env python
# -*- coding: utf-8
#
#    murmurcl.py - A small ice+python => murmur demo script
#
#    Copyright (C) 2009 Stefan Hacker
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
#    this script was fixed by haru_arc (http://cheatcode.xrea.jp/)
#    Fixed issue:
#        work option 'cfgserver'
#        work option 'cfgplayer'
#
import Ice
from optparse import OptionParser

class IcedMurmur(object):
    """
    Provides several small wrapper functions to ease the use
    of the ice interface
    """
    def __init__(self,
                 slice = "Murmur.ice",
                 proxy = "Meta:tcp -h 127.0.0.1 -p 6502"):
        #Ice.loadSlice(slice)
        import Murmur
        ice = Ice.initialize()
        prx = ice.stringToProxy(proxy)
        self.murmur = Murmur.MetaPrx.checkedCast(prx)
        self.Murmur = Murmur

    def registerPlayer(self, server, name, password, email =""):
        pid = server.registerPlayer(name)
        player = server.getRegistration(pid)
        self.updatePlayer(server, player, name, password, email)
        return pid

    def updatePlayer(self, server, player,
                   name = None,
                   password = None,
                   email = None):
        if name: player.name = name
        if password: player.pw = password
        if email: player.email = email
        server.updateregistration(player)
        return player

    def createServer(self, port = None):
        server = self.murmur.newServer()
        if port:
            server.setConf('port', str(port))
        return server

    def getServer(self, port):
        baseport = int(self.murmur.getDefaultConf()['port'])
        for server in self.murmur.getAllServers():
            cport = server.getConf('port')
            if cport: cport = int(cport)
            else:
               cport = baseport + server.id() - 1
            if port == cport:
                return server
        return None

    def getPlayer(self, server, name):
        players = server.getRegisteredPlayers(name)
        for player in players:
            if player.name == name:
                return player
        return None


def cb_addplayer(options, args, murmur):
    """
    Add a player to a server
    usage: addplayer <name> <password> <email> to <server>
    """
    try:
        name, password, email, keyw, server = args[1:]
        if keyw.lower() != "to": raise ValueError
    except ValueError:
        print cb_addplayer.__doc__
        return False

    # Get the server
    s = murmur.getServer(int(server))
    pid = murmur.registerPlayer(s, name, password, email)
    print "New player '%s' created with player pid: %d" % (name, pid)
    return True

def cb_delplayer(options, args, murmur):
    """
    Delete a player from a server
    usage: delplayer <name> from <server>
    """
    try:
        name, keyw, server = args[1:]
        if keyw.lower() != "from": raise ValueError
    except ValueError:
        print cb_delplayer.__doc__
        return False

    # Get the player
    s = murmur.getServer(int(server))
    player = murmur.getPlayer(s, name)
    pid = player.playerid
    s.unregisterPlayer(pid)
    print "Player '%s' with the pid %d got deleted" % (name, pid)
    return True

def cb_addserver(options, args, murmur):
    """
    Add a new virtual server to the murmur instance
    usage: addserver [port]
    """
    if len(args) > 2:
        print cb_addserver.__doc__
        return False

    port = None
    if args[1:]:
        port = int(args[1])
        if murmur.getServer(port):
            print "Port %d is already used by another server" % port
            return False
    server = murmur.createServer(port)
    print "Created new server with sid %d" % server.id()

def cb_delserver(options, args, murmur):
    """
    Deletes a virtual server
    usage: delserver <port>
    """

    try:
        if len(args) != 2: raise ValueError
        port = int(args[1])
    except ValueError:
        print cb_delserver.__doc__
        return False

    s = murmur.getServer(port)
    sid = s.id()
    s.delete()
    print "Deleted server with sid %d on port %d" % (sid, port)

def cb_startserver(options, args, murmur):
    """
    Starts a virtual server
    usage: startserver <port>
        or startserver all
    """
    try:
        if len(args) != 2: raise ValueError
        if args[1] != "all":
            port = int(args[1])
    except ValueError:
        print cb_startserver.__doc__
        return False

    if args[1] == "all":
        for server in murmur.murmur.getAllServers():
            try:
                server.start()
                print "Started sid %d" % server.id()
            except murmur.Murmur.ServerBootedException:
                pass
        print "All servers are running now"
        return True

    s = murmur.getServer(port)
    if not s:
        print "No server configured for port %d" % port
        return False
    try:
        s.start()
        print "Started server %d" % s.sid()
    except murmur.Murmur.ServerBootedException:
        print "Server is already running"
    return True

def cb_stopserver(options, args, murmur):
    """
    Stops a virtual server
    usage: stopserver <port>
        or stopserver all
    """
    try:
        if len(args) != 2: raise ValueError
        if args[1] != "all":
            port = int(args[1])
    except ValueError:
        print cb_stopserver.__doc__
        return False

    if args[1] == "all":
        for server in murmur.murmur.getAllServers():
            try:
                server.stop()
                print "Stopped sid %d" % server.id()
            except murmur.Murmur.ServerBootedException:
                pass
        print "All servers are stopped now"
        return True

    s = murmur.getServer(port)
    if not s:
        print "No server configured for port %d" % port
        return False
    try:
        s.stop()
        print "Stopped server %d" % s.sid()
    except murmur.Murmur.ServerBootedException:
        print "Server is already stopped"
    return True

def cb_cfgserver(options, args, murmur):
    """
    Configures a server
    usage: cfgserver <key> <value> on <server>
    example: cfgserver port 12345
    """
    try:
        key, value, keyw, server = args[1:5]
        if keyw.lower() != "on": raise ValueError
    except ValueError:
        print cb_cfgserver.__doc__
        return False

    s = murmur.getServer(int(server))
    s.setConf(key, value)
    print "'%s' set to '%s' on server %d" % (key, value, int(server))
    return True

def cb_cfgplayer(options, args, murmur):
    """
    Configures a user
    usage: cfgplayer <name> to <newname> <newpassword> <newemail> on <server>
    """
    try:
        name, keyw, newname, newpassword, newemail, keyw2, server = args[1:8]
        if keyw.lower() != "to" or keyw2.lower() != "on": raise ValueError
    except ValueError:
        print cb_cfgplayer.__doc__
        return False

    s = murmur.getServer(int(server))
    p = murmur.getPlayer(s, name)
    murmur.updatePlayer(s, p, newname, newpassword, newemail)
    print "Player with pid %d now updated!" % (p.playerid)

def cb_listplayers(options, args, murmur):
    """
    List all players on a server
    usage: listplayers <server> [filter <filter>]
    """
    try:
        if len(args) == 2:
            server = args[1]
            filter = ''
        else:
            server, keyw, filter = args[1:]
            if keyw.lower() != "filter": raise ValueError
    except ValueError:
        print cb_listplayers.__doc__
        return False

    s = murmur.getServer(int(server))
    if not s:
        print "No server present on port %s" % server
        return False
    print 50*"="
    print "Id\t\tName\t\tEmail"
    print 50*"="
    for p in s.getRegisteredPlayers(filter):
        print "%d\t\t%s\t\t%s" % (p.playerid,
                                  p.name,
                                  p.email)
    return True

def cb_listservers(options, args, murmur):
    """
    List all servers
    usage: listservers
    """
    baseport = int(murmur.murmur.getDefaultConf()['port'])
    print 50*"="
    print "Id\t\tPort\t\tRunning"
    print 50*"="
    for s in murmur.murmur.getAllServers():
        port = s.getConf('port')
        if not port: port = baseport + s.id() - 1
        else: port=int(port)
        print "%d\t\t%d\t\t%s" % (s.id(), port, s.isRunning())
    return True

def cb_addchannel(options, args, murmur):
    """
    Add a new channel on a server
    usage: addchannel <server> <name> <parent>
    """
    port = int(args[1])
    print(port)
    name = args[2]
    parent = int(args[3])
    server = murmur.getServer(port)
    server.addChannel(name, parent)


def display_help(args, commands):
    """
    Displays this help
    usage: help [command]
    """
    if args[1:]:
        if args[1].lower() in commands:
            print commands[args[1].lower()].__doc__
    else:
        print display_help.__doc__
        print
        print "Available commands: %s" % list(commands)

def dispatch(options, args):
    """
    Command dispatcher
    """

    commands = {'addplayer':cb_addplayer,
                'addserver':cb_addserver,
                'delplayer':cb_delplayer,
                'delserver':cb_delserver,
                'cfgserver':cb_cfgserver,
                'cfgplayer':cb_cfgplayer,
                'startserver':cb_startserver,
                'stopserver':cb_stopserver,
                'addchannel':cb_addchannel,
                'listplayers':cb_listplayers,
                'listservers':cb_listservers}

    if args[0].lower() == "help":
        display_help(args, commands)
        return True

    if not args[0].lower() in commands:
        # Command not found
        print "Unknown command: '%s'" % args[0]
        return False

    murmur = IcedMurmur(options.slice, options.iceprx)
    return commands[args[0].lower()](options, args, murmur)



if __name__ == "__main__":
    # Setup the commandline argument parser
    usage = "usage: %prog command [parameters...]"
    parser = OptionParser(usage=usage)
    parser.add_option("-i", "--iceprx",
                      dest = "iceprx",
                      default = "Meta:tcp -h 127.0.0.1 -p 6502")
    parser.add_option("-s", "--slice",
                      dest = "slice",
                      default = "Murmur.ice")
    (options, args) = parser.parse_args()

    if not args:
        # Hack for help
        dispatch(None, ["help"])
    else:
        dispatch(options, args)


