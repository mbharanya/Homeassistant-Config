DOMAIN = 'led_color_temp'

import logging
import homeassistant.loader as loader
import homeassistant.components as core
import homeassistant.helpers.config_validation as cv
from homeassistant.components import device_tracker, light
from homeassistant.const import (ATTR_ENTITY_ID, SERVICE_TURN_OFF,
                                 SERVICE_TURN_ON, STATE_HOME, STATE_NOT_HOME,
                                 STATE_OFF, STATE_ON)
from homeassistant.core import split_entity_id
from homeassistant.helpers.event import (async_track_state_change,
                                         async_track_time_change)
import math
                                   
# Shortcut for the logger
_LOGGER = logging.getLogger(__name__)

MAX_HUE = 240
MIDDLE_TEMP = 20
SENSITIVITY = 2

TARGET_ID = "sensor.weather_now_temperature"

async def async_setup(hass, config):
    async def async_set_color(service):
        if hass.states.get(TARGET_ID) is None:
            _LOGGER.info("TARGET_ID not found")
            return
            
        temp = hass.states.get(TARGET_ID).state
        hass.states.set(DOMAIN+'.led_color_temp', str(celsius_to_rgb(temp)))


    def hsv_to_rgb(h, s, v):
        if s == 0.0: v*=255; return (v, v, v)
        i = int(h*6.) # XXX assume int() truncates!
        f = (h*6.)-i; p,q,t = int(255*(v*(1.-s))), int(255*(v*(1.-s*f))), int(255*(v*(1.-s*(1.-f)))); v*=255; i%=6
        if i == 0: return (v, t, p)
        if i == 1: return (q, v, p)
        if i == 2: return (p, v, t)
        if i == 3: return (p, q, v)
        if i == 4: return (t, p, v)
        if i == 5: return (v, p, q)

    def celsius_to_rgb(temp):
        # hue = MAX_HUE-(temp-CELSIUS_MIN)*(MAX_HUE/(CELSIUS_MAX-CELSIUS_MIN))
        hue = MAX_HUE*(1-(math.atan((float(temp)-MIDDLE_TEMP)/SENSITIVITY)/math.pi+0.5))
        return hsv_to_rgb(hue/360., 1, 1)

    # register the example.flash service
    hass.services.async_register(DOMAIN, "led_color_service", async_set_color)

    return True
