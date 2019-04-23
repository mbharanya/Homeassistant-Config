from homeassistant.helpers.entity import Entity
import subprocess
import socket
import logging
from dataclasses import dataclass

_LOGGER = logging.getLogger(__name__)

volumes = [
    "zbackup",
    "zmain"
]

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

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Setup the sensor platform."""
    sensors = [ZfsSensor(volume, name)
                for volume in volumes
                    for name in properties]
    
    async_add_entities(sensors, True)
 

class ZfsSensor(Entity):
    """Representation of a Sensor."""

    def __init__(self, volume, name):
        """Initialize the sensor."""
        self._name = name
        self._volume = volume
        self._state = None
        self._api = ZfsApi("192.168.1.8", 7777)
        self._element = None
        self.update()

    @property
    def name(self):
        """Return the name of the sensor."""
        return "zfs_"+self._volume+"_"+self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._element.unit()

    def update(self):
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        elements = self._api.getAllElements()
        self._element = [element for element in elements[self._volume] if element.property() == self._name][0]
        self._state = self._element.value()

class ZfsApi:
    def __init__(self, hostname, port):
        """Initialize the data object."""
        self.hostname = hostname
        self.port = port

    def netcat(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.hostname, self.port))
        s.shutdown(socket.SHUT_WR)
        while 1:
            data = s.recv(1024)
            if data == "":
                break
            return data
        s.close()


    def getAllElements(self):
        output = self.netcat()

        elements = {}
        for line in output.splitlines():
            zfs_values = line.decode("utf-8").split("\t")
            volume_name = zfs_values[0]
            elements[volume_name] = []

            for i in range(0,len(properties)):
                elements[volume_name].append(ZfsElement(properties[i], zfs_values[i]))
                
        
        return elements

class ZfsElement:
    def __init__(self, property, value):
        self._property = property
        self._value = value

    def property(self):
        return self._property
    
    def value(self):
        return self._value.replace("%", "").replace("T", "").replace("x", "")
    
    def unit(self):
        if "%" in self._value:
            return "%"
        elif "T" in self._value:
            return "TB"
        elif "x" in self._value:
            return "x"
        else :
            return None