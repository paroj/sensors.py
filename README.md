sensors.py
==========
python bindings using ctypes for libsensors3 of the [lm-sensors project](http://www.lm-sensors.org/). The code was written against libsensors 3.3.4.


For documentation of the low level API see [sensors.h](http://www.lm-sensors.org/browser/lm-sensors/tags/V3-3-4/lib/sensors.h). For an example of the high level API see [example.py](example.py).

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
As Python does not support call by reference for primitive types some of the libsensors API had to be adapted.

Iterate over all chips using the low level API:
```python
nr = 0
feature, nr = get_detected_chips(None, nr) # nr gets changed by the C API
```

Missing Features (pull requests are welcome):
* `sensors_get_subfeature` wrapper
* `sensors_subfeature_type` enum
