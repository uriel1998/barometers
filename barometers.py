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
tolerance = 0
interval = 0 
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
    if to_verify == True:
        l_list = verify_data(l_list)
        
        def check_intervals(input_list, start, last, num_output = 64, interval = 1800, tolerance = 300):
    write_cache(weather_location,l_list)
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

def verify_data(l_list)
    """ Ensuring the intervals in the sample are roughly equivalent """
    multiplier = 0
    l_list.sort()
    start_time = l_list[0][0]
    
    while multiplier < len(l_list):
        if multiplier > 0:  # first one goes through
            now_time = int(input_list[multiplier][0])
            expected = (start_time + (interval * multiplier)
            if (abs(now_time - expected)) < tolerance: 
                o_list.append(l_list[multiplier])
                multiplier += 1                
            else:
                if the_silence == False:
                    print("Error found with timestamp {0}".format(l_list[count][0]))
                if now_time > expected:     # there are missed readings. what we 
                                            # have is actually, start_time + (interval * (multiplier + 4))
                                            # So we are changing *expected time* until it matches actual time.
                    submultiplier = multiplier # last accepted multiplier
                    found_match = False
                    while now_time > l_list[sub_multiplier][0]:   # so it aborts when hits current time
                        sub_expected_time=(start_time + (interval * sub_multiplier))
                        if (abs(now_time - sub_expected_time)) > tolerance:  # found where missed reading stops and is within tolerance
                            sub_multiplier += 1
                            #check for end of list, and continue loop
                        else
                            found_match = True
                            if the_silence == False:
                                print("Detected {0} missing rows; inserting duplicates of last approved row".format(sub_multiplier))
                            # insert fake rows
                            #TODO - make sure this doesn't overcount by 1
                            for add_count in range (multiplier,sub_multiplier):
                                ts = datetime.datetime.fromtimestamp(start_time + ((add_count + count) * interval))
                                datestring = ts.strftime("%Y-%m-%d")
                                timestring = ts.strftime("%H:%M")
                                fakerow = [ str(start_time + ((add_count + count) * interval)),
                                        datestring,timestring,
                                        l_list[count-1][3],l_list[count-1][4],"†" ]
                                o_list.append(fakerow)
                            o_list.append(l_list[multiplier])
                            multiplier = sub_multiplier + 1 # getting everything even
                elif now_time < expected:     # current reading is too early but out of tolerance; 
                                              # is there a good reading ahead of us? So we are incrementing the *row* until we find a good one
                    submultiplier = multiplier
                    submultiplier +=1
                    while submultiplier < len(l_list):
                        try:
                            test_time=int(input_list[submultiplier][0])
                        except IndexError:
                            continue
                        
                        if abs(expected - test_time) < tolerance:
                            skipped_rows = (submultiplier - multiplier)
                            if the_silence = False:
                                print("Found {0} extra rows before in-tolerance data found.".format(skipped_rows))
                            multiplier=submultiplier
                            l.list[multiplier].append("‡")
                            o_list.append(l_list[multiplier])
            multiplier += 1
        else         
            # first row goes through
            o_list.append(l_list[multiplier])
            multiplier += 1
    o_list.sort
    return o_list

def calculate_data(l_list):
    """ Calculating the data for the passed in dataset.  """
    """ The dataset should have 64 prior rows, if possible """
    
    if the_silence = False:
        print("Performing calculations...")
    count = 0
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
        l_list[count].insert(5,tuple(signed_calc))  

        # deriving walking calculations from what we just did.
        walk_calc = []
        subcounter = 1
        while subcounter < 64:
            walk_calc.append = max(signed_calc[:subcount]) - min(signed_calc[:subcount])
            subcounter += 1
            
        l_list[count].insert(6,tuple(walk_calc)) 
        l_list[count].insert(7,autohealed)
        count += 1
    return l_list


def display_data(l_list)
    """ Print out the selected data to STDOUT """
    
    while row in l_list:
        print ("{0}".format(l_list[row]))


def get_range(l_list,l_position):
    """ Obtaining range of points in list (optionally at position inside of list)"""

    l_range = 0
    l_arange = 0
    l_max = 0
    l_min = 0
    ll_list = []

    if l_position is not None:
        for row in l_list:
            ll_list.append(l_list[l_position])
    else:
        ll_list = l_list

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


def make_chart(l_list,type_of_chart,line_graph,output_stem,user_font)
    """ Create charts of a passed in slice of the dataset """
    
    #look for font in cwd
    font_path = Path(user_font)

    if font_path.is_file() = True:
        font_filename = str(font_path)  # this may be superflous
        font = ImageFont.truetype(font=font_filename, size=7)
        font2 = ImageFont.truetype(font=font_filename, size=15)
    else
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
    

##### make charts
##### make line chart

main(ini):
""" Pull in configurations, main control function """

    global the_silence
    global cache_overwrite 
    global to_verify   
    global tolerance
    global interval
    
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

    if args.quiet is not True:
        the_silence = False
    if args.cache_overwrite is not True:
        cache_overwrite = False
    if args.verify = is not True:
        to_verify = False
    tolerance = args.tolerance
    interval = args.interval
        
    # Add in new raw data
    for rawfile in list(cur_path.joinpath(cur_path.cwd(),'raw').iterdir()):    
        if the_silence == False:
            print("Reading in {0}".format(rawfile))
        l_list=read_in_file(format(rawfile),args.num_input)

# passing lists (or slices of lists) is all done from here, as 

if __name__ == '__main__':
    main(ini)
else:
    print("barometers loaded as a module")
