
just_pressure.sh - subset of weather.sh that just gets and saves pressure data. Will use same cache as weather.sh
barometers.py - what actually does the heavy calculations here

usage: barometers.py [-h] [-s NUM_OUTPUT] [-a NUM_INPUT] [-c] [-l] [-S] [-A]
                     [-t]

optional arguments:
  -h, --help            show this help message and exit
  -s NUM_OUTPUT, --show-records NUM_OUTPUT
                        number of records back to show
  -a NUM_INPUT, --add-records NUM_INPUT
                        max number of records to add from input files
  -c, --show-calc       Show calc on stdout
  -l, --line-graph      Produce line graph overlay
  -S, --signed-values   Produce signed value chart
  -A, --abs-values      Produce abs value chart
  -t, --test            Test mode: reads from stdin
