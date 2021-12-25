
can use a generator object to produce the various values in python by comparing positionals without having to store them in arrays holy shit
# data structure
# pressures = [ epoch, date, time, pressure, calc_abs[], calc_sign[] ] 

# (optionally - look at cache file as well and read it into dict first?)
# get locnumber from file name

pressures = []

# double check global and local vars - d

def read_in_cache(cache_file):
    """ Reading in the cache file into the pressures data structure """ 

    with open(cache_file) as infile:
        for row in infile:            
            if not row.find(",,"(replace("@", ",")):
                # okay, this is it - but this needs to be assigned to a dictionary (or list?).
                # epochtime
                y = row.split(',',7)
                # change this to dictionary definitions here mate
                epochtime = y[0]
                date = y[1]
                time = y[2]
                imp_now = y[3]
                metric_now = y[5]
                # this should be converting it to a list, but probably isn't
                # need a different split here for abs with sign calculations
                calc_abs = int(y[7])
                calc_sign = int(y[8])
                
                if not date in pressures and not time in pressures:   # may need to do a sub-key check? unsure if this will also trigger off different lines
                    list_to_add = [epochtime,date,time,imp_now,metric_now]
                    list_to_add.append(calc_abs)
                    list_to_add.append(calc_sign)  # because I want it as a sub-list
                    pressures.append(list_to_add)   #needs to be a list because I will use positionals for calculations later
                    pressures.sort() # because key 0 is epochtime


        
# read in line by line
    # remove if empty value
    # sort dict keys (or read dict keys) by epoch key
# generator (or do calculations) for ABS_val and SIGN_val (er, research that) and add to dict
    # you can assign functions to variables! (9.5)
    # lambda expressions might be what I'm looking for? (9.6)
    # nope, it's generators with a subgenerator for counting or somesuch
        while count < 52:
            then=get dictvalue[now-count]
            now[position in dict for data]=now[0] - then
            #ABSVAL as well
            count += 1
            
# for last (user input?) entries, output the generated values
# graphics to output colored data (no idea yet)



list[ curr_value, [ list_of_abv[] ], [list of ] ]

access by 

list[1][3]


New calculation is 

C52-C51 C51-C50 C50-C49 C49-C48
|(1024-1025)|+|(1025-1026)|+|(1026-1025)|+|(1025-1024)|
1 + 1 + 1 + 1 = 4
without abs, gets you to 0.

timestamp. current pressure.  [ set of ABV(current pressure - interval back current pressure) ].  [ set of (current pressure - interval back current pressure) ]. \ 
