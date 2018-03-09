import subprocess
import socket

DOMAIN = "zfs"

def netcat(hostname, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hostname, port))
    s.shutdown(socket.SHUT_WR)
    while 1:
        data = s.recv(1024)
        if data == "":
            break
        return data
    s.close()

def setup(hass, config):
    output = netcat("192.168.1.8", 7777)

    properties = [
    "NAME",
    "SIZE",
    "ALLOC",
    "FREE",
    "EXPANDSZ",
    "FRAG",
    "CAP",
    "DEDUP",
    "HEALTH",
    "ALTROOT"
    ]

    for line in output.splitlines():
        zfs_values = line.decode("utf-8").split("\t")
        name = zfs_values[0]
        for i in range(0,len(properties)):
            hass.states.set("zfs."+name+"_"+properties[i], zfs_values[i])

    return True