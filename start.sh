(python3 ./mqttbkp_srv.py >out.txt 2>&1 ) &

echo mqttbkp_srv started with ps:
ps | grep python