#! /usr/bin/env python3

import pathlib
import linecache
import pickle, sys, string, argparse, datetime
from PIL import Image, ImageDraw, ImageFont


pressures = []
cur_path = pathlib.Path()

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



def read_in_file(in_file,num_input=256):
    """ Reading in the new file into the pressures data structure """ 
    global pressures
    
    with open(in_file) as f:
        rowcount = sum(1 for line in f)

    if rowcount <= num_input:
        count = 0
        num_input = rowcount
    else:
        count = rowcount - num_input
    
    while count < rowcount:
        count += 1
        row = linecache.getline(str(in_file), count)
        row = row.replace("@", ",")
        row = row.strip()
        if row.find(",,") != -1:
            continue
        else: 
            # epochtime
            # Oh, yeah, we didn't want units did we.
            list_to_add = row.split(',',7)
            if list_to_add[0] == "epoch":
                continue
            else:
                dupe = 0
                for c1 in pressures:                   
                    if c1[1] == list_to_add[1] and c1[2] == list_to_add[2]:
                        dupe = 1
                
                if dupe != 1:
                    # print("adding {0} {1} {2}".format(list_to_add[0],list_to_add[1],list_to_add[2]))
                    # taking out units if they exist
                    try:
                        list_to_add.remove("hPa")
                    except ValueError:
                        print("already clean")
                    
                    try: 
                        list_to_add.remove("in")
                    except ValueError:
                        print("already clean")
                                
                    pressures.append(list_to_add)   #needs to be a list because I will use positionals for calculations later
    linecache.clearcache()


def loop_calculations(input_list,make_sure_of_calc,to_verify, interval = 1800, tolerance = 300):
    """ Control loop for calculations """

    count = 0
    if to_verify == True:
        print("{0}".format(len(input_list)))
        input_list, rejected = check_intervals(input_list,0,len(input_list),len(input_list),interval,tolerance)
        if rejected > 0:  
            print ("{0} rejected times found in selected set.".format(rejected))
            if make_sure_of_calc == False:
                print ("You *WILL* have erroneous output if you do not use the verify functions.")
    
    if make_sure_of_calc == True:  # delete all the tuples in our current set so they're recalculated
        print ("Recalculating for selected range...")
        count = 0
        while count < len(input_list):
            try:
                bob=(len(input_list[count]) == 6)
            except IndexError:
                print ("{0} : {1}".format(count,len(input_list)))
            else:
                del (input_list[count][5])
                count += 1
            
            
### TODO OH FFS - Because I'm now recalculating only a subset, I need priors 
### for the FIRST INPUTTED ROWS so that they have calculations
        
    row = 0 
    while row < len(input_list):
        now = input_list[row][4]  # only need this once
        signed_calc = []  # maybe?
        count = 0
        try:
            bob=(len(input_list[row]) == 6)
        except IndexError:
            print ("{0} : {1}".format(count,len(input_list)))
        else:
            if len(input_list[row]) == 5:   # no tuple in that row
                print ("{0}".format(input_list[row]))
                while count < 64:
                    then = input_list[int(row) - int(count)][4]
                    signed_calc.append(int(now) - int(then))
                    count += 1

                input_list[row].append(tuple(signed_calc))  #This SHOULD work?
        row += 1
    
    return input_list

def show_calculations(start = None, num_output = 64,last = len(pressures)):
    """ Display the tuples for the requested number of intervals back """
    global pressures
    
    if not start:
        start = last - num_output
        
    if start < 0:
        count = 0
    else:
        count = start 

    while count < len(pressures):
        print ("{0} {1} @ {2} : {3}".format(pressures[count][0],pressures[count][1],pressures[count][2],pressures[count][5]))
        count += 1

def check_intervals(input_list, start, last, num_output = 64, interval = 1800, tolerance = 300):
    """ Ensuring the intervals in the sample are roughly equivalent """
    """ If auto interval, it should have None passed to it, otherwise default of 1800 sec """   

    my_times = []
    rejected = 0
    skipped = 0
    
    if not start:
        start = last - int(num_output)
        
    if start < 0:
        count = 0
    else:
        count = start 
 
    if not interval:
        interval = (int(input_list[count + 1][0]) - int(input_list[count][0]))
    else:
        interval = int(interval)
    tolerance = int(tolerance)
    
    my_multiplier = 0
    
    start_time = int(input_list[start][0])
    while count < last:  
        now_time = int(input_list[count][0])
        
        if my_multiplier > 0:
            # first one always goes through
            finished = False
            da_difference = (start_time + (my_multiplier * interval)) - now_time
            if abs(da_difference) < tolerance:  
                my_times.append(input_list[count])  # appending that whole row
                my_multiplier += 1
                finished = True
            else:
                print ("Timestamp {0} out of tolerance (off by {1})".format(now_time,da_difference))               
                if da_difference < 0: # looking for missed readings
                    print ("Checking for missing readings...")
                    subcount = 1
                    while da_difference < 0: 
                        da_difference = (start_time + (my_multiplier + subcount) * interval) - now_time
                        if abs(da_difference) < tolerance:
                            print ("Detected {0} missing intervals before recovery.".format(subcount))
                            print ("Inserting {0} duplicate(s) of last row sans calculations for placeholder(s).".format(subcount))
                            subbycount = 0
                            while subbycount < subcount:
                                ts = datetime.datetime.fromtimestamp(now_time + (subbycount * interval))
                                datestring = ts.strftime("%Y-%m-%d")
                                timestring = ts.strftime("%H:%M")
                                
                                fakerow = [ str(start_time + (subbycount * interval)),
                                        datestring,timestring,
                                        input_list[count-1][3],input_list[count-1][4] ]
                                my_times.append(fakerow)  
                                subbycount += 1
                            my_times.append(input_list[count])  # appending current row in next spot
                            finished = True
                            rejected += subbycount
                            my_multiplier += subcount + 1 # incrementing multiplier by subcount
                            # done with second dia
                        subcount += 1    
                            
                            
                if finished == False:
                    # this should be a loop tooooooooo
                    if count + 1 < last: 
                        print ("Checking for excess readings...") # third dia
                        da_difference = abs((start_time + (my_multiplier * (interval))) - int(input_list[count+1][0]))
                        if da_difference < tolerance:
                            print ("Excess reading detected, next reading is for this interval. Skipping {0}.".format(now_time))
                            rejected += 1
                            # do not increment multiplier, let count increment and catch up.
                        else:
                            # fourth dia
                            da_difference = abs((start_time + (my_multiplier * (interval+1))) - int(input_list[count+1][0]))
                            if da_difference < tolerance:
                                print ("Next record at correct interval; skipping {1}.".format(da_difference2,now_time))
                                multiplier += 1
                                rejected += 1
                                # This one is just wack, but the next one is okay.
                            else:
                                print ("Next record is also out of tolerance by {0};".format(da_difference))
                                print ("Please examine your dataset around {0}.".format(now_time))
                                # The next one is fucky too, and that's a problem with the dataset then
                                # the multipliers get out of whack here
                                rejected += 1
                
                    else:
                        print ("Last record out of tolerance as well.")
                        rejected += 1
                
            
        else:
            # first row is always appended
            my_times.append(input_list[count])  # is good
            my_multiplier += 1

        count += 1         
    return my_times, rejected


def data_for_my_graph(start, num_output=64,last = len(pressures)):
    """ Draw the line graph over the chart """
    global pressures

    my_points = []

    if not start:
        start = last - num_output
        
    if start < 0:
        count = 0
    else:
        count = start 
 
    while count < last:
        my_points.append(int(pressures[count][4]))
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

def match_cache(weather_location):
    """ See if a pickled cache file exists for the rawfile we're reading in """
    global pressures

    cache_file = cur_path.joinpath(cur_path.cwd(),'cache',weather_location)
    cache_filename = str(cur_path.joinpath(cur_path.cwd(),'cache',weather_location))
    try:
        file = open(cache_filename, 'rb')
        print("Reading in cache for location {0}".format(weather_location))
        pressures = pickle.load(file)
        file.close()
    except FileNotFoundError:
        print("No cache exists for location {0}".format(cache_file))   

def make_chart(start, last = len(pressures), num_output = 64,linegraph = False,scheme = None,is_abs = None,stem = "out", my_verify = False, my_interval = 1800, my_tolerance = 300):
    """ Create output graphic chart data """
    global pressures
    global cur_path
    
    font = ImageFont.truetype("Arial", size=7)
    font2 = ImageFont.truetype("Arial", size=15)
    my_image = Image.new('RGB', (552, (num_output * 8)), (125, 125, 125))
    draw = ImageDraw.Draw(my_image)
    
    if not start:
        start = last - num_output
        
    if start < 0:
        start = 0
        count = 0
    else:
        count = start 
    count = last - num_output
    y = 0
    da_duration = "From: {0} @ {1} until {2} @ {3}".format(pressures[start][1],pressures[start][2],pressures[last-1][1],pressures[last-1][2])



###TODO:  Use this bit with show_calculations to help me narrow this down where it's going wrong...
###Almost certainly the verify code - perhaps I need to add one more in the addition part??

    # substituting in the check_intervals to give us a list to scroll through instead of pressures
    da_times, da_rejected = check_intervals(pressures, start, last, num_output, my_interval, my_tolerance)
    print ("{0} Accepted : {1} Rejected".format(len(da_times),da_rejected))
    if da_rejected > 0:
        print ("Recalculation needed on this subset; performing now.")
        da_times = loop_calculations(da_times,True,False)
        
    count = 0 # reassigning it since da_times is now the count
    while count < len(da_times):  # row count    
        x_counter = 0
        while x_counter < 64:
            if is_abs:
                if scheme == "wide":
                    fill_color = _my_colors_wide.get(abs(da_times[count][5][x_counter]), (254, 255, 255))
                elif scheme == "alt":
                    fill_color = _my_colors_alt.get(abs(da_times[count][5][x_counter]), (255, 255, 255))
                elif scheme == "original":
                    fill_color = _my_colors_original.get(abs(da_times[count][5][x_counter]), (255, 255, 255))
                else:
                    fill_color = _my_colors.get(1-(abs(da_times[count][5][x_counter])), (255, 255, 255))           
            else:
                if scheme == "wide":
                    fill_color = _my_colors_wide.get(da_times[count][5][x_counter], (254, 255, 255))
                elif scheme == "alt":
                    fill_color = _my_colors_alt.get(da_times[count][5][x_counter], (255, 255, 255))
                elif scheme == "original":
                    fill_color = _my_colors_original.get(da_times[count][5][x_counter], (255, 255, 255))
                else:
                    fill_color = _my_colors.get(da_times[count][5][x_counter], (255, 255, 255))           
                

            x = (x_counter * 8) + 40
            draw.rectangle((x, y, x + 8, y + 8), fill=(fill_color) , outline=None)
            x_counter += 1
            draw.text((5, y), str(pressures[count][2]), fill="white", font=font)
        count += 1
        y += 8
        
    if linegraph == True:
        points, da_max, da_min, da_range = data_for_my_graph(start, num_output, last)
        draw.line(points, width=5, fill="green", joint="curve")  
        da_string = "Max: {0} Min: {1} Range: {2}".format(da_max,da_min,da_range) 
        draw.text((100, 45), da_string, fill="white", font=font2, stroke_width=2, stroke_fill="black")
    
    draw.text((100, 25), da_duration, fill="white", font=font2, stroke_width=2, stroke_fill="black")

    if is_abs:
        fn = "{0}_abs.png".format(stem)
    else: 
        fn = "{0}_signed.png".format(stem)
    my_image.save(fn)

def write_cache(weather_location):
    """ Writing pickled info to cache """
    global pressures

    cache_file = cur_path.joinpath(cur_path.cwd(),'cache',weather_location)
    cache_filename = str(cur_path.joinpath(cur_path.cwd(),'cache',weather_location))    
    try:
        cache_file.unlink()
    except FileNotFoundError:
        print ("Creating new cache {0}".format(cache_file))
    
    file = open(cache_filename, 'wb')
    pickle.dump(pressures,file)
    file.close()

    
def main():
    """ main loop """
    
    global pressures
    
    parser = argparse.ArgumentParser(usage=__doc__)
    parser.add_argument("-d", "--display-records", type=int, help="number of records back to show", default=None,action='store',dest='num_output')
    parser.add_argument("-a", "--add-records", type=int, help="max number of records to add from input files", default=256,action='store',dest='num_input')
    parser.add_argument("-c", "--show-calc", dest="showcalc",action='store_true', default=False, help="Show calc on stdout")
    parser.add_argument("-l", "--line-graph", dest="linegraph",action='store_true', default=False, help="Produce line graph overlay")
    parser.add_argument("-s", "--scheme", dest="scheme",action='store', default=None, help="Color scheme - default, wide, alt, original")
    parser.add_argument("-S", "--signed-values", dest="signval",action='store_true', default=False, help="Produce signed value chart")
    parser.add_argument("-A", "--abs-values", dest="absval",action='store_true', default=False, help="Produce abs value chart")
    parser.add_argument("-b", "--begin-date", dest="start_date", action='store', default=None,help="Provide the start date for chart or calculation data.")
    parser.add_argument("-e", "--end-date", dest="end_date", action='store', default=None,help="Provide the end date for chart or calculation data; optional, only makes sense with --begin-date.")
    parser.add_argument('-f', '--file', action='store',dest='fn_stem', default="out",help="Stem for output filename, defaults to out_[abs|signed].png")
    parser.add_argument('-v', '--verify', dest='to_verify', action='store_true', default=False,help="Verify interval ranges")
    parser.add_argument('-i', '--interval', action='store',dest='verify_interval', default="1800",help="Expected interval in seconds, only makes sense with -v")
    parser.add_argument('-t', '--tolerance', action='store',dest='tolerance_range', default="300",help="Acceptable range in seconds, only makes sense with -v")
    parser.add_argument('-m', '--make-sure', action='store_true', default=False,dest='make_sure_of_calc',help="Make sure calculations in range take into account verified interval ranges.")
    parser.add_argument('-B', '--bout-here', action='store', dest='bout_here',help="Where to output/input weather location from.")
    args = parser.parse_args()

    #print ('Media file is ', args.media_fn)
    #print ('Message is ', args.message)    
    
    for rawfile in list(cur_path.joinpath(cur_path.cwd(),'raw').iterdir()):    
        test_stem = str(rawfile.stem).strip()
        
        if test_stem.find("_") > 0:
            weather_location = test_stem.split('_',1)[0]
        else:
            weather_location = test_stem
        
        weather_location.strip()
        match_cache(weather_location)
        print("Reading in {0}".format(rawfile))
        read_in_file(format(rawfile),args.num_input)
        pressures.sort() # because key 0 is epochtime
        
        pressures = loop_calculations(pressures,args.make_sure_of_calc,args.to_verify,args.verify_interval,args.tolerance_range)
        write_cache(weather_location)
        print ("Wrote cache of {0} records for {1}.".format(len(pressures),weather_location))

    if args.bout_here is not None:
        weather_location = args.bout_here
        match_cache(weather_location)
        if args.to_verify == True:
            print ("Checking intervals...")
            check_intervals(pressures, 0, len(pressures), num_output = len(pressures), interval = args.verify_interval, tolerance = args.tolerance_range)
        
    print ("We have {0} records stored for {1},".format(len(pressures),weather_location))
    print ("From {0} at {1} to {2} at {3}".format(pressures[0][2],pressures[0][1],pressures[len(pressures)-1][2],pressures[len(pressures)-1][1]))
    # date selection
    # calculating both start point and num_output        
    if args.start_date:           
        start_output = 0
        while start_output < len(pressures):
            if pressures[start_output][1] == args.start_date:
                break
            start_output += 1
        
        if not args.end_date:
            # inclusive, effectively EOF thanks to next line
            end_date = str(datetime.date.today())

        if not args.num_output:
            end_date = args.end_date
            end_row = start_output
            while end_row < len(pressures):
                if pressures[end_row][1] == end_date:
                    while end_row < len(pressures):
                        if pressures[end_row][1] != end_date:
                            break
                        else:
                            end_row += 1
                end_row += 1
            num_output = end_row - start_output
        else:
            num_output = args.num_output
            end_row = start_output + num_output
    else: 
        if args.num_output: # defaults if date is not selected
            num_output = args.num_output 
        else:
            num_output = 64 # because there's default
        start_output = len(pressures) - num_output
        end_row = len(pressures)

    if end_row > len(pressures):
        end_row = len(pressures)
        
    if args.showcalc:
        show_calculations(start_output,end_row,num_output)
        
    if args.signval:
        make_chart(start_output,end_row,num_output,args.linegraph,args.scheme,is_abs=False,stem=args.fn_stem,my_verify=args.to_verify,my_interval=args.verify_interval,my_tolerance=args.tolerance_range)
        
    if args.absval:
        make_chart(start_output,end_row,num_output,args.linegraph,args.scheme,is_abs=True,stem=args.fn_stem,my_verify=args.to_verify,my_interval=args.verify_interval,my_tolerance=args.tolerance_range)

if __name__ == '__main__':
    main()
else:
    print("barometers loaded as a module")






