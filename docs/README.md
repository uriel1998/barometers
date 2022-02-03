barometers
==========

# A different way at looking at historical and current barometric data for a location.


* `barometers.py` - Produce graphs and various charts of historical barometric data for a location to aid in visualization of pressure changes quickly for (possible) prediction of health effects from the change in weather pressure.  

* Quickstart:  Install [Python (tested with v3.9.9)](https://www.python.org/downloads/) and [the PIL library](https://pillow.readthedocs.io/en/stable/installation.html).  Clone/download this repository. Get an [API key from OpenWeatherMap](http://openweathermap.org/appid).  Run the program once every half hour from a scheduled task or as a cron job.  After you've collected enough data, start outputting graphs or the "barometric load".

* To see the differences the calculations and color schemes make with data, skip down to the Examples section.

  ![](https://i.imgur.com/BDd3tBx.png)

  ![](https://i.imgur.com/OaxA4JG.png)

## Contents
 1. [About](#1-about)
 2. [Methodology](#2-methodology-and-theory)
 3. [License](#3-license)
 4. [Prerequisites](#4-prerequisites)
 5. [Installation](#5-installation)
 6. [Usage](#6-usage)
 7. [Examples](#7-Examples)
 8. [TODO](#8-todo)

***

## 1. About

I suffer from Willis-Ekbom Syndrome, commonly (and in my case, wrongly) called "Restless Legs Syndrome".  In my case, I experience it as *pain*, and it seemed to be significantly worse when there was a rapid change in the barometric pressure.

I know a number of other people who experience symptoms when the pressure changes quickly - or at least, it *seems* to correlate.  I noticed that I could see the correlation when I looked back at graphs, but I had a hard time *predicting* when I'd have bad symptoms from publicly available data and graphs.

Until it hit me that bodily symptoms - particularly around pressure - take *time* to adjust to changes in the environment. [I made a rough bash script that charted change over time, and it seems to provide some degree of predictive ability](https://ideatrash.net/2021/12/data-hiding-in-plain-sight-pain-and-pressure-changes-over-time.html) 

So then I taught myself python properly in a week and rewrote the program so it could provide more visualizations of the data, and am making it available so that others can do the same.

## 2. Methodology and Theory

### Hypothesis

When I looked at the raw data - particularly at hour-over-hour change - the changes in barometric pressure did *not* seem to track with my symptoms, even though I had plenty of anecdata that it did.  When I looked at graphs of barometric pressure over the past day (or even few hours), it was *intuitively* obvious most of the time.  I could even experience the difference in pressure driving from the higher elevations at my parent's house in the Appalachian mountains back home.  So from my own experience and *visually* looking at the graphs, I knew there was something there.

Recently I was telling a friend about how I used to have really bad problems getting my ears to pop due to elevation changes. Usually when I'd fly - something I've not done pretty much since I left the military - it would be overnight before the pressure would equalize.  (I also recently got a continuous glucose monitor, which also helped reinforce this realization that bodily processes react on a relatively slow time frame.)

And I realized that if my nerves were being irritated by physical changes of the fluid sacs inside my joints (a probable hypothesis for how barometric pressure relates to my nervous system disorder), it would *also* take time for equalization to happen.  **Therefore, it was not just *recent* changes, but *longer scale* changes over time**.

### Methods: Initial Graphing

My initial graphs were pretty straightforward affairs; I collected the data using a tweak to my [weather.sh](https://uriel1998.github.io/weather.sh) script and a cron job.  (Most of the images and charts used here are from roughly the same time period that I was re-writing this README; coincidentally there is also a winter storm passing overhead literally right now as well.)

![](https://i.imgur.com/6aGQ2up.png)

With my new realization, I coded a (very, very) kludgy bash script that was able to create a rudimentary chart:

![](https://i.imgur.com/Pm7NfiI.png)

It took *forever* to run and calculate things, and it was just held together by chewing gum and twine. So I taught myself Python properly over a week or so and created the 0.9 version of this program.  Which *works*, but had some serious drawbacks and limitations due to my own inexperience.  So I took the next month to level up with Python, re-check my methodology, and to add additional functions and features for robustness and to allow others to both use this tool and to check my own findings.

### Methods: Verification

One of the trickiest parts of this project was verifying the data being fed into it. Garbage in, garbage out, after all.  

* When reading data in from a CSV/text file (see the example in the "raw" subdirectory), the program checks for rows that do not have input data and skips them.

* A binary cache is maintained of the data. If the --overwrite-cache (or -o) flag is passed, data being read in that has the same timestamp will *overwrite* whatever is in the cache.

* The primary goal of verification is to ensure that each data entry row is at roughly the same time interval. This is calculated by taking the first *selected* entry and rounding it to the closest half hour.  The program then walks through the selected data set, ensuring that each entry is separated by *interval* seconds, plus or minus *tolerance* seconds.  The defaults for *interval* is 1800 seconds (a half hour) and for *tolerance* is 300 seconds (five minutes).  This works well for me, YMMV.

* If the program detects that there is a reading that occurred *too soon*, it *skips* that entry and puts a "‡" symbol in the record for the *prior* entry.

* If the program detects that there were *missed* readings, it looks back to see how many readings were missed, and *duplicates* the last good reading to stand in for any readings that were missed. Those placeholder readings have a "†" symbol added to their record.

### Methodology: Calculations

There are several different derivative calculations that are performed. Each is explained and may be more helpful in your particular case for seeing any correlations between your symptoms and barometric pressure.  

* Signed Calculations: This compares the barometric pressure in entry X with the pressures of prior entries, maintaining the signed difference.  
* Absolute Value Calculations: This compares the absolute value of the difference in pressure in entry X with the pressures of prior entries.
* Walking Value Calculations: This attempts to account for peaks and valleys by integrating the distance "walked" by the pressure over time.  Currently this is done in a kind of "shortcut" by looking at the maximum and minimum value and looking at the range between them.

<img src="https://i.imgur.com/F1GyEJK.jpg" style="zoom:150%;" />

In this simplified example, with pressure as the Y axis and time interval as the X axis, at time #2, the *signed* value would be -5, the *absolute* value would be 5, and the *walking* value would be 5.  At time #4, the *signed* and *absolute* value would both be 0 (because they're back at "5"), while the *walking* value would be 5.

Additionally, I have created two "load" calculations - *signed load* and *walking load*.  

The term "load" is a computing term; the key thing is that it is usually reported out as "1 minute, 5 minute, and 15 minute" values. In that way, three numbers can give you a quick idea of how hard your computer is working overall, and how long it's been working that way.  

<img src="https://i.imgur.com/EvutNwN.jpg" style="zoom:150%;" />

Both *signed load* and *walking load* work the same way, but for how active barometric pressure is over time.  They get their information from either the signed calculations or the walking calculations respectively.  Rather than 1,5, and 15 minutes, the "load" reported by this program covers 8, 16, or 32 intervals - by default, 4, 8, and 16 hours.  

### Output and Results

This chart - displaying *signed* calculations - has all the bells and whistles enabled.  The Y-axis is the time period (most recent at the bottom).  Each "block" of color from left to right represents the difference in pressure between that time and a half-hour further back in time.  The line graph overlying is the same style of line graph from the very beginning, just rotated so that the time periods match.  The "load" is in tiny text right next to the time period label.  You can clearly see how the graph correlates to the color gradients.

![](https://i.imgur.com/gcdOV8X.png)

One of the most striking things I noted was that if there is no change in pressure, the "load" seems to *slowly* return back toward normal.  This output covers the most recent ("bottommost") plateau in the chart above.  Note in particular the leftmost value of "load" here ticks back toward 0 over time when there is no change in barometric pressure.  In this way, this derivative value seems to be a rough model of the time it takes the body to readjust.

```
2022-02-02 @ 03:27: load:   0: -6:-20 w_load:   0:  8: 30 in:30.06 hPa:1018 epoch:1643790602
2022-02-02 @ 03:57: load:   8: 10: 15 w_load:   0:  7: 27 in:30.09 hPa:1019 epoch:1643792401
2022-02-02 @ 04:27: load:  -1: -7:-15 w_load:   7: 15: 33 in:30.06 hPa:1018 epoch:1643794202
2022-02-02 @ 04:58: load:   7: 10: 19 w_load:   7: 15: 32 in:30.09 hPa:1019 epoch:1643796002
2022-02-02 @ 05:29: load:  -2: -6:-12 w_load:   7: 15: 31 in:30.06 hPa:1018 epoch:1643797802
2022-02-02 @ 05:59: load:   6: 11: 21 w_load:   7: 15: 31 in:30.09 hPa:1019 epoch:1643799602
2022-02-02 @ 06:29: load:   5: 11: 21 w_load:   7: 15: 31 in:30.09 hPa:1019 epoch:1643801401
2022-02-02 @ 06:59: load:  12: 27: 53 w_load:   6: 14: 30 in:30.12 hPa:1020 epoch:1643803202
2022-02-02 @ 07:29: load:  10: 26: 52 w_load:  12: 28: 60 in:30.12 hPa:1020 epoch:1643805002
2022-02-02 @ 07:50: load:   8: 24: 50 w_load:  10: 26: 58 in:30.12 hPa:1020 epoch:1643806802
2022-02-02 @ 08:20: load:   7: 22: 48 w_load:   8: 24: 56 in:30.12 hPa:1020 epoch:1643808602
2022-02-02 @ 08:50: load:   5: 20: 46 w_load:   6: 22: 54 in:30.12 hPa:1020 epoch:1643810402
2022-02-02 @ 09:20: load:   4: 18: 44 w_load:   4: 20: 52 in:30.12 hPa:1020 epoch:1643812202
2022-02-02 @ 09:50: load:   2: 16: 42 w_load:   2: 18: 50 in:30.12 hPa:1020 epoch:1643814002
2022-02-02 @ 10:21: load:   1: 14: 40 w_load:   1: 16: 48 in:30.12 hPa:1020 epoch:1643815802
2022-02-02 @ 10:51: load:   0: 12: 38 w_load:   0: 14: 46 in:30.12 hPa:1020 epoch:1643817602
2022-02-02 @ 11:21: load:   0: 10: 36 w_load:   0: 12: 44 in:30.12 hPa:1020 epoch:1643819402
2022-02-02 @ 11:52: load:  -8: -8:  2 w_load:   0: 10: 42 in:30.09 hPa:1019 epoch:1643821202
2022-02-02 @ 12:22: load: -15:-24:-31 w_load:   7: 18: 50 in:30.06 hPa:1018 epoch:1643823002
2022-02-02 @ 12:52: load: -13:-24:-30 w_load:  13: 29: 61 in:30.06 hPa:1018 epoch:1643824802
2022-02-02 @ 13:22: load: -19:-39:-61 w_load:  11: 27: 59 in:30.03 hPa:1017 epoch:1643826602
2022-02-02 @ 13:52: load: -16:-38:-59 w_load:  16: 40: 88 in:30.03 hPa:1017 epoch:1643828401
2022-02-02 @ 14:22: load: -13:-36:-57 w_load:  13: 37: 85 in:30.03 hPa:1017 epoch:1643830202
2022-02-02 @ 14:53: load: -18:-50:-87 w_load:  10: 34: 82 in:30.00 hPa:1016 epoch:1643832002
2022-02-02 @ 15:23: load: -14:-46:-84 w_load:  14: 46:110 in:30.00 hPa:1016 epoch:1643833802
2022-02-02 @ 15:53: load: -10:-42:-82 w_load:  10: 42:106 in:30.00 hPa:1016 epoch:1643835602
2022-02-02 @ 16:24: load:   1:-22:-48 w_load:   7: 38:102 in:30.03 hPa:1017 epoch:1643837402
2022-02-02 @ 16:54: load:  -6:-35:-79 w_load:   8: 37:101 in:30.00 hPa:1016 epoch:1643839202
2022-02-02 @ 17:24: load:  -4:-31:-77 w_load:   7: 34: 98 in:30.00 hPa:1016 epoch:1643841001
2022-02-02 @ 17:54: load:  -3:-27:-75 w_load:   6: 30: 94 in:30.00 hPa:1016 epoch:1643842802
2022-02-02 @ 18:25: load:   6: -7:-41 w_load:   5: 26: 90 in:30.03 hPa:1017 epoch:1643844601
2022-02-02 @ 18:55: load:   6: -4:-40 w_load:   7: 25: 89 in:30.03 hPa:1017 epoch:1643846402
2022-02-02 @ 19:25: load:   5: -1:-39 w_load:   6: 21: 85 in:30.03 hPa:1017 epoch:1643848202
2022-02-02 @ 19:56: load:   4:  2:-38 w_load:   5: 17: 81 in:30.03 hPa:1017 epoch:1643850002
2022-02-02 @ 20:26: load:   3:  4:-36 w_load:   4: 14: 77 in:30.03 hPa:1017 epoch:1643851801
2022-02-02 @ 20:56: load:   3:  5:-35 w_load:   3: 12: 73 in:30.03 hPa:1017 epoch:1643853602
2022-02-02 @ 21:26: load:   2:  6:-33 w_load:   2: 10: 69 in:30.03 hPa:1017 epoch:1643855402
```

Looking at it this way, you can get an "at a glance" sense of how the pressure has been changing without even looking at a graph.  A load of, say, 5 26 90 (the walking load from epoch 1643844601) tells you that while the pressure has somewhat leveled off, there were some significant changes not long before.  

These different forms of visualizing and calculating the barometric data have helped me better understand the correlation with my symptoms, and while not *prediction*, I can now easily and quickly get a measure of how much "load" the barometric pressure is under - that is, how fast it's been changing, and how recently it changed.

### Future Research

A more robust "walking" calculation (where, in my simple example above, the *walking* value would be 10 instead of 5) might also be worth developing.

## 3. License

This project is licensed under the MIT license. For the full license, see `LICENSE`.

## 4. Prerequisites

 * [The Pillow (or PIL) library](https://pillow.readthedocs.io/en/stable/installation.html)
    - Written and tested using `python3-willow` 1.4-1 from Debian stable (e.g `sudo apt-get python3-willow`)

 * OpenWeatherMap API key ([http://openweathermap.org/appid](http://openweathermap.org/appid)).
 * Python 3 https://www.python.org/downloads/

## 5. Installation

* Clone the repository (or unpack a release) into its own directory.

* Install the PIL/Pillow library (above version 4; the version "1.4-1" in Debian stable is sufficient).  

* Create a directory "raw" and "cache" underneath the program directory.

* Edit the file `barometers.ini` in the program directory. 

  * The first line is the [OpenWeatherMap API key](https://openweathermap.org/appid). _Note: If the OpenWeatherMap API key is specified from the command-line, it 
    will override the API key set in the file._

  * The second line is your default location. It is **STRONGLY** recommended to use the City ID from OpenWeatherMap 
    instead of a city name. Instructions on finding your city's City ID [here](https://www.dmopress.com/openweathermap-howto/) .


## 6. Usage

`barometers.py` requires a dataset. While the repository includes data I've collected, it *probably* does not apply to your location.  You must obtain an OpenWeatherMap API key and find out your location ID.  At that point, set up a scheduled task for every thirty minutes to run:

`python ./barometers.py -r -k YOURAPIKEY -B YOURLOCATIONID`

If you have configured `barometers.ini` with this information, you can simply call:

`python ./barometers.py -r`

After that, experiment with the possible options for output.  A suggested start for output is `barometers.py -q -v -S -L -l` which produces a chart similar to the one under "Output and Results" above.
```
usage: barometers.py [-h] [-q] [-a NUM_INPUT] [-o] [-r] [-k API_KEY] [-n]
                   [-B BOUT_HERE] [-b START_DATE] [-e END_DATE]
                   [-d NUM_OUTPUT] [-s SCHEME] [-v] [-t TOLERANCE]
                   [-i INTERVAL] [-F FONT] [-f FN_STEM] [-l] [-D] [-L] [-S]
                   [-A] [-W]
```
### General Switches
```
-h, --help            show this help message and exit
-q, --quiet           Minimize output to STDOUT/STDERR
```
### Controlling addition of data  
```
-a NUM_INPUT, --add-records NUM_INPUT	Number of records to add from input files
-o, --overwrite-cache 					Overwrite cache data when importing new data.
-r, --retrieve-current					Get reading from OpenWeatherMap
-k API_KEY, --api-key API_KEY			API key for OpenWeatherMap
-n, --no-cache        					Do not write retrieved information to cache.
```
* The data structure used is: 
  `[time of collection (epoch),date of collection (YYYY-mm-dd),time of collection (HH:MM),pressure imperial,pressure metric, calc[64],walking[64],autoheal (either "†" or "‡")] `

### Selecting data

You can amass a *lot* of data, so there are several ways to control the amount of 
output shown.  The default number of records charted/shown is 256 if unspecified 
in any way.

- If the start date is given (in YYYY-mm-dd format), and the end date is set, it 
  will show between those dates inclusive (or to the end of the file).
  
- If the start date is given and the number of records is set, it will show from 
  beginning of the start date and show that many records (or to the end of the file).
  
- If the start date is given and no other criteria given, it will show from the 
  beginning of the start date to the end of the data.  
  

```
-B BOUT_HERE, --bout-here BOUT_HERE			Where to output/input weather location from. 
											Also selects which cache file to use.
-b START_DATE, --begin-date START_DATE		Provide the start date for chart or calculation data.
-e END_DATE, --end-date END_DATE			Provide the end date for chart or calculation data;
											optional, only makes sense with --begin-date.
-d NUM_OUTPUT, --display-records NUM_OUTPUT	Number of records to display
```

### Verification of Data

Verification is done on the data selected for output/display.  Defaults are 1800 seconds/300 seconds, respectively.
```
-v, --verify          				Verify interval ranges
-t TOLERANCE, --tolerance TOLERANCE	Acceptable range in seconds, only makes sense with -v
-i INTERVAL, --interval INTERVAL	Expected interval in seconds, only makes sense with -v
```
### Specifying the Output of Data

- Line graph time values match the Y-axis; the X-axis auto-scales to fit the generated chart.
- "Auto" attempts to maintain a roughly consistent color scale
- If **load** calculations are specified by themselves, it will output *only* the most recent load calculations to STDOUT. 

```
-s SCHEME, --scheme SCHEME	Color scheme - default, auto alt, original
-F FONT, --font FONT  		Path to TTF/OTF font if desired. Defaults to Arial
-f FN_STEM, --file FN_STEM	Stem for output filename, defaults to out_[abs|signed|walk].png
-l, --load            		Show  "load" calculations in selected output
-D, --show-data       		Show data of range on stdout, or load calculations 
							for data range if **load** is also specified.
-L, --line-graph      		Produce line graph overlay
-S, --signed-values   		Produce signed value chart
-A, --abs-values      		Produce abs value chart
-W, --walking         		Produce walking value chart
```

## 7. Examples

### Command Line Switch Examples

Produce a chart of the last 256 intervals, only of absolute values of pressure change, 
using the default color scheme, with overlaid line graph and legend, 
named `out_abs.png` in the current directory:

`python ./barometers.py -A -l`

Produce a chart of the last 256 intervals, of absolute values *and* signed values 
of pressure change, using the default color scheme, with overlaid line graph and legend, 
named `out_abs.png` and `out_signed.png` in the current directory:

`python ./barometers.py -A -S -l`

Produce a chart of the last 512 intervals, only of absolute values of pressure change, 
using the "alt" color scheme, with overlaid line graph and legend, 
named `foo_abs.png` in the current directory:

`python ./barometers.py -A -l -f foo -s alt -d 512`

Produce a chart of data from 2021-12-30 through 2022-01-01, only of signed 
values of pressure change, using the "original" color scheme, with overlaid line 
graph and legend, named `bar_signed.png` in the current directory:

`python ./barometers.py --signed-values -l -f bar -s original -b 2021-12-30 -e 2022-01-01`

### Output Examples

Console output when reading in a text file (where a large amount of the data has already been read into the cache): `examples/reading_in_output.txt`

Console output for `display data`: `examples/dump_output.txt`

Console output for `display data` with `load` enabled: `examples/load_output.txt`

Chart output of the same time period, all using the auto color scale, showing the difference in signed, abs, and walking charts respectively:

![](https://i.imgur.com/Z3nfmVe.png)

![](https://i.imgur.com/pqEVciw.png)

![](https://i.imgur.com/ZHs7gEj.png)

Chart output of the same time period showing the default, original, alt, and auto color scales in that order:

![](https://i.imgur.com/INRfGWi.png)

![](https://i.imgur.com/0YzJuR1.png)

![](https://i.imgur.com/IJssHtX.png)

![](https://i.imgur.com/u0WbZcp.png)

## 8. ToDo

* A more robust "walking" calculation (where, in my simple example above, the *walking* value would be 10 instead of 5) might also be worth developing.
