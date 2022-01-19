#! /usr/bin/env python3

import pathlib
import linecache
import configparser
import os
from os.path import expanduser
from appdirs import *
import pickle, sys, string, argparse, datetime
from PIL import Image, ImageDraw, ImageFont

# global variables
appname = "barometers"
dir_appname = "com.stevensaus.barometers"
appauthor = "Steven Saus"
the_silence = False

cur_path = pathlib.Path()
cachedir = user_cache_dir(dir_appname)
configdir = user_config_dir(dir_appname)
if not os.path.isdir(cachedir):
    os.makedirs(user_cache_dir(dir_appname))
if not os.path.isdir(configdir):
    os.makedirs(user_config_dir(dir_appname))
ini = os.path.join(configdir,'barometers.ini')



main(ini):
""" Pull in configurations, main control function """

    #TODO - add try statement here 
    config = configparser.ConfigParser()
    config.read(ini)
    sections=config.sections()

    parser = argparse.ArgumentParser(usage=__doc__)
    # generic arguments
    parser.add_argument("-q", "--quiet", dest="quiet",action='store_true', default=False, help="Minimize output to STDOUT/STDERR")
    #adding arguments
    parser.add_argument("-a", "--add-records", type=int, help="max number of records to add from input files", default=256,action='store',dest='num_input')
    parser.add_argument("-r", "--retrieve-current", dest="get_data",action='store_true', default=False, help="Get reading from OpenWeatherMap")    
    parser.add_argument("-o", "--overwrite-cache", dest="cache_overwrite",action='store_true', default=False, help="Overwrite cache data when importing new data.")
    # choosing arguments
    parser.add_argument('-B', '--bout-here', action='store', dest='bout_here',help="Where to output/input weather location from."    
    parser.add_argument("-b", "--begin-date", dest="start_date", action='store', default=None,help="Provide the start date for chart or calculation data.")
    parser.add_argument("-e", "--end-date", dest="end_date", action='store', default=None,help="Provide the end date for chart or calculation data; optional, only makes sense with --begin-date.")
    parser.add_argument("-d", "--display-records", type=int, help="number of records back to display", default=None,action='store',dest='num_output')
    parser.add_argument("-s", "--scheme", dest="scheme",action='store', default=None, help="Color scheme - default, wide, alt, original")
    # verification arguments
    parser.add_argument('-v', '--verify', dest='to_verify', action='store_true', default=False,help="Verify interval ranges")
    parser.add_argument('-t', '--tolerance', action='store',dest='tolerance_range', default="300",help="Acceptable range in seconds, only makes sense with -v")
    parser.add_argument('-i', '--interval', action='store',dest='verify_interval', default="1800",help="Expected interval in seconds, only makes sense with -v")    
    # output arguments
    parser.add_argument('-f', '--file', action='store',dest='fn_stem', default="out",help="Stem for output filename, defaults to out_[abs|signed].png")
    parser.add_argument("-w", "--walk_about", dest="walkabout",action='store_true', default=False, help="Modify walking chart by distance from present")
    # type of output arguments
    parser.add_argument("-D", "--show-data", dest="showdata",action='store_true', default=False, help="Show data of range on stdout")
    parser.add_argument("-L", "--line-graph", dest="linegraph",action='store_true', default=False, help="Produce line graph overlay")
    parser.add_argument("-S", "--signed-values", dest="signval",action='store_true', default=False, help="Produce signed value chart")
    parser.add_argument("-A", "--abs-values", dest="absval",action='store_true', default=False, help="Produce abs value chart")
    parser.add_argument("-W", "--walking", dest="walking",action='store_true', default=False, help="Produce walking value chart")
    args = parser.parse_args()

    # Add in new raw data
    for rawfile in list(cur_path.joinpath(cur_path.cwd(),'raw').iterdir()):    
        if the_silence == False:
            print("Reading in {0}".format(rawfile))
        
        read_in_file(format(rawfile),args.num_input)





if __name__ == '__main__':
    main(ini)
else:
    print("barometers loaded as a module")
