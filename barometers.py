import pathlib
import pickle
from PIL import Image, ImageDraw

# TODO:  Max entries as passed variable
# TODO: Graph over chart?  https://www.blog.pythonlibrary.org/2021/02/23/drawing-shapes-on-images-with-python-and-pillow/


pressures = []
cur_path = pathlib.Path()
my_colors = { -16:(255, 255, 255),-15:(255, 224, 224),-14:(255, 192, 192), 
    -13:(255, 160, 160),-12:(255, 128, 128),-11:(255, 96, 96),  
    -10:(255, 64, 64),-9:(255, 32, 32),-8:(255, 0, 0),-7:(224, 0, 0), 
    -6:(192, 0, 0),-5:(160, 0, 0),-4:(128, 0, 0),-3:(96, 0, 0), 
    -2:(64, 0, 0),-1:(32, 0, 0),0 : (0, 0, 0), 16:(255, 255, 255), 
    15:(224, 224, 255),14:(192, 192, 255),13:(160, 160, 255),
    12:(128, 128, 255),11:(96, 96, 255),10:(64, 64, 255),
    9:(32, 32, 255),8:(0, 0, 255),7:(0, 0, 224),6:(0, 0, 192),
    5:(0, 0, 160),4:(0, 0, 128),3:(0, 0, 96),2:(0, 0, 64),
    1:(0, 0, 32),0:(0, 0, 0)}



def read_in_file(in_file):
    """ Reading in the new file into the pressures data structure """ 
    global pressures
    
    
    with open(in_file, 'r') as infile:
        for row in infile:            # DO I NEED AN EXPLICIT READLINE HERE? I don't think so...
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
        print ("{0} @ {1} : {2}".format(pressures[count][1],pressures[count][2],pressures[count][5]))
        count += 1

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
    
    my_image = Image.new('RGB', (512, 512), (125, 125, 125))
    draw = ImageDraw.Draw(my_image)
    last = len(pressures)
    count = last - num_output
    y = 0
    while count < len(pressures):  # row count        
        x_counter = 0
        while x_counter < 64:
            fill_color = my_colors.get(pressures[count][5][x_counter], (255, 255, 255))           
            x = x_counter * 8
            print ("x = {0} y = {1} color = {2}".format(x,y,fill_color))
            draw.rectangle((y, x, y + 8, x + 8), fill=(fill_color) , outline=None)
            x_counter += 1

        count += 1
        y += 8
        
    my_image.save('signed_color.png')


def make_abs_chart(num_output = 64):
    """ Create output graphic chart with signed data """
    global pressures
    global my_colors
    
    my_image = Image.new('RGB', (512, 512), (125, 125, 125))
    draw = ImageDraw.Draw(my_image)
    last = len(pressures)
    count = last - num_output
    y = 0
    while count < len(pressures):  # row count        
        x_counter = 0
        while x_counter < 64:
            fill_color = my_colors.get(abs(int(pressures[count][5][x_counter])), (255, 255, 255))
            x = x_counter * 8
            print ("x = {0} y = {1} color = {2}".format(x,y,fill_color))
            draw.rectangle((y, x, y + 8, x + 8), fill=(fill_color) , outline=None)
            x_counter += 1

        count += 1
        y += 8
        
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
    

for rawfile in list(cur_path.joinpath(cur_path.cwd(),'raw').iterdir()):    

    weather_location = str(rawfile.name.split('_',1)[0])
    match_cache(weather_location)
    print("Reading in {0}".format(rawfile))
    read_in_file(rawfile)

pressures.sort() # because key 0 is epochtime

loop_calculations()
write_cache()
show_calculations(64)
make_chart(64)
make_abs_chart(64)
