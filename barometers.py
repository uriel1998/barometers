
#can use a generator object to produce the various values in python by comparing positionals without having to store them in arrays holy shit
# data structure
# pressures = [ epoch, date, time, pressure, calc_sign(tuple) ] 
# store with sign, calculate abs each time.
# (optionally - look at cache file as well and read it into dict first?)
# get locnumber from file name

pressures = []

# double check global and local vars - d

def read_in_file(in_file):
    """ Reading in the cache file into the pressures data structure """ 
    global pressures
    with open(in_file) as infile:
        for row in infile:            
            if not row.find(",,"(replace("@", ",")):
                # epochtime
                list_to_add = row.split(',',7)
                if ( not list_to_add[1] in pressures ) AND ( not list_to_add[2] in pressures): 
                    pressures.append(list_to_add)   #needs to be a list because I will use positionals for calculations later
                    pressures.sort() # because key 0 is epochtime
    in_file.close


# loop through pressures after value 52
# if the tuple exists (len of the array is 7, don't calc)
# if it doesn't exist, calc with sign.  Can ABS it later


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
