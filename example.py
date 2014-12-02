#!/usr/bin/env python3
# Author: Pavel Rojtberg <http://www.rojtberg.net>
# License: LGPL2 (same as libsensors)
# Web: 

import sensors

def print_feature(chip, feature):
    sfs = list(sensors.SubFeatureIterator(chip, feature)) # get a list of all subfeatures
    
    skipname = len(feature.name)+1 # skip common prefix
    vals = [sensors.get_value(chip, sf.number) for sf in sfs]
    names = [sf.name.decode("utf-8")[skipname:] for sf in sfs]
    data = list(zip(names, vals))
    
    label = sensors.get_label(chip, feature)
    str_data = [e[0]+": "+str(e[1]) for e in data]
    print("\t"+label+"\t"+", ".join(str_data))

if __name__ == "__main__":
    sensors.init() # optionally takes config file
    
    print("libsensors version: "+sensors.version)
    
    for chip in sensors.ChipIterator("coretemp-*"): # use sensors.ChipIterator() to iterate over all chips
        print(sensors.chip_snprintf_name(chip)+" ("+sensors.get_adapter_name(chip.bus)+")")
        for feature in sensors.FeatureIterator(chip):
            print_feature(chip, feature)
        
    sensors.cleanup()