#! /usr/bin/env python3
# -*- coding: utf-8 -*-

###########################################################################
# Header information 
###########################################################################

"""API_download_S1_SLC.py: Script to download Sentinel-1 SLC images from the ASF mirror"""

__author__ = "Alexis Hrysiewicz"
__copyright__ = "Copyright 2022"
__credits__ = ["Alexis Hrysiewicz"]
__license__ = "GPL"
__version__ = "3.0.0"
__maintainer__ = "Alexis Hrysiewicz"
__status__ = "Production"
__date__ = "Jan. 2022"

###########################################################################
# Python packages
###########################################################################

import os 
import sys
import pandas as pd
import datetime
import os.path
import optparse

###########################################################################
###########################################################################

class OptionParser (optparse.OptionParser):

    def check_required(self, opt):
        option = self.get_option(opt)
        if getattr(self.values, option.dest) is None:
            self.error("%s option not supplied" % option)

###########################################################################
###########################################################################

if len(sys.argv) != 23:
    prog = os.path.basename(sys.argv[0])
    print("example: python3 %s -u username -p password -s . -r . -b -10.78,51.27,-5.03,55.70 -i 2017-01-01T00:00:00 -j 2023-12-31T00:00 -o 1 -f a -m csv -w n" %
          sys.argv[0])
    sys.exit(-1)
else:
    usage = "usage: %prog [options] "
    parser = OptionParser(usage=usage)
    parser.add_option("-u", "--username", action="store", type="string", default='username') 
    parser.add_option("-p", "--password", action="store", type="string", default='password')
    parser.add_option("-s", "--path_SLC", action="store", type="string", default='.')
    parser.add_option("-r", "--path_RSLC", action="store", type="string", default='.') # Only available for GAMMA stack
    parser.add_option("-b", "--bbox", action="store", type="string", default='-10.78,51.27,-5.03,55.70')
    parser.add_option("-i", "--date_start", action="store", type="string", default='2017-01-01T00:00:00')
    parser.add_option("-j", "--date_end", action="store", type="string", default='2024-01-01T00:00:00')
    parser.add_option("-o", "--orbit_relative", action="store", type="float", default='1')
    parser.add_option("-f", "--flight_direction", action="store", type="string", default='a')
    parser.add_option("-m", "--mode", action="store", type="string", default='csv')
    parser.add_option("-w", "--write", action="store", type="string", default='n')
    (options, args) = parser.parse_args()

###########################################################################
# Main
###########################################################################

date_format = "%Y-%m-%d"

cmd1 = 'curl "https://api.daac.asf.alaska.edu/services/search/param?platform=s1&bbox=%s&start=%sUTC&end=%sUTC&relativeOrbit=%d&flightDirection=%s&processingLevel=SLC&maxResults=10000&output=%s" > SLC_list.%s' % (options.bbox,options.date_start,options.date_end,int(options.orbit_relative),options.flight_direction.upper(),options.mode.upper(),options.mode.lower())

if options.mode.upper() == 'KML':
    os.system(cmd1)
elif options.mode.upper() == 'CSV':
    os.system(cmd1)
else:
    print('Please, select a correct mode (csv or kml)...')

if options.mode.upper() == 'CSV' and options.write.upper() == 'Y':
    listSLC = pd.read_csv("SLC_list.csv")
    h = 0
    for slci in listSLC['Granule Name']:
        print('Checking if the SLC %s is stored or processed (.zip or .rslc from GAMMA)\n\t The url is %s' % (slci,listSLC['URL'][h]))
        datei = datetime.datetime.strptime(listSLC['Acquisition Date'][h].split('.')[0], '%Y-%m-%dT%H:%M:%S').strftime("%Y%m%d")
        if os.path.exists(options.path_SLC+'/'+slci+'.zip') == 1 or os.path.exists(options.path_RSLC+'/'+datei+'.vv.rslc') == 1:
            print('\t\tThe SLC has been stored or processed.')
        else:
            print('\t\tThe SLC has not been stored or processed. Downloading needed...')
            cmd1 = 'wget -c --http-user=%s --http-password=%s "%s" -P %s' % (options.username,options.password,listSLC['URL'][h],options.path_SLC)
            os.system(cmd1)
        h+=1
elif options.mode.upper() == 'KML' and options.write.upper() == 'Y':
    print('Please, select a CSV mode to download..')
