#!/usr/bin/env python3
# Author: Pavel Rojtberg <http://www.rojtberg.net>
# License: LGPLv2 (same as libsensors)
# Web: https://github.com/paroj/sensors.py

import sensors

def print_feature(chip, feature):
    sfs = list(sensors.SubFeatureIterator(chip, feature)) # get a list of all subfeatures
    
    label = sensors.get_label(chip, feature)
    
    skipname = len(feature.name)+1 # skip common prefix
    vals = [sensors.get_value(chip, sf.number) for sf in sfs]
    
    if feature.type == sensors.feature.INTRUSION:
        # short path for INTRUSION to demonstrate type usage
        status = "alarm" if int(vals[0]) == 1 else "normal"
        print("\t"+label+"\t"+status)
        return
    
    names = [sf.name.decode("utf-8")[skipname:] for sf in sfs]
    data = list(zip(names, vals))
    
    str_data = ", ".join([e[0]+": "+str(e[1]) for e in data])
    print("\t"+label+"\t"+str_data)

if __name__ == "__main__":
    sensors.init() # optionally takes config file
    
    print("libsensors version: "+sensors.version)
    
    for chip in sensors.ChipIterator(): # optional arg like "coretemp-*" restricts iterator
        print(sensors.chip_snprintf_name(chip)+" ("+sensors.get_adapter_name(chip.bus)+")")
        for feature in sensors.FeatureIterator(chip):
            print_feature(chip, feature)
        
    sensors.cleanup()