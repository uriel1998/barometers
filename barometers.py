#! /usr/bin/env python3

import pathlib
import linecache
import configparser
import pickle, sys, string, argparse, datetime
from PIL import Image, ImageDraw, ImageFont

# global variables
appname = "barometers"
dir_appname = "com.stevensaus.barometers"
appauthor = "Steven Saus"
the_silence = False
cache_overwrite = False
to_verify = False

cur_path = pathlib.Path()
cache_dir = cache_path = cur_path.joinpath(cur_path.cwd(),'cache')
data_dir = cache_path = cur_path.joinpath(cur_path.cwd(),'raw')  


def match_cache(weather_location):
    """ See if a pickled cache file exists for the rawfile we're reading in """

    cache_file = cur_path.joinpath(cache_dir,weather_location)
    cache_filename = str(cache_file)
    try:
        file = open(cache_filename, 'rb')
        if the_silence == False:
            print("Reading in cache for location {0}".format(weather_location))
        l_list = pickle.load(file)
        file.close()
        return l_list
    except FileNotFoundError:
        if the_silence == False:
            print("No cache exists for location {0}".format(cache_file))   


def read_in_file(in_file,num_input=256):
    """ Reading in the new file into the pressures data structure """ 
    """ Format has to be CITYID.ext or CITYID_whatever.ext """
        
    test_stem = str(in_file.stem).strip()
        
    if test_stem.find("_") > 0:
        weather_location = test_stem.split('_',1)[0]
    else:
        weather_location = test_stem    

    l_list=match_cache(weather_location)
    
    with open(in_file) as f:
        rowcount = sum(1 for line in f)
    
    # auto-adjusting range to input PRN
    if rowcount <= num_input:
        count = 0
        num_input = rowcount
    else:
        count = rowcount - num_input
    
    for while count < rowcount:  #the generator stuff was making it hard to read...
        count += 1 # for linecache's sake
        row = linecache.getline(str(in_file), count)
        row = row.replace("@", ",")
        row = row.strip()
        if row.find(",,") != -1:
            continue
        else: 
            list_to_add = row.split(',',7)
            if list_to_add[0] == "epoch":  # header row
                continue
            else:
                c1=0
                while c1 < len(l_list):  # we are numerically looping so we can remove entries
                    if l_list[c1][0] == list_to_add[0]:
                        if cache_overwrite == True:
                            del l_list[c1]
                        else:
                            continue  # dupe, next iteration
                # removing units if they exist in there
                try:
                    list_to_add.remove("hPa")
                except ValueError:
                    print("already clean")
                
                try: 
                    list_to_add.remove("in")
                except ValueError:
                    print("already clean")
                                
                l_list(list_to_add)   #needs to be a list because I will use positionals for calculations later
    linecache.clearcache()
    return l_list

def write_cache(weather_location,l_list):
    """ Writing pickled info to cache """
    
    cache_file = cur_path.joinpath(cache_dir,weather_location)
    cache_filename = str(cache_file)
    try:
        cache_file.unlink()
    except FileNotFoundError:
        if the_silence == False: 
            print ("Creating new cache {0}".format(cache_file))
    
    file = open(cache_filename, 'wb')
    pickle.dump(l_list,file)
    file.close()


main(ini):
""" Pull in configurations, main control function """

    global the_silence
    global cache_overwrite 
    global to_verify   
    
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

    if args.quiet is not True:
        the_silence = False
    if args.cache_overwrite is not True:
        cache_overwrite = False
    if args.verify = is not True:
        to_verify = False
        
    # Add in new raw data
    for rawfile in list(cur_path.joinpath(cur_path.cwd(),'raw').iterdir()):    
        if the_silence == False:
            print("Reading in {0}".format(rawfile))
        l_list=read_in_file(format(rawfile),args.num_input)
        write_cache


if __name__ == '__main__':
    main(ini)
else:
    print("barometers loaded as a module")
