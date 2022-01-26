#! /usr/bin/env python3

import pathlib
import linecache
import configparser
import requests
import time
import pickle, sys, string, argparse, datetime
from PIL import Image, ImageDraw, ImageFont
from datetime import date, datetime, timedelta

# global variables
appname = "barometers"
dir_appname = "com.stevensaus.barometers"
appauthor = "Steven Saus"
the_silence = False
cache_overwrite = False
to_verify = False
tolerance = 0
interval = 0 
cur_path = pathlib.Path()
cache_dir = cur_path.joinpath(cur_path.cwd(),'cache')
data_dir = cur_path.joinpath(cur_path.cwd(),'raw')  
ini_file = cur_path.joinpath(cur_path.cwd(),'barometers.ini')  

_my_colors = { -16:(255, 255, 255),-15:(255, 224, 224),-14:(255, 192, 192), 
    -13:(255, 160, 160),-12:(255, 128, 128),-11:(255, 96, 96),  
    -10:(255, 64, 64),-9:(255, 32, 32),-8:(255, 0, 0),-7:(224, 0, 0), 
    -6:(192, 0, 0),-5:(160, 0, 0),-4:(128, 0, 0),-3:(96, 0, 0), 
    -2:(64, 0, 0),-1:(32, 0, 0),0:(0, 0, 0),16:(255, 255, 255),15:(255,236,224),14:(255,216,192),
    13:(255,196,160),12:(255,176,128),11:(255,156,96),10:(255,136,64),
    9:(255,116,32),8:(255,96,0),7:(224,84,0),6:(192,72,0),5:(160,60,0),
    4:(128,48,0),3:(96,36,0),2:(64,24,0),1:(32,12,0)}

_my_colors_alt = { -16:(255, 255, 255),-15:(255, 224, 224),-14:(255, 192, 192), 
    -13:(255, 160, 160),-12:(255, 128, 128),-11:(255, 96, 96),  
    -10:(255, 64, 64),-9:(255, 32, 32),-8:(255, 0, 0),-7:(224, 0, 0), 
    -6:(192, 0, 0),-5:(160, 0, 0),-4:(128, 0, 0),-3:(96, 0, 0), 
    -2:(64, 0, 0),-1:(32, 0, 0),0:(0, 0, 0),16:(255, 255, 255), 15:(255, 224, 248), 
    14:(255, 192, 240),13:(255, 160, 232), 12:(255, 128, 224), 11:(255, 96, 216),
    10:(64, 232, 208), 9:(255, 32, 200), 8:(255, 0, 192), 7:(224, 0, 168),
    6:(192, 0, 144), 5:(160, 0, 120), 4:(128, 0, 96), 3:(96, 0, 72),
    2:(64, 0, 48), 1:(32, 0, 24)}

_my_colors_original = { 18:(96, 0, 0),-18:(96, 0, 0), 17:(96, 12, 0), -17:(96, 24, 0), 
    16:(96, 36, 0), -16:(96, 48, 0), 15:(96, 60, 0), -15:(96, 72, 0), 
    14:(96, 84, 0), -14:(96, 96, 0), 13:(84, 96, 0), -13:(72, 96, 0), 
    12:(60, 96, 0), -12:(48, 96, 0), 11:(36, 96, 0), -11:(24, 96, 0), 
    10:(12, 96, 0), -10:(0, 96, 0), 9:(0, 96, 12), -9:(0, 96, 24), 
    8:(0, 96, 36), -8:(0, 96, 48), 7:(0, 96, 60), -7:(0, 96, 72), 
    6:(0, 96, 84), -6:(0, 96, 96), 5:(0, 84, 96), -5:(0, 72, 96), 
    4:(0, 60, 96), -4:(0, 48, 96), 3:(0, 36, 96), -3:(0, 24, 96), 
    2:(0, 12, 96), -2:(0, 0, 96), 1:(0, 0, 64), -1:(0, 0, 32), 0:(0, 0, 0)}

_my_colors_wide = {-24:(192, 0, 0), -23:(192, 24, 0), -22:(192, 48, 0), -21:(192, 72, 0), -20:(192, 96, 0), -19:(192, 120, 0), -18:(192, 144, 0), -17:(192, 168, 0), -16:(192, 192, 0), -15:(168, 192, 0), -14:(144, 192, 0), -13:(120, 192, 0), -12:(96, 192, 0), -11:(72, 192, 0), -10:(48, 192, 0), -9:(24, 192, 0), -8:(0, 192, 0), -7:(0, 192, 24), -6:(0, 192, 48), -5:(0, 192, 72), -4:(0, 192, 96), -3:(0, 192, 120), -2:(0, 192, 144), -1:(0, 192, 168), 0:(0, 192, 192), 1:(0, 168, 192), 2:(0, 144, 192), 3:(0, 120, 192), 4:(0, 96, 192), 5:(0, 72, 192), 6:(0, 48, 192), 7:(0, 24, 192), 8:(0, 0, 192), 9:(24, 0, 192), 10:(48, 0, 192), 11:(72, 0, 192), 12:(96, 0, 192), 13:(120, 0, 192), 14:(144, 0, 192), 15:(168, 0, 192), 16:(192, 0, 192), 17:(192, 0, 168), 18:(192, 0, 144), 19:(192, 0, 120), 20:(192, 0, 96), 21:(192, 0, 72), 22:(192, 0, 48), 23:(192, 0, 24), 24:(192, 0, 0)}

_my_colors_superwide = {53:(255, 255, 0), 52:(224, 224, 0), 51:(192, 192, 0), 50:(160, 160, 0), 49:(128, 128, 0), 48:(96, 96, 0), 47:(64, 64, 0), 46:(32, 32, 0), 45:(0, 0, 0), 44:(255, 0, 0), 43:(224, 0, 0), 42:(192, 0, 0), 41:(160, 0, 0), 40:(128, 0, 0), 39:(96, 0, 0), 38:(64, 0, 0), 37:(32, 0, 0), 36:(0, 0, 0), 35:(255, 0, 255), 34:(224, 0, 224), 33:(192, 0, 192), 32:(160, 0, 160), 31:(128, 0, 128), 30:(96, 0, 96), 29:(64, 0, 64), 28:(32, 0, 32), 27:(0, 0, 0), 26:(0, 255, 0), 25:(0, 224, 0), 24:(0, 192, 0), 23:(0, 160, 0), 22:(0, 128, 0), 21:(0, 96, 0), 20:(0, 64, 0), 19:(0, 32, 0), 18:(0, 0, 0), 17:(0, 255, 255), 16:(0, 224, 224), 15:(0, 192, 192), 14:(0, 160, 160), 13:(0, 128, 128), 12:(0, 96, 96), 11:(0, 64, 64), 10:(0, 32, 32), 9:(0, 0, 0), 8:(0, 0, 255), 7:(0, 0, 224), 6:(0, 0, 192), 5:(0, 0, 160), 4:(0, 0, 128), 3:(0, 0, 96), 2:(0, 0, 64), 1:(0, 0, 32), 0:(0, 0, 0)}

_my_colors_autoscale1 = { 0:(0, 0, 0), 1:(0, 0, 64), 2:(0, 0, 96), 3:(0, 96, 96), 4:(0, 128, 128), 5:(0, 96, 0), 6:(0, 128, 0), 7:(96, 96, 0), 8:(128, 128, 0), 9:(96, 0, 96), 10:(128, 0, 128), 11:(128, 0, 0), 12:(96, 0, 0), -1:(0, 0, 64), -2:(0, 0, 96), -3:(0, 96, 96), -4:(0, 128, 128), -5:(0, 96, 0), -6:(0, 128, 0), -7:(96, 96, 0), -8:(128, 128, 0), -9:(96, 0, 96), -10:(128, 0, 128), -11:(128, 0, 0), -12:(96, 0, 0)}

_my_colors_autoscale2 = {0:(0, 0, 0), 1:(0, 0, 64), 2:(0, 0, 96), 3:(0, 0, 128), 4:(0, 96, 96), 5:(0, 128, 128), 6:(0, 160, 160), 7:(0, 96, 0), 8:(0, 128, 0), 9:(0, 160, 0), 10:(96, 96, 0), 11:(128, 128, 0), 12:(160, 160, 0), 13:(96, 0, 96), 14:(128, 0, 128), 15:(160, 0, 160), 16:(160, 0, 0), 17:(128, 0, 0), 18:(96, 0, 0), -1:(0, 0, 64), -2:(0, 0, 96), -3:(0, 0, 128), -4:(0, 96, 96), -5:(0, 128, 128), -6:(0, 160, 160), -7:(0, 96, 0), -8:(0, 128, 0), -9:(0, 160, 0), -10:(96, 96, 0), -11:(128, 128, 0), -12:(160, 160, 0), -13:(96, 0, 96), -14:(128, 0, 128), -15:(160, 0, 160), -16:(160, 0, 0), -17:(128, 0, 0), -18:(96, 0, 0)}

_my_colors_autoscale3 = {0:(0, 0, 0), 1:(0, 0, 64), 2:(0, 0, 96), 3:(0, 0, 128), 4:(0, 0, 160), 5:(0, 96, 96), 6:(0, 128, 128), 7:(0, 160, 160), 8:(0, 192, 192), 9:(0, 96, 0), 10:(0, 128, 0), 11:(0, 160, 0), 12:(0, 192, 0), 13:(96, 96, 0), 14:(128, 128, 0), 15:(160, 160, 0), 16:(192, 192, 0), 17:(96, 0, 96), 18:(128, 0, 128), 19:(160, 0, 160), 20:(192, 0, 192), 21:(160, 0, 0), 22:(128, 0, 0), 23:(96, 0, 0), 24:(192, 0, 0), -1:(0, 0, 64), -2:(0, 0, 96), -3:(0, 0, 128), -4:(0, 0, 160), -5:(0, 96, 96), -6:(0, 128, 128), -7:(0, 160, 160), -8:(0, 192, 192), -9:(0, 96, 0), -10:(0, 128, 0), -11:(0, 160, 0), -12:(0, 192, 0), -13:(96, 96, 0), -14:(128, 128, 0), -15:(160, 160, 0), -16:(192, 192, 0), -17:(96, 0, 96), -18:(128, 0, 128), -19:(160, 0, 160), -20:(192, 0, 192), -21:(160, 0, 0), -22:(128, 0, 0), -23:(96, 0, 0), -24:(192, 0, 0)}

_my_colors_autoscale4 = {0:(0, 0, 0), 1:(0, 0, 64), 2:(0, 0, 96), 3:(0, 0, 128), 4:(0, 0, 160), 5:(0, 0, 160), 6:(0, 0, 192), 7:(0, 96, 96), 8:(0, 128, 128), 9:(0, 160, 160), 10:(0, 192, 192), 11:(0, 224, 224), 12:(0, 255, 255), 13:(0, 96, 0), 14:(0, 128, 0), 15:(0, 160, 0), 16:(0, 192, 0), 17:(0, 224, 0), 18:(0, 255, 0), 19:(96, 96, 0), 20:(128, 128, 0), 21:(160, 160, 0), 22:(192, 192, 0), 23:(224, 224, 0), 24:(255, 255, 0), 25:(96, 0, 96), 26:(128, 0, 128), 27:(160, 0, 160), 28:(192, 0, 192), 29:(224, 0, 224), 30:(255, 0, 255), 31:(160, 0, 0), 32:(128, 0, 0), 33:(96, 0, 0), 34:(192, 0, 0), 35:(224, 0, 0), 36:(255, 0, 0), -0:(0, 0, 0), -1:(0, 0, 64), -2:(0, 0, 96), -3:(0, 0, 128), -4:(0, 0, 160), -5:(0, 0, 160), -6:(0, 0, 192), -7:(0, 96, 96), -8:(0, 128, 128), -9:(0, 160, 160), -10:(0, 192, 192), -11:(0, 224, 224), -12:(0, 255, 255), -13:(0, 96, 0), -14:(0, 128, 0), -15:(0, 160, 0), -16:(0, 192, 0), -17:(0, 224, 0), -18:(0, 255, 0), -19:(96, 96, 0), -20:(128, 128, 0), -21:(160, 160, 0), -22:(192, 192, 0), -23:(224, 224, 0), -24:(255, 255, 0), -25:(96, 0, 96), -26:(128, 0, 128), -27:(160, 0, 160), -28:(192, 0, 192), -29:(224, 0, 224), -30:(255, 0, 255), -31:(160, 0, 0), -32:(128, 0, 0), -33:(96, 0, 0), -34:(192, 0, 0), -35:(224, 0, 0), -36:(255, 0, 0)}

_my_colors_autoscale5 = {0:(0, 0, 0), 1:(0, 0, 64), 2:(0, 0, 96), 3:(0, 0, 128), 4:(0, 0, 160), 5:(0, 0, 160), 6:(0, 0, 192), 7:(0, 0, 224), 8:(0, 0, 255), 9:(0, 96, 96), 10:(0, 128, 128), 11:(0, 160, 160), 12:(0, 192, 192), 13:(0, 224, 224), 14:(0, 255, 255), 15:(32, 255, 255), 16:(64, 255, 255), 17:(0, 96, 0), 18:(0, 128, 0), 19:(0, 160, 0), 20:(0, 192, 0), 21:(0, 224, 0), 22:(0, 255, 0), 23:(32, 255, 32), 24:(64, 255, 64), 25:(96, 96, 0), 26:(128, 128, 0), 27:(160, 160, 0), 28:(192, 192, 0), 29:(224, 224, 0), 30:(255, 255, 0), 31:(255, 255, 32), 32:(255, 255, 64), 33:(96, 0, 96), 34:(128, 0, 128), 35:(160, 0, 160), 36:(192, 0, 192), 37:(224, 0, 224), 38:(255, 0, 255), 39:(255, 32, 255), 40:(255, 64, 255), 41:(160, 0, 0), 42:(128, 0, 0), 43:(96, 0, 0), 44:(192, 0, 0), 45:(224, 0, 0), 46:(255, 0, 0), 47:(255, 32, 32), 48:(255, 64, 64), -1:(0, 0, 64), -2:(0, 0, 96), -3:(0, 0, 128), -4:(0, 0, 160), -5:(0, 0, 160), -6:(0, 0, 192), -7:(0, 0, 224), -8:(0, 0, 255), -9:(0, 96, 96), -10:(0, 128, 128), -11:(0, 160, 160), -12:(0, 192, 192), -13:(0, 224, 224), -14:(0, 255, 255), -15:(32, 255, 255), -16:(64, 255, 255), -17:(0, 96, 0), -18:(0, 128, 0), -19:(0, 160, 0), -20:(0, 192, 0), -21:(0, 224, 0), -22:(0, 255, 0), -23:(32, 255, 32), -24:(64, 255, 64), -25:(96, 96, 0), -26:(128, 128, 0), -27:(160, 160, 0), -28:(192, 192, 0), -29:(224, 224, 0), -30:(255, 255, 0), -31:(255, 255, 32), -32:(255, 255, 64), -33:(96, 0, 96), -34:(128, 0, 128), -35:(160, 0, 160), -36:(192, 0, 192), -37:(224, 0, 224), -38:(255, 0, 255), -39:(255, 32, 255), -40:(255, 64, 255), -41:(160, 0, 0), -42:(128, 0, 0), -43:(96, 0, 0), -44:(192, 0, 0), -45:(224, 0, 0), -46:(255, 0, 0), -47:(255, 32, 32), -48:(255, 64, 64)}



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
    if l_list is None:
        l_list=[]
        
    with open(in_file) as f:
        rowcount = sum(1 for line in f)
    
    # auto-adjusting range to input PRN
    if rowcount <= num_input:
        count = 0
        num_input = rowcount
    else:
        count = rowcount - num_input
    
    
    while count < rowcount:  
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
                if len(l_list) != 0:
                    c1=0
                    while c1 < len(l_list):  # we are numerically looping so we can remove entries
                        if int(l_list[c1][0]) == int(list_to_add[0]):
                            if cache_overwrite == True:
                                if the_silence == False: 
                                    print("Duplicate; overwriting cache entry at {0}".format(list_to_add[0]))
                                del l_list[c1]
                        c1 += 1
                try:
                    list_to_add.remove("hPa")
                except ValueError:
                    print("already clean")
                try: 
                    list_to_add.remove("in")
                except ValueError:
                    print("already clean")  
                l_list.append(list_to_add)   
                
                
    linecache.clearcache()
    if to_verify == True:
        l_list = verify_data(l_list)
        
    write_cache(weather_location,l_list)

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


#https://stackoverflow.com/questions/48937900/round-time-to-nearest-hour-python#48938464
def hour_rounder(t):
    # Rounds to nearest hour by adding a timedelta hour if minute >= 30
    return (t.replace(second=0, microsecond=0, minute=0, hour=t.hour)
               +timedelta(hours=t.minute//30))
               
def verify_data(l_list):
    """ Ensuring the intervals in the sample are roughly equivalent """
    multiplier = 0
    count = 0
    l_list.sort()
    
    # The problem I am running into here is that if I have manually updated the 
    # weather/pressure readings, it's sometimes thrown the verification off.
    # So initial time is rounded to the closest hour, and then increment from there.
    # https://www.epoch101.com/Python
    
    scratch_x = "{0} {1}".format(l_list[0][1],l_list[0][2])
    dt_object = datetime.strptime(scratch_x, '%Y-%m-%d %H:%M')
    scratch_x = hour_rounder(dt_object)
    start_time = int(time.mktime(scratch_x.timetuple()))
    #start_time = l_list[0][0]
    print("{0}".format(start_time))
    
    
    
    o_list=[]
    while count < len(l_list):
        now_time = int(l_list[count][0])
        expected = int(start_time) + (int(interval) * int(multiplier))
        # Condition #1 - expected == actual +- tolerance
        if abs(now_time - expected) < int(tolerance): 
            o_list.append(l_list[multiplier])
            multiplier += 1
            count += 1                
        else:
            #Outside of tolerance conditions
            
            #Condition #2 - the actual time is outside of tolerance, and lower than expected (too early)
            ## In this case, we have extra readings
            ## So skip this reading, append the correction mark to the prior reading
            ### which is why row_count needs to be separate from multiplier 
            if now_time < expected:
                if the_silence == False:
                    print("Timestamp {0}: Outside of tolerance, too early, skipping.".format(l_list[count][0]))
                if o_list[-1][-1] != "‡":
                    o_list[-1].append("‡")
                count += 1
        
            #Condition #3 - the actual time is outside of tolerance, and higher than expected (missed a reading)
            ## Does this ever match?
            ## That is:
            ### Increment expected until it hits (or exceeds) actual
            #### Does this reading actually match at any point?
            ##### If so, how many missed readings were there?  
            #TODO - this is not working correctly and giving too many missed readings.
            elif now_time > expected:
                if the_silence == False:
                    print("Timestamp {0}: Out of tolerance, too late.".format(l_list[count][0]))

                matched = False
                while now_time > expected and matched is False:
                    multiplier += 1
                    expected = int(start_time) + (int(interval) * int(multiplier))
                    if abs(now_time - expected) < int(tolerance): 
                        if the_silence == False:
                            print("Found match after {0} rows.".format(multiplier - count))
                        for x in range(count, multiplier - 1):
                            ts = datetime.datetime.fromtimestamp(start_time + (x * interval))
                            datestring = ts.strftime("%Y-%m-%d")
                            timestring = ts.strftime("%H:%M")
                            fakerow = [ str(start_time + (x * interval)),
                                    datestring,timestring,
                                    l_list[count-1][3],l_list[count-1][4],"†" ]
                            o_list.append(fakerow)
                        o_list.append(l_list[count])
                        count = multiplier
                        matched = True

    o_list.sort
    return o_list

def calculate_data(l_list):
    """ Calculating the data for the passed in dataset.  """

    if the_silence == False:
        print("Performing calculations...")
    count = 0
    print("{0}".format(len(l_list)))    
    while count < len(l_list):
        autohealed = " "
        if "‡" in l_list[count]:
            autohealed = autohealed + "‡"
        if "†" in l_list[count]:
            autohealed = autohealed + "†"
        
        # original calculations, put in position 5 of current row
        subcounter = 1
        signed_calc = [] 

        curr_row_value = l_list[count][4]
        while subcounter < count:
            prior_row_value = l_list[count - subcounter][4]
            signed_calc.append(int(curr_row_value) - int(prior_row_value))
            subcounter += 1
        while subcounter < 64:  # padding the rest 
            signed_calc.append(int("0")) 
            subcounter += 1
        l_list[count].insert(5,tuple(signed_calc)) 
        # deriving walking calculations from what we just did.
        walk_calc = []
        subcounter = 1
        while subcounter < 64:
            walk_calc.append(max(signed_calc[:subcounter]) - min(signed_calc[:subcounter]))
            subcounter += 1
            
        l_list[count].insert(6,tuple(walk_calc)) 
        l_list[count].insert(7,autohealed)
        count += 1
    print("sd {0}".format(len(l_list)))
    return l_list


def display_data(l_list):
    """ Print out the selected data to STDOUT """
    
    row = 0
    while row < len(l_list):
        print ("{0}".format(l_list[row]))
        row += 1


def get_range(l_list,l_position):
    """ Obtaining range of points in list (optionally at position inside of list)"""

    l_range = 0
    l_abs_range = 0
    l_max = 0
    l_min = 0
    ll_list = []
    counter = 0 
    
    if l_position == None:
        ll_list = l_list
    else:
        while counter < len(l_list):
            ll_list.append(l_list[counter][l_position])
            counter += 1

    for l_object in ll_list:
        if int(max(l_object)) > l_max:
            l_max = int(max(l_object))
        if int(min(l_object)) > l_max:
            l_max = int(max(l_object))
        if (l_max - l_min) > l_range:
            l_range = (l_max - l_min)
        if abs(l_max - l_min) > l_abs_range:
            l_abs_range = abs(l_max - l_min)
        
    return l_range,l_abs_range


def data_for_line_graph(l_times):
    """ Arrange line graph data and scale appropriately for size of chart  """

    my_points = []
    count = 0
    while count < len(l_times):
        my_points.append(int(l_times[count][4]))
        count += 1
       
    my_range = max(my_points) - min(my_points)
    my_scalar = 0
    while (450 - (my_range * my_scalar)) > 1:
        my_scalar += 1
        
    my_max=max(my_points)
    my_min=min(my_points)
    my_plot = []
    
    count = 0
    while count < len(my_points):
        point=(512-(abs(my_max - my_points[count]) * my_scalar)) 
        my_plot.append(tuple([point,(count*8)]))  
        count += 1

    return my_plot, my_max, my_min, my_range


def make_chart(l_list,type_of_chart,scheme,line_graph,output_stem,user_font):
    """ Create charts of a passed in slice of the dataset """
    
    
    #look for font in cwd
    
    if user_font != None:
        font_path = Path(user_font)
        if font_path.is_file() == True:
            font_filename = str(font_path)  # this may be superflous
            font = ImageFont.truetype(font=font_filename, size=7)
            font2 = ImageFont.truetype(font=font_filename, size=15)
    else:
        try:
            font = ImageFont.truetype("Arial", size=7)
            font2 = ImageFont.truetype("Arial", size=15)
        except OSError:
            font = ImageFont.load_default()
            font2 = ImageFont.load_default()
            
    my_image = Image.new('RGB', (552, (len(l_list) * 8)), (125, 125, 125))
    draw = ImageDraw.Draw(my_image)
    duration_string = "From: {0} @ {1} until {2} @ {3}".format(l_list[0][1],l_list[0][2],l_list[-1][1],l_list[-1][2])
    if type_of_chart.find("walk") != -1:
        chart_range, chart_abs_range = get_range(l_list,5)
    else:
        chart_range, chart_abs_range = get_range(l_list,6)
    
    if scheme == None:
        scheme = "auto"
        
    if scheme == "auto":  # There is probably a more clever way to do this, but...
        if chart_range < 12 and chart_abs_range < 24:
            scheme = "autoscale1"
        elif chart_range < 18 and chart_abs_range < 36:
            scheme = "autoscale2"           
        elif chart_range < 24 and chart_abs_range < 48:            
            scheme = "autoscale3"
        elif chart_range < 36 and chart_abs_range < 72:
            scheme = "autoscale4"           
        elif chart_range < 48 and chart_abs_range < 96:
            scheme = "autoscale5"

    if the_silence == False: 
        print ("Creating chart with {0} colorscheme...".format(scheme))
    
    y = 0
    for row in l_list:
        if type_of_chart.find("walk") != -1: # doing it this way means one variable
            the_index = 5                    # four possible conditions
        else:
            the_index = 6
            
        x_counter = 0        
        for this_value in row[the_index]:
            if type_of_chart.find("abs") != -1:       ### why am I not seeing this?
                this_value = abs(this_value)
            else:
                this_value = int(this_value)
               
            if scheme == "wide":
                fill_color = _my_colors_wide.get(this_value, (254, 255, 255))
            elif scheme == "superwide":
                fill_color = _my_colors_superwide.get(this_value, (255, 255, 255))
            elif scheme == "alt":
                fill_color = _my_colors_alt.get(this_value, (255, 255, 255))
            elif scheme == "original":
                fill_color = _my_colors_original.get(this_value, (255, 255, 255))
            elif scheme == "autoscale1":
                fill_color = _my_colors_autoscale1.get(this_value, (255, 255, 255))
            elif scheme == "autoscale2":                    
                fill_color = _my_colors_autoscale2.get(this_value, (255, 255, 255))
            elif scheme == "autoscale3":                    
                fill_color = _my_colors_autoscale3.get(this_value, (255, 255, 255))
            elif scheme == "autoscale4":                    
                fill_color = _my_colors_autoscale4.get(this_value, (255, 255, 255))
            elif scheme == "autoscale5":                                                                                
                fill_color = _my_colors_autoscale5.get(this_value, (255, 255, 255))
            else:
                fill_color = _my_colors_original.get(this_value, (255, 255, 255))
            x = (x_counter * 8) + 40
            draw.rectangle((x, y, x + 8, y + 8), fill=(fill_color) , outline=None)
            x_counter += 1
        timestring = str(row[2]) + str(row[7])  # autoheal marker    
        draw.text((5, y), str(timestring), fill="white", font=font)
        y += 8
# now is for linegraph overlay
    if line_graph == True:
        if the_silence == False:
            print ("Creating line graph...")
        
        points, val_max, val_min, val_range = data_for_line_graph(l_list)
        draw.line(points, width=5, fill="green", joint="curve")  
        range_string = "Max: {0} Min: {1} Range: {2}".format(val_max,val_min,val_range) 
        draw.text((100, 45), range_string, fill="white", font=font2, stroke_width=2, stroke_fill="black")

    draw.text((100, 25), duration_string, fill="white", font=font2, stroke_width=2, stroke_fill="black")

    if type_of_chart.find("abs") != -1:
        fn = "{0}_abs.png".format(output_stem)
    elif type_of_chart.find("walk") != -1:    
        fn = "{0}_walk.png".format(output_stem)
    else: 
        fn = "{0}_signed.png".format(output_stem)
        
    my_image.save(fn)


def choose_date_slice(l_list,start_date,end_date):
    """ Find start and end point of date in list """
    first_slice = 0
    last_slice = len(l_list)
    l_list.sort()
    if start_date != None:
        count=0
        while count < len(l_list):
            if l_list[count][1] == start_date:
                first_slice=count
                count=len(l_list)
            count += 1
            
    if end_date != None:
        l_list.reverse()
        count=0
        while count < len(l_list):
            if l_list[count][1] == end_date:
                last_slice=len(l_list) - count 
                count=len(l_list)
            count+=1
        l_list.reverse()
    return first_slice,last_slice


def main(ini):
    """ Pull in configurations, main control function """

    global the_silence
    global cache_overwrite 
    global to_verify   
    global tolerance
    global interval
    
    config = configparser.ConfigParser()
    try:
        config.read(ini_file)
        sections=config.sections()
        api_key = config['DEFAULT']['owm_api']
        weather_location = str.lower(config['DEFAULT']['city_id'])
    except FileNotFoundError: 
        api_key = None
        weather_location = None

    parser = argparse.ArgumentParser(usage=__doc__)
    # generic arguments
    parser.add_argument("-q", "--quiet", dest="quiet",action='store_true', default=False, help="Minimize output to STDOUT/STDERR")
    #adding arguments
    parser.add_argument("-a", "--add-records", type=int, help="Number of records to add from input files", default=0, action='store',dest='num_input')
    parser.add_argument("-r", "--retrieve-current", dest="get_data",action='store_true', default=False, help="Get reading from OpenWeatherMap")    
    parser.add_argument("-o", "--overwrite-cache", dest="cache_overwrite",action='store_true', default=False, help="Overwrite cache data when importing new data.")
    # choosing arguments
    parser.add_argument('-B', '--bout-here', action='store', dest='bout_here',help="Where to output/input weather location from.")    
    parser.add_argument("-b", "--begin-date", dest="start_date", action='store', default=None,help="Provide the start date for chart or calculation data.")
    parser.add_argument("-e", "--end-date", dest="end_date", action='store', default=None,help="Provide the end date for chart or calculation data; optional, only makes sense with --begin-date.")
    parser.add_argument("-d", "--display-records", type=int, help="number of records back to display", default=None,action='store',dest='num_output')
    parser.add_argument("-s", "--scheme", dest="scheme",action='store', default=None, help="Color scheme - default, wide, alt, original")
    # verification arguments
    parser.add_argument('-v', '--verify', dest='to_verify', action='store_true', default=False,help="Verify interval ranges")
    parser.add_argument('-t', '--tolerance', action='store',dest='tolerance', default="300",help="Acceptable range in seconds, only makes sense with -v")
    parser.add_argument('-i', '--interval', action='store',dest='interval', default="1800",help="Expected interval in seconds, only makes sense with -v")    
    # output arguments
    parser.add_argument('-F', '--font', action='store',dest='font', default=None,help="Path to TTF/OTF font if desired")
    parser.add_argument('-f', '--file', action='store',dest='fn_stem', default="out",help="Stem for output filename, defaults to out_[abs|signed].png")
    parser.add_argument("-w", "--walk_about", dest="walkabout",action='store_true', default=False, help="Modify walking chart by distance from present")
    # type of output arguments
    parser.add_argument("-D", "--show-data", dest="showdata",action='store_true', default=False, help="Show data of range on stdout")
    parser.add_argument("-L", "--line-graph", dest="linegraph",action='store_true', default=False, help="Produce line graph overlay")
    parser.add_argument("-S", "--signed-values", dest="signval",action='store_true', default=False, help="Produce signed value chart")
    parser.add_argument("-A", "--abs-values", dest="absval",action='store_true', default=False, help="Produce abs value chart")
    parser.add_argument("-W", "--walking", dest="walking",action='store_true', default=False, help="Produce walking value chart")
    args = parser.parse_args()

    if args.quiet is True:
        the_silence = True
    if args.cache_overwrite is True:
        cache_overwrite = True
    if args.to_verify is True:
        to_verify = True
    tolerance = args.tolerance
    interval = args.interval
    if args.bout_here != None:
        weather_location = args.bout_here
    if args.num_output is None:
        num_output = 64
    else:
        num_output = args.num_output
        
    if args.num_input != 0:
        # Add in new raw data
        for rawfile in list(cur_path.joinpath(cur_path.cwd(),'raw').iterdir()):    
            if the_silence == False:
                print("Reading in {0}".format(rawfile))
            read_in_file(rawfile,args.num_input)

    if args.get_data == True:
        if weather_location is None:
            print ("Location not set in ini or commandline")
        else:
            if the_silence == False:
                print("Obtaining new data for {0}".format(weather_location))
            l_list=match_cache(weather_location)
            base_url = "http://api.openweathermap.org/data/2.5/weather?id="
            final_url = base_url + weather_location + "&units=metric&appid=" + api_key
            weather_data = requests.get(final_url).json()
            now_metric = weather_data['main']['pressure']
            now_imperial=round(now_metric/33.863886666667,2)
            ts = round(datetime.datetime.timestamp(datetime.datetime.utcnow()))
            datestring = ts.strftime("%Y-%m-%d")
            timestring = ts.strftime("%H:%M")
            addrow = [ str(ts),datestring,timestring,now_imperial,now_metric ]
            l_list.append(addrow)
            write_cache(weather_location,l_list)
    
    type_of_chart = ""
    if args.showdata == True:
        type_of_chart = type_of_chart + "show"
    if args.signval == True:
        type_of_chart = type_of_chart + "sign"    
    if args.absval == True:
        type_of_chart = type_of_chart + "abs"        
    if args.walking == True:
        type_of_chart = type_of_chart + "walk"
    

    if len(type_of_chart) > 0:  
        if weather_location is not None:
            l_list = match_cache(weather_location)
        else:
            print ("Location not set in ini or commandline")
            exit()
        
        # Selection of data to calculate and display
        if args.start_date != None:
            display_start,display_end = choose_date_slice(l_list,args.start_date,args.end_date)    
        elif args.num_output != None:
            display_start = (len(l_list) - num_output)
            display_end = len(l_list)

        # Adjustment of data selection so that calculations go through properly
        calc_start_adjust = 1
        while calc_start_adjust < 64:
            try:
                scratch = l_list[display_start - calc_start_adjust][0]
            except IndexError:
                continue
            else:
                calc_start_adjust += 1
        
        if to_verify == True:
            l_list = verify_data(l_list[(display_start - calc_start_adjust):display_end])
        
        l_list=calculate_data(l_list[(display_start - calc_start_adjust):display_end])
        l_list=l_list[calc_start_adjust:len(l_list)]
        
        if type_of_chart.find("show") != -1: 
            display_data(l_list)
        if type_of_chart.find("abs") != -1: 
            make_chart(l_list,"abs",args.scheme,args.linegraph,args.fn_stem,args.font)
        if type_of_chart.find("sign") != -1: 
            make_chart(l_list,"sign",args.scheme,args.linegraph,args.fn_stem,args.font)
        if type_of_chart.find("walk") != -1: 
            make_chart(l_list,"walk",args.scheme,args.linegraph,args.fn_stem,args.font)

    else:
        exit()

if __name__ == '__main__':
    main(ini_file)
else:
    print("barometers loaded as a module")
