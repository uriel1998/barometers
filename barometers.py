#! /usr/bin/env python3

import pathlib
import pickle, sys, string, argparse
from PIL import Image, ImageDraw

# TODO: Max entries as passed variable
# TODO: select time period as passed interval
# TODO: Graph over chart?  https://www.blog.pythonlibrary.org/2021/02/23/drawing-shapes-on-images-with-python-and-pillow/
# TODO: Ensure range for graph not > 64


# Note on the data structure for pressures
# pressures = epoch,date,time,pressure imperial,pressure metric, calc[64]


pressures = []
cur_path = pathlib.Path()
my_colors = { -16:(255, 255, 255),-15:(255, 224, 224),-14:(255, 192, 192), 
    -13:(255, 160, 160),-12:(255, 128, 128),-11:(255, 96, 96),  
    -10:(255, 64, 64),-9:(255, 32, 32),-8:(255, 0, 0),-7:(224, 0, 0), 
    -6:(192, 0, 0),-5:(160, 0, 0),-4:(128, 0, 0),-3:(96, 0, 0), 
    -2:(64, 0, 0),-1:(32, 0, 0),0 : (0, 0, 0),15:(255,236,224),14:(255,216,192),
    13:(255,196,160),12:(255,176,128),11:(255,156,96),10:(255,136,64),
    9:(255,116,32),8:(255,96,0),7:(224,84,0),6:(192,72,0),5:(160,60,0),
    4:(128,48,0),3:(96,36,0),2:(64,24,0),1:(32,12,0)}



def read_in_file(in_file):
    """ Reading in the new file into the pressures data structure """ 
    global pressures
    
    
    with open(in_file, 'r') as infile:
        for row in infile:            
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
                        if c1[1] == list_to_add[1]:
                            if c1[2] == list_to_add[2]:
                                dupe = 1

                    if dupe != 1:
                        #print("adding {0} {1} {2}".format(list_to_add[0],list_to_add[1],list_to_add[2]))
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

    infile.close

def perform_calculations(row):
    """ Calculate the values for calc_signed for the specified row in pressures array """
    global pressures
    now = pressures[row][4]  # only need this once
    signed_calc = []  # maybe?
    count = 0
    if len(pressures[row]) == 5:   # no tuple in that row
        while count < 64:
            then = pressures[int(row) - int(count)][4]
            signed_calc.append(int(now) - int(then))
            count += 1

        pressures[row].append(tuple(signed_calc))  #This SHOULD work?
    
def loop_calculations():
    """ Control loop for calculations """
    global pressures
    count = 0
    while count < len(pressures):
        perform_calculations(count)
        count += 1

def show_calculations(num_output):
    """ Display the tuples for the requested number of intervals back """
    global pressures
    
    last = len(pressures)
    print("{0}".format(last))
    count = last - num_output
    while count < len(pressures):
        #print ("{0} @ {1} : {2}".format(pressures[count][1],pressures[count][2],pressures[count][5]))
        count += 1

def data_for_my_graph(num_output=64):
    """ Draw the line graph over the chart """
    global pressures

    my_points = []
    last = len(pressures)
    count = last - num_output
    while count < len(pressures):
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
    return my_plot

def match_cache(weather_location):
    """ See if a pickled cache file exists for the rawfile we're reading in """
    global pressures
    global cache_file
    
    cache_file = cur_path.joinpath(cur_path.cwd(),'cache',weather_location)
    try:
        file = open(cache_file, 'rb')
        print("Reading in cache for location {0}".format(weather_location))
        pressures = pickle.load(file)
        file.close()
    except FileNotFoundError:
        print("No cache exists for location {0}".format(cache_file))   

def make_chart(num_output = 64):
    """ Create output graphic chart with signed data """
    global pressures
    global my_colors
    
    
    my_image = Image.new('RGB', (552, (num_output * 8)), (125, 125, 125))
    draw = ImageDraw.Draw(my_image)
    last = len(pressures)
    count = last - num_output
    y = 0
    while count < len(pressures):  # row count        
        x_counter = 0
        while x_counter < 64:
            fill_color = my_colors.get(pressures[count][5][x_counter], (255, 255, 255))           
            x = (x_counter * 8) + 49
            #print ("x = {0} y = {1} color = {2}".format(x,y,fill_color))
            draw.rectangle((x, y, x + 8, y + 8), fill=(fill_color) , outline=None)
            x_counter += 1

        draw.text((5, y), str(pressures[count][2]), fill=(255,255,0))
        count += 1
        y += 8
    
    points = data_for_my_graph(num_output)
    draw.line(points, width=5, fill="green", joint="curve")    
    my_image.save('signed_color.png')


def make_abs_chart(num_output = 64):
    """ Create output graphic chart with ABS data """
    global pressures
    global my_colors
    
    my_image = Image.new('RGB', (552, (num_output * 8)), (125, 125, 125))
    draw = ImageDraw.Draw(my_image)
    last = len(pressures)
    count = last - num_output
    y = 0
    while count < len(pressures):  # row count        
        x_counter = 0
        while x_counter < 64:
            fill_color = my_colors.get(abs(int(pressures[count][5][x_counter])), (255, 255, 255))
            x = (x_counter * 8) + 40
            #print ("x = {0} y = {1} color = {2}".format(x,y,fill_color))
            draw.rectangle((x, y, x + 8, y + 8), fill=(fill_color) , outline=None)
            x_counter += 1
            
        draw.text((5, y), str(pressures[count][2]), fill=(255,255,0))
        count += 1
        y += 8
        
    points = data_for_my_graph(num_output)
    draw.line(points, width=5, fill="green", joint="curve")    
    my_image.save('abs_color.png')


def write_cache():
    """ Writing pickled info to cache """
    global pressures
    global cache_file
    
    
    try:
        cache_file.unlink()
    except FileNotFoundError:
        print ("Creating new cache {0}".format(cache_file))
    
    file = open(cache_file, 'wb')
    pickle.dump(pressures,file)
    file.close()
    
def main():
    """ main loop """
    
    parser = argparse.ArgumentParser(usage=__doc__)
    parser.add_argument("num", nargs='*')
    
    parser.add_argument("-t", "--test", dest="test",
    action='store_true', default=False,
    help="Test mode: reads from stdin")
    args = parser.parse_args()
    if args.test:
        test()
    else:
        for rawfile in list(cur_path.joinpath(cur_path.cwd(),'raw').iterdir()):    

            weather_location = str(rawfile.name.split('_',1)[0])
            match_cache(weather_location)
            print("Reading in {0}".format(rawfile))
            read_in_file(rawfile)

        pressures.sort() # because key 0 is epochtime

        loop_calculations()
        write_cache()
        show_calculations(64)
        make_chart(256)
        make_abs_chart(64)


if __name__ == '__main__':
    main()
else:
    print("barometers loaded as a module")

