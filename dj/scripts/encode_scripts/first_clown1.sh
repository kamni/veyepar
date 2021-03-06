#!/bin/bash -x

# http://www.firstclown.us/2008/07/01/transcoding-dv-to-widescreen-mp4-in-linux/
# http://juliensimon.blogspot.com/2009/01/howto-ffmpeg-x264-presets.html

# params: show_dir file_root
echo show_dir: $1
echo file_root: $2

IN=$1/tmp/$2.dv
TEMP=$1/tmp/$2.mp4
OUT=$1/mp4/$2.mp4

# First Pass
ffmpeg -f dv -i $IN -pass 1 -vcodec libx264 -g 300 -vpre fastfirstpass -mbd 2 -cmp 2 -subcmp 2 -deinterlace -aspect 16:9 -s 640x360 -padtop 4 -padbottom 4 -b 768k -acodec libfaac -y $TEMP

# Second Pass
ffmpeg -f dv -i $IN -pass 2 -vcodec libx264 -vpre hq -g 300 -mbd 2 -cmp 2 -subcmp 2 -deinterlace -aspect 16:9 -s 640x360 -padtop 4 -padbottom 4 -b 768k -acodec libfaac -y $TEMP

MP4Box -add $TEMP $OUT  
MP4Box -par 1=1:1 $OUT

