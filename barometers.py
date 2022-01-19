#! /usr/bin/env python3

import pathlib
import linecache
import pickle, sys, string, argparse, datetime
from PIL import Image, ImageDraw, ImageFont

cur_path = pathlib.Path()

parser = argparse.ArgumentParser(usage=__doc__)
    parser.add_argument("-a", "--add-records", type=int, help="max number of records to add from input files", default=256,action='store',dest='num_input')
    parser.add_argument("-b", "--begin-date", dest="start_date", action='store', default=None,help="Provide the start date for chart or calculation data.")
    parser.add_argument("-d", "--display-records", type=int, help="number of records back to show", default=None,action='store',dest='num_output')
    parser.add_argument("-e", "--end-date", dest="end_date", action='store', default=None,help="Provide the end date for chart or calculation data; optional, only makes sense with --begin-date.")
    parser.add_argument("-s", "--scheme", dest="scheme",action='store', default=None, help="Color scheme - default, wide, alt, original")
    parser.add_argument('-v', '--verify', dest='to_verify', action='store_true', default=False,help="Verify interval ranges")
    parser.add_argument('-t', '--tolerance', action='store',dest='tolerance_range', default="300",help="Acceptable range in seconds, only makes sense with -v")
    parser.add_argument('-i', '--interval', action='store',dest='verify_interval', default="1800",help="Expected interval in seconds, only makes sense with -v")    
    parser.add_argument('-B', '--bout-here', action='store', dest='bout_here',help="Where to output/input weather location from.")    
    parser.add_argument('-f', '--file', action='store',dest='fn_stem', default="out",help="Stem for output filename, defaults to out_[abs|signed].png")
    parser.add_argument("-w", "--walk_about", dest="walkabout",action='store_true', default=False, help="Modify walking chart by distance from present")
    
    
    
    
    
    parser.add_argument("-C", "--show-calc", dest="showcalc",action='store_true', default=False, help="Show calc on stdout")
    parser.add_argument("-L", "--line-graph", dest="linegraph",action='store_true', default=False, help="Produce line graph overlay")

    parser.add_argument("-S", "--signed-values", dest="signval",action='store_true', default=False, help="Produce signed value chart")
    parser.add_argument("-A", "--abs-values", dest="absval",action='store_true', default=False, help="Produce abs value chart")



    parser.add_argument("-W", "--walking", dest="walking",action='store_true', default=False, help="Produce walking value chart")

    args = parser.parse_args()
    
