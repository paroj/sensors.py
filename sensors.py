# Author: Pavel Rojtberg <http://www.rojtberg.net>
# License: LGPLv2 (same as libsensors)
# Web: https://github.com/paroj/sensors.py
"""
sensors.py: Python Bindings for libsensors3

use the documentation of libsensors for the low level API.
see example.py for high level API usage.
"""

from ctypes import *
import ctypes.util

_libc = cdll.LoadLibrary(ctypes.util.find_library("c"))
_hdl = cdll.LoadLibrary(ctypes.util.find_library("sensors"))

version = c_char_p.in_dll(_hdl, "libsensors_version").value.decode("ascii")

class bus_id(Structure):
    _fields_ = [("type", c_short),
                ("nr", c_short)]

class chip_name(Structure):
    _fields_ = [("prefix", c_char_p),
                ("bus", bus_id),
                ("addr", c_int),
                ("path", c_char_p)]

class feature(Structure):
    _fields_ = [("name", c_char_p),
                ("number", c_int),
                ("type", c_int)]
    
    # sensors_feature_type
    IN = 0x00
    FAN = 0x01
    TEMP = 0x02
    POWER = 0x03
    ENERGY = 0x04
    CURR = 0x05
    HUMIDITY = 0x06
    MAX_MAIN = 0x7
    VID = 0x10
    INTRUSION = 0x11
    MAX_OTHER = 0x12
    BEEP_ENABLE = 0x18

class subfeature(Structure):
    _fields_ = [("name", c_char_p),
                ("number", c_int),
                ("type", c_int),
                ("mapping", c_int),
                ("flags", c_uint)]

_hdl.sensors_get_detected_chips.restype = POINTER(chip_name)
_hdl.sensors_get_features.restype = POINTER(feature)
_hdl.sensors_get_all_subfeatures.restype = POINTER(subfeature)
_hdl.sensors_get_label.restype = c_void_p # return pointer instead of str so we can free it
_hdl.sensors_get_adapter_name.restype = c_char_p # docs do not say whether to free this or not 

### RAW API ###
MODE_R = 1
MODE_W = 2
COMPUTE_MAPPING = 4

def init(cfg_file = None):
    file = _libc.fopen(cfg_file) if cfg_file is not None else None 
    
    if _hdl.sensors_init(file) != 0:
        raise Exception("sensors_init failed")

def cleanup():
    _hdl.sensors_cleanup()

def parse_chip_name(orig_name):
    res = chip_name()
    if _hdl.sensors_parse_chip_name(orig_name.encode("utf-8"), byref(res)) < 0:
        raise Exception("parse_chip_name('{}') failed".format(orig_name))
    return res

def get_detected_chips(match, nr):
    """
    @return: opaque chip handle, next nr to query
    """
    _nr = c_int(nr)
    
    if match is not None:
        match = byref(match)
    
    chip = _hdl.sensors_get_detected_chips(match, byref(_nr))
    chip = chip.contents if bool(chip) else None
    return chip, _nr.value

def chip_snprintf_name(chip):
    ret = create_string_buffer(200) # same size as in sensors utility
    if _hdl.sensors_snprintf_chip_name(ret, 200, byref(chip)) < 0:
        raise Exception("sensors_snprintf_chip_name failed")
        
    return ret.value.decode("utf-8")

def do_chip_sets(chip):
    """
    ATTENTION: untested!
    """
    if _hdl.sensors_do_chip_sets(byref(chip)) < 0:
        raise Exception("sensors_do_chip_sets failed")
    
def get_adapter_name(bus):
    return _hdl.sensors_get_adapter_name(byref(bus)).decode("utf-8")

def get_features(chip, nr):
    """
    @return: feature, next nr to query
    """
    _nr = c_int(nr)
    feature = _hdl.sensors_get_features(byref(chip), byref(_nr))
    feature = feature.contents if bool(feature) else None
    return feature, _nr.value

def get_label(chip, feature):
    ptr = _hdl.sensors_get_label(byref(chip), byref(feature)) 
    val = cast(ptr, c_char_p).value.decode("utf-8")
    _libc.free(ptr)
    return val

def get_all_subfeatures(chip, feature, nr):
    """
    @return: subfeature, next nr to query
    """
    _nr = c_int(nr)
    subfeature = _hdl.sensors_get_all_subfeatures(byref(chip), byref(feature), byref(_nr))
    subfeature = subfeature.contents if bool(subfeature) else None
    return subfeature, _nr.value

def get_value(chip, subfeature_nr):
    val = c_double()
    if _hdl.sensors_get_value(byref(chip), subfeature_nr, byref(val)) < 0:
        raise Exception("sensors_get_value({}, {}) failed".format(chip, subfeature_nr))
    return val.value

def set_value(chip, subfeature_nr, value):
    """
    ATTENTION: untested!
    """
    val = c_double(value)
    if _hdl.sensors_set_value(byref(chip), subfeature_nr, byref(val)) < 0:
        raise Exception("sensors_set_value({}, {}, {}) failed".format(chip, subfeature_nr, value))

### Convenience API ###
class ChipIterator:
    def __init__(self, match = None):
        self.match = parse_chip_name(match) if match is not None else None
    
    def __iter__(self):
        self.nr = 0
        return self
     
    def __next__(self):
        chip, self.nr = get_detected_chips(self.match, self.nr)
        
        if chip is None:
            raise StopIteration
        
        return chip
    
    def next(self): # python2 compability
        return self.__next__()
    
class FeatureIterator:
    def __init__(self, chip):
        self.chip = chip

    def __iter__(self):
        self.nr = 0
        return self
        
    def __next__(self):
        feature, self.nr = get_features(self.chip, self.nr)
        
        if feature is None:
            raise StopIteration
        
        return feature

    def next(self): # python2 compability
        return self.__next__()
    
class SubFeatureIterator:
    def __init__(self, chip, feature):
        self.chip = chip
        self.feature = feature
    
    def __iter__(self):
        self.nr = 0
        return self
        
    def __next__(self):
        subfeature, self.nr = get_all_subfeatures(self.chip, self.feature, self.nr)
        
        if subfeature is None:
            raise StopIteration
        
        return subfeature
    
    def next(self): # python2 compability
        return self.__next__()
