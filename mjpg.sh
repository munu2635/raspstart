export STREAMER_PATH=/home/pi/raspstart/mjpg-streamer/mjpg-streamer-experimental
export LD_LIBRARY_PATH=$STREAMER_PATH
$STREAMER_PATH/mjpg_streamer -i "input_raspicam.so" -o "output_http.so -p 8891 -w $STREAMER_PATH/www/"


