import pathlib
#can use a generator object to produce the various values in python by comparing positionals without having to store them in arrays holy shit
# data structure
# pressures = [ epoch, date, time, imp_pressure, unit, metric_pressure, unit, calc_sign(tuple) ] 
# store with sign, calculate abs each time.
# (optionally - look at cache file as well and read it into dict first?)
# get locnumber from file name

pressures = []
cur_path = pathlib.Path()


# double check global and local vars - d

def read_in_file(in_file):
    """ Reading in the cache file into the pressures data structure """ 
    global pressures
    with open(in_file) as infile:
        for row in infile:         
            row.replace("@", ",")
            if not row.find(",,"):
                # epochtime
                # Oh, yeah, we didn't want units did we.
                list_to_add = row.split(',',7)
                if not list_to_add[1] in pressures and not list_to_add[2] in pressures:
                    # taking out units if they exist
                    list_to_add.remove("hPa")
                    list_to_add.remove("in")
                    pressures.append(list_to_add)   #needs to be a list because I will use positionals for calculations later
                    pressures.sort() # because key 0 is epochtime
    in_file.close

def perform_calculations(row):
    """ Calculate the values for calc_signed for the specified row in pressures array """
    global pressures
    now = pressures[row][5]  # only need this once
    signed_calc = [None] * 52  # maybe?
    
    if len(pressures[row]) == 6:   # no tuple in that row
        while count < 52:
            then = pressures[row - count][5]
            signed_calc.append(now - then)
            count += 1

        pressures[row].append(tuple(signed_calc))  #This SHOULD work?

def loop_calculations():
    """ Control loop for calculations """
    global pressures
    
    while count < len(pressures):
        perform_calculations(count)
        count += 1

def show_calculations(num_output):
    """ Display the tuples for the requested number of intervals back """
    global pressures

    while count < num_output:
        print ("{0} {1} {2}".format(str(pressures[row - count][1]), str(pressures[row - count][2]), str(pressures[row - count][7])))
        count += 1


for cachefile in list(cur_path.joinpath(cur_path.cwd(),'cache').iterdir()):
    read_in_file(cachefile)

for rawfile in list(cur_path.joinpath(cur_path.cwd(),'raw').iterdir()):    
    read_in_file(rawfile)



loop_calculations
show_calculations(52)

# for last (user input?) entries, output the generated values
# graphics to output colored data (no idea yet)
