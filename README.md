
just_pressure.sh - subset of weather.sh that just gets and saves pressure data. Will use same cache as weather.sh
barometers.py - what actually does the heavy calculations here

Automatically reads in text files from ./raw  where location number is first in 
the filename (if anythign after, have location_blahblah.ext ) and uses existing 
cache to avoid dupes.  Reads in most recent 256 records by default, performs 
calculations out to 64 intervals back (for new data), and then saves it to the 
cache and reports out how many records and from what dates/times.

Output is controlled by command line switches.

# TODO: select time period as passed interval

    If number of output is not set, defaults to 256
    If start_date is set and end date is set, shows between those two inclusive
    If start_date is set and num_output is set, starts at start_date and shows num_output
    If start_date is set, and num output not set, defaults to end of data
    

# TODO: Incorporate gathering data as well?
# TODO: Check intervals for equivalent time passage
# TODO: Line-only graph
# Line graph auto scales!

# Note on the data structure for pressures
# pressures = epoch,date,time,pressure imperial,pressure metric, calc[64]

usage: barometers.py [-h] [-d NUM_OUTPUT] [-a NUM_INPUT] [-c] [-l] [-s SCHEME]
                     [-S] [-A] [-t]

optional arguments:
  -h, --help            show this help message and exit
  -d NUM_OUTPUT, --display-records NUM_OUTPUT
                        number of records back to show
  -a NUM_INPUT, --add-records NUM_INPUT
                        max number of records to add from input files
  -c, --show-calc       Show calc on stdout
  -l, --line-graph      Produce line graph overlay
  -s SCHEME, --scheme SCHEME
                        Color scheme - default, wide, alt, original
  -S, --signed-values   Produce signed value chart
  -A, --abs-values      Produce abs value chart
  -t, --test            Test mode: reads from stdin
