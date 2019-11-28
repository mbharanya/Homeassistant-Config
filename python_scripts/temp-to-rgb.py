import math
MAX_HUE = 240
MIDDLE_TEMP = 20
SENSITIVITY = 2
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
    hue = MAX_HUE*(1-(math.atan((temp-MIDDLE_TEMP)/SENSITIVITY)/math.pi+0.5))
    return hsv_to_rgb(hue/360., 1, 1)


print(celsius_to_rgb(10))

# sensor_id = data.get('sensor')
# light_entity_id = data.get('entity_id')

# if sensor_id != "" and light_entity_id != "":
#     sensor = hass.states.get(sensor_id)
#     temp = sensor.state
#     if temp is not None and temp is not "Unknown":
#         service_data = {'entity_id': light_entity_id, 'rgb_color': celsius_to_rgb(temp), 'brightness': 255 }
#         hass.services.call('light', 'turn_on', service_data, False)
