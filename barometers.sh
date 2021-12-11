#! /bin/bash


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
import(){
    for file in "$SCRIPTDIR"/raw/*.txt; do
        Skippy="0"
        if [ -f "$1" ];then
            LocNumber=$(basename "$file" | awk -F "_" '{print $1}')
            sed 's/@/,/g' "$1" | grep -v ",," > $CACHEDIR/temp.txt

            while IFS= read -r line; do
                currval=$(echo "$line"| awk -F ',' '{print $3}')
                if [ "$currval" != "$priorval" ];then
                    priorval="$currval"
                    CurrentLineEpoch=$(echo "$line" | awk -F ',' '{print $1}')
                    DoesExist=(grep -c "$CurrentLineEpoch" "$CACHEDIR/$LocNumber_out.txt")
                    if [ "$DoesExist" == "0" ];then
                        echo "$line" >> "$CACHEDIR/$LocNumber_out.txt"
                    else
                        echo "Already have this line."
                    fi
                else
                    ((Skippy++))
                    echo "Skipping duplicate $Skippy"
                fi
            done < $CACHEDIR/temp.txt
        fi
    done
}

do_math(){
    for file in "$CACHEDIR"/*_out.txt; do
        NumberOfLines=$(wc -l < "$file")
        LineCounter=1
        LocNumber=$(basename "$file" | awk -F "_" '{print $1}')
        while [ $LineCounter -lt $NumberOfLines ];do 
            # get the line
            CurrentLine=$(sed -n "$LineCounter{p;q}" "$file")
            CurrentLineValue=$(echo "$CurrentLine" | awk -F ',' '{print $6}')
            CurrentLineEpoch=$(echo "$CurrentLine" | awk -F ',' '{print $1}')
            MathCounter=1
            DoesExist=(grep -c "$CurrentLineEpoch" "$CACHEDIR"/"$LocNumber"_processed.txt)
            if [ "$DoesExist" == "0" ];then
                while [ $MathCounter -lt 51 ];do 
                    ((ReadLineNumber=$LineCounter-$MathCounter))
                    #echo "$ReadLineNumber"
                    BackLine=$(sed -n "$ReadLineNumber{p;q}" "$file")
                    BackLineValue=$(echo "$BackLine" | awk -F ',' '{print $6}')
                    ((DiffLineValue=$CurrentLineValue - $BackLineValue))
                    CurrentLine="$CurrentLine,$DiffLineValue"
                    ((MathCounter++))
                done 
                echo "$CurrentLine" >> "$CACHEDIR"/"$LocNumber"_processed.txt
                echo "$LineCounter of $NumberOfLines processed"
            else
                "Exists"
            fi
            ((LineCounter++))
        done 
    done
}


show_load(){
    while IFS= read -r line; do

        runline=$(echo -e "$line" | awk -F 'hPa,' '{print $2}' | sed "s/^/,/g" | sed "s/\-//g" | sed "s/,/@/g" )

        echo -e "$runline" | sed "s/@2[0-9]/$WHITE█/g" | sed "s/@20/$WHITE█/g" | sed "s/@19/$YELLOW█/g" | sed "s/@18/$YELLOW█/g" |  sed "s/@17/$YELLOW█/g"  | sed "s/@16/$YELLOW█/g"  | sed "s/@15/$YELLOW█/g" | sed "s/@14/$YELLOW█/g" | sed "s/@13/$YELLOW▒/g" | sed "s/@12/$YELLOW░/g" | sed "s/@11/$RED█/g" | sed "s/@10/$RED▒/g" |  sed "s/@0/$CYAN░/g" |  sed "s/@1/$CYAN▒/g" | sed "s/@2/$CYAN█/g" |  sed "s/@3/$BLUE░/g" | sed "s/@4/$BLUE▒/g" |  sed "s/@5/$BLUE█/g" | sed "s/@6/$PURPLE░/g" | sed "s/@7/$PURPLE▒/g" | sed "s/@8/$PURPLE█/g" |  sed "s/@9/$RED░/g" 

    done < $CACHEDIR/out2.txt
}
