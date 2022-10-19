#! /usr/bin/env python3
# -*- coding: iso-8859-1 -*-

###########################################################################
# Header information 
###########################################################################

"""API_orbits_S1.py: Script to download Sentinel-1 orbit files from the ASF mirror"""

__author__ = "Alexis Hrysiewicz"
__copyright__ = "Copyright 2022"
__credits__ = ["Alexis Hrysiewicz"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Alexis Hrysiewicz"
__status__ = "Production"
__date__ = "Jan. 2022"

###########################################################################
# Python packages
###########################################################################

import os
import os.path
import optparse
import sys
import urllib.request
import re
import datetime
import pandas as pd

###########################################################################
###########################################################################

class OptionParser (optparse.OptionParser):

    def check_required(self, opt):
        option = self.get_option(opt)
        if getattr(self.values, option.dest) is None:
            self.error("%s option not supplied" % option)

###########################################################################
###########################################################################

if len(sys.argv) != 9:
    prog = os.path.basename(sys.argv[0])
    print("example: python3 %s -f SLC.list -o Orbits -u username -p password" %
          sys.argv[0])
    sys.exit(-1)
else:
    usage = "usage: %prog [options] "
    parser = OptionParser(usage=usage)
    parser.add_option("-f", "--file", dest="file", action="store", type="string", default='SLC.list')
    parser.add_option("-o", "--output", dest="output", action="store", type="string", default='.')
    parser.add_option("-u", "--username", dest="user", action="store", type="string", default='username')
    parser.add_option("-p", "--password", dest="password", action="store", type="string", default='XXXXXX')
    (options, args) = parser.parse_args()

###########################################################################
# MAIN
###########################################################################

if os.path.isfile('tmp_list_orbits_download.txt'):
    os.remove('tmp_list_orbits_download.txt')

# Check the precise files
url_precise = "https://s1qc.asf.alaska.edu/aux_poeorb/"
html = urllib.request.urlopen(url_precise)
text = html.read()
plaintext = text.decode('utf8')
links = re.findall("href=[\"\'](.*?)[\"\']", plaintext)
orbits_precise = []
for li in links:
    if ".EOF" in li:
        orbits_precise.append(li)

# Check the restitued files
url_restitued = "https://s1qc.asf.alaska.edu/aux_resorb/"
html = urllib.request.urlopen(url_restitued)
text = html.read()
plaintext = text.decode('utf8')
links = re.findall("href=[\"\'](.*?)[\"\']", plaintext)
orbits_restitued = []
for li in links:
    if ".EOF" in li:
        orbits_restitued.append(li)

# Open the list of SLCs
dateSLC = []
satSLC = []
date_format = "%Y-%m-%dT%H:%M:%S" 
fi = pd.read_csv(options.file)
h = 0
for slci in fi['Granule Name']:
    if 'S1A' in slci:
        satSLC.append("S1A")
    elif 'S1B' in slci:
        satSLC.append("S1B")
    
    di = fi['Acquisition Date'][h].split('.')[0]
    dateSLC.append(datetime.datetime.strptime(di, date_format))
    h+=1

# Downloading
date_format = "%Y%m%dT%H%M%S" 
for i in range(len(dateSLC)):
    dslc = dateSLC[i]
    sati = satSLC[i]
    a = 'Checking of orbits for %s SLC acquired by %s' % (dslc,sati)
    print(a)
    check_precise=False
    check_restitued=False
    name_orbit_precise = []
    name_orbit_restitued = []
    for pi in orbits_precise:
        if sati in pi: 
            orb_test = pi.split('V')[1].split('.')[0]
            d1 = datetime.datetime.strptime(orb_test.split('_')[0], date_format)
            d2 = datetime.datetime.strptime(orb_test.split('_')[1], date_format)
            if d1 <= dslc <= d2:
                check_precise=True
                name_orbit_precise.append(pi)
    if check_precise:
        for ni in name_orbit_precise:
            a = '\tThe precise orbit %s has been found.' % (ni)
            print(a)
    else:
        a = '\tNo precise orbit has been found, checking of restitued orbit...'
        print(a)
        for pi in orbits_restitued:
            if sati in pi: 
                orb_test = pi.split('V')[1].split('.')[0]
                d1 = datetime.datetime.strptime(orb_test.split('_')[0], date_format)
                d2 = datetime.datetime.strptime(orb_test.split('_')[1], date_format)
                if d1 <= dslc <= d2:
                    check_restitued=True
                    name_orbit_restitued.append(pi)
        if check_restitued:
            for ni in name_orbit_restitued:
                a = '\tThe restitued orbit %s has been found.' % (ni)
                print(a)
    if check_precise:
        for ni in name_orbit_precise: 
            if not os.path.isfile(options.output+'/'+ni): 
                with open('tmp_list_orbits_download.txt','a') as fi:
                    fi.write('%s\n' %(url_precise+ni))
    if check_restitued:
        for ni in name_orbit_restitued: 
            if not os.path.isfile(options.output+'/'+ni): 
                with open('tmp_list_orbits_download.txt','a') as fi:
                    fi.write('%s\n' %(url_restitued+ni))
                
if os.path.isfile('tmp_list_orbits_download.txt'):
    cmd = "wget --user %s --password %s -P %s -i %s" % (options.user,options.password,options.output,'tmp_list_orbits_download.txt')
    os.system(cmd)
    os.remove('tmp_list_orbits_download.txt')
