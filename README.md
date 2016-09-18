sensors.py
==========
python bindings using ctypes for libsensors3 of the [lm-sensors project](https://github.com/groeck/lm-sensors). The code was written against libsensors 3.3.4.  

For documentation of the low level API see [sensors.h](https://github.com/groeck/lm-sensors/blob/master/lib/sensors.h). For an example of the high level API see [example.py](example.py).

For a GUI application that displays the sensor readings and is based on this library, take a look at [sensors-unity](https://launchpad.net/sensors-unity).

Features
--------
* Full access to low level libsensors3 API
* High level iterator API
* unicode handling
* Python2 and Python3 compatible

Licensing
---------
LGPLv2 (same as libsensors3)

Usage Notes
-----------
As Python does not support call by reference for primitive types some of the libsensors API had to be adapted:

```python
# nr is changed by refrence in the C API
chip_name, nr = sensors.get_detected_chips(None, nr)

# returns the value. throws on error
val = sensors.get_value(chip, subfeature_nr)
```

Missing Features (pull requests are welcome):
* `sensors_subfeature_type` enum
* `sensors_get_subfeature`
* Error handlers
