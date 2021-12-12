#! /bin/bash

# Dayton is : 4509884
#Derived from https://gist.githubusercontent.com/elucify/c7ccfee9f13b42f11f81/raw/9f27e072aadc4df6f84d515309c82585a8a13d8e/gistfile1.txt

RESTORE=$(echo -en '\033[0m')
RED=$(echo -en '\033[00;31m')
GREEN=$(echo -en '\033[00;32m')
YELLOW=$(echo -en '\033[00;33m')
BLUE=$(echo -en '\033[00;34m')
MAGENTA=$(echo -en '\033[00;35m')
PURPLE=$(echo -en '\033[00;35m')
CYAN=$(echo -en '\033[00;36m')
LGRAY=$(echo -en '\033[00;37m')
LRED=$(echo -en '\033[01;31m')
LGREEN=$(echo -en '\033[01;32m')
LYELLOW=$(echo -en '\033[01;33m')
LBLUE=$(echo -en '\033[01;34m')
LMAGENTA=$(echo -en '\033[01;35m')
LPURPLE=$(echo -en '\033[01;35m')
LCYAN=$(echo -en '\033[01;36m')
WHITE=$(echo -en '\033[01;37m')


SCRIPTDIR="$( cd "$(dirname "$0")" ; pwd -P )"
CACHEDIR="$SCRIPTDIR"/cache

# parse CSV - sub out @ for , so hours are right
# clean CSV - remove lines that contain ,,
# loop through CSV, comparing third column to the prior line, third column, if the same, don't print it
### THIS

## AFTER INITIAL IMPORT, ONLY TAKE LAST 100 LINES OR SO? 

import(){

     for file in $(find "$SCRIPTDIR"/raw -iname "*.txt"); do
        Skippy="0"
        echo "!$file!"
        if [[ -f "$file" ]];then
            LocNumber=$(basename "$file" | awk -F "_" '{print $1}')
            echo "Parsing location $LocNumber from file $file"
            LocTemp="$CACHEDIR/$LocNumber"_temp.txt
            LocOut="$CACHEDIR/$LocNumber"_out.txt
            if [ ! -f "$LocTemp" ];then
                touch "$LocTemp"
            fi
            sed 's/@/,/g' "$file" | grep -v ",," > "$LocTemp"
            if [ ! -f "$LocOut" ];then
                touch "$LocOut"
            fi
            while IFS= read -r line; do
                currval=$(echo "$line"| awk -F ',' '{print $3}')
                if [ "$currval" != "$priorval" ];then
                    priorval="$currval"
                    CurrentLineEpoch=$(echo "$line" | awk -F ',' '{print $1}')
                    DoesExist=$(grep -c "$CurrentLineEpoch" "$LocOut")
                    if [ "$DoesExist" == "0" ];then
                        echo "$line" >> "$LocOut"
                    else
                        echo "Already have this line."
                    fi
                else
                    ((Skippy++))
                    echo "Skipping duplicate $Skippy"
                fi
            done < "$LocTemp"
        fi
    done
}

do_math(){
    for file in $(find "$CACHEDIR" -iname "*_out.txt"); do
        InMathFile="$file"
        NumberOfLines=$(wc -l < "$InMathFile")
        # THIS MUST START AT > 51 (or greater than number of values you're looking back)
        # UNLESS YOU'RE USING A TRUNCATED DATA SET
        LineCounter=52
        LocNumber=$(basename "$InMathFile" | awk -F "_" '{print $1}')
        LocProcessed="$CACHEDIR"/"$LocNumber"_processed.txt
        if [ ! -f "$LocProcessed" ];then
            touch "$LocProcessed"
        fi
        while [ $LineCounter -lt $NumberOfLines ];do 
            # get the line

            CurrentLine=$(sed -n "$LineCounter{p;q}" "$InMathFile")
            CurrentLineValue=$(echo "$CurrentLine" | awk -F ',' '{print $6}')
            CurrentLineEpoch=$(echo "$CurrentLine" | awk -F ',' '{print $1}')
            MathCounter=1
            DoesExist=$(grep -c "$CurrentLineEpoch" "$LocProcessed" )
            if [ "$DoesExist" == "0" ];then
                while [ $MathCounter -lt 51 ];do 
                    ((ReadLineNumber=$LineCounter-$MathCounter))
                    #echo "$ReadLineNumber"
                    BackLine=$(sed -n "$ReadLineNumber{p;q}" "$InMathFile")
                    BackLineValue=$(echo "$BackLine" | awk -F ',' '{print $6}')
                    ((DiffLineValue=$CurrentLineValue-$BackLineValue))
                    CurrentLine="$CurrentLine,$DiffLineValue"
                    ((MathCounter++))
                done 
                echo "$CurrentLine" >> "$LocProcessed"
                echo "$LineCounter of $NumberOfLines processed"
            else
                echo "Line $LineCounter Exists"
            fi
            ((LineCounter++))
        done 
    done
}


show_load(){

    if [ ! -f "$CACHEDIR"/display.tmp ];then
        touch "$CACHEDIR"/display.tmp
    fi
    
    for file in $(find "$CACHEDIR" -iname "*_processed.txt"); do
        if [ -f "$file" ];then 
            echo "!$file!"
            tail -n 256 "$file" > "$CACHEDIR"/display.tmp
            #cat "$file" > "$CACHEDIR"/display.tmp
            
            while IFS= read -r line; do
                datetime=$(echo -e "$line" | awk -F ',' '{print $2" "$3}')
                runline=$(echo -e "$line" | awk -F 'hPa,' '{print $2}' | sed "s/^/,/g" | sed "s/\-//g" | sed "s/,/@/g" )

                colorline=$(echo -e "$runline" | sed "s/@2[0-9]/$WHITE█/g" | sed "s/@20/$WHITE█/g" | sed "s/@19/$YELLOW█/g" | sed "s/@18/$WHITE▒/g" |  sed "s/@17/$WHITE▒/g"  | sed "s/@16/$WHITE░/g"  | sed "s/@15/$WHITE░/g" | sed "s/@14/$YELLOW█/g" | sed "s/@13/$YELLOW▒/g" | sed "s/@12/$YELLOW░/g" | sed "s/@11/$RED█/g" | sed "s/@10/$RED▒/g" |  sed "s/@0/$CYAN░/g" |  sed "s/@1/$CYAN▒/g" | sed "s/@2/$CYAN█/g" |  sed "s/@3/$BLUE░/g" | sed "s/@4/$BLUE▒/g" |  sed "s/@5/$BLUE█/g" | sed "s/@6/$PURPLE░/g" | sed "s/@7/$PURPLE▒/g" | sed "s/@8/$PURPLE█/g" |  sed "s/@9/$RED░/g" )
                echo -e "$datetime  $colorline"
            done < $CACHEDIR/display.tmp
        fi
    done
}

show_numbers_load(){

    if [ ! -f "$CACHEDIR"/display.tmp ];then
        touch "$CACHEDIR"/display.tmp
    fi
    
    for file in $(find "$CACHEDIR" -iname "*_processed.txt"); do
        if [ -f "$file" ];then 
            echo "!$file!"
            tail -n 256 "$file" > "$CACHEDIR"/display.tmp
            #cat "$file" > "$CACHEDIR"/display.tmp
            
            while IFS= read -r line; do
                datetime=$(echo -e "$line" | awk -F ',' '{print $2" "$3}')
                runline=$(echo -e "$line" | awk -F 'hPa,' '{print $2}' | sed "s/^/,/g" | sed "s/\-//g" | sed "s/,/@/g" )
                runline=$(echo -e "$runline" | awk -F '@' '{print "@"$2 "@"$7 "@"$13 "@"$18 "@"$25 "@"$37 "@"$50}')
                colorline=$(echo -e "$runline" | sed "s/@2[0-9]/$WHITE█/g" | sed "s/@20/$WHITE█/g" | sed "s/@19/$YELLOW█/g" | sed "s/@18/$WHITE▒/g" |  sed "s/@17/$WHITE▒/g"  | sed "s/@16/$WHITE░/g"  | sed "s/@15/$WHITE░/g" | sed "s/@14/$YELLOW█/g" | sed "s/@13/$YELLOW▒/g" | sed "s/@12/$YELLOW░/g" | sed "s/@11/$RED█/g" | sed "s/@10/$RED▒/g" |  sed "s/@0/$CYAN░/g" |  sed "s/@1/$CYAN▒/g" | sed "s/@2/$CYAN█/g" |  sed "s/@3/$BLUE░/g" | sed "s/@4/$BLUE▒/g" |  sed "s/@5/$BLUE█/g" | sed "s/@6/$PURPLE░/g" | sed "s/@7/$PURPLE▒/g" | sed "s/@8/$PURPLE█/g" |  sed "s/@9/$RED░/g" )
                echo -e "$datetime  $colorline"
            done < $CACHEDIR/display.tmp
        fi
    done
}


#tail -n 576 /home/steven/tmp/4509884.txt > "$SCRIPTDIR"/raw/4509884_barometer_readings.txt
#import
#do_math
#show_load
# this is prototyping a load type display
show_numbers_load
