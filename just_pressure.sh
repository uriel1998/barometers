#!/bin/bash

# This is a stripped-down version that just returns the barometric data
# until I rewrite it in python3 

apiKey=""
defaultLocation=""
data=0
lastUpdateTime=0
FeelsLike=0
CityID="True"
SCRIPTDIR="$( cd "$(dirname "$0")" ; pwd -P )"
RAWDIR="$SCRIPTDIR"/raw

if [ -f "$HOME/.config/weather_sh.rc" ];then
    readarray -t line < "$HOME/.config/weather_sh.rc"
    apiKey=${line[0]}
    defaultLocation=${line[1]}
fi

while [ $# -gt 0 ]; do
option="$1"
    case $option
    in
    -k) apiKey="$2"
    shift
    shift ;;
    -l) defaultLocation="$2"
    shift
    shift ;;
    esac
done

if [ -z $apiKey ];then
    echo "No API Key specified in rc, script, or command line."
    exit
fi

#Is it City ID or a string?
case $defaultLocation in
    ''|*[!0-9]*) CityID="False" ;;
    *) CityID="True" ;;
esac

dataPath="/tmp/wth-$defaultLocation.json"

if [ ! -e $dataPath ];
then
    touch $dataPath
    #The API call is different if city ID is used instead of string lookup
    if [ "$CityID" = "True" ];then
        data=$(curl "http://api.openweathermap.org/data/2.5/weather?id=$defaultLocation&units=metric&appid=$apiKey" 2>/dev/null)
    else
        data=$(curl "http://api.openweathermap.org/data/2.5/weather?q=$defaultLocation&units=metric&appid=$apiKey" 2>/dev/null)
    fi
    echo $data > $dataPath
else
    echo "reading"
    data=$(cat "$dataPath")
    echo "$data"
fi
lastUpdateTime=$(($(date +%s) -600))

    lastfileupdate=$(date -r $dataPath +%s)
    if [ $(($(date +%s)-$lastfileupdate)) -ge 600 ];then
        
        if [ "$CityID" = "True" ];then
            data=$(curl "http://api.openweathermap.org/data/2.5/weather?id=$defaultLocation&units=metric&appid=$apiKey" 2>/dev/null)
        else
            data=$(curl "http://api.openweathermap.org/data/2.5/weather?q=$defaultLocation&units=metric&appid=$apiKey" 2>/dev/null)
        fi
        echo $data > $dataPath
    fi

    lastUpdateTime=$(date +%s)
    ####################################################################
    # Pressure Data
    ####################################################################
    pressure=$(echo $data | jq .main.pressure)
    
    metricpressure=${pressure}
    pressure=$(echo "scale=2; $pressure/33.863886666667" | bc | awk '{$1=$1};1' )
    AsOf=$(date +"%Y-%m-%d %R" -d @$lastfileupdate) 
    nowtime=$(TZ=UTC0 printf '%(%s)T\n' '-1')
    AsOf2=$(date +"%Y-%m-%d@%R," -d @$lastfileupdate)
    echo "${nowtime},${AsOf2}${pressure},in,${metricpressure},hPa" >> "${RAWDIR}/${defaultLocation}_barometer_readings.txt"
