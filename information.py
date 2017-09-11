__author__ = 'Bhagat'
import time
import geocoder
from requests.exceptions import ConnectionError
def get_info():
    try:
        g = geocoder.ip('me')
        place = g.json['address']
    except ConnectionError:
        place = ''

    current_time = time.asctime()
    return current_time, place
print 'you just imported me'
