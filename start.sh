echo start...

(source venv/bin/activate && python3 ./mqttbkp_srv.py >out_log.txt 2>&1 ) &

echo started ok

sleep 5

echo mqttbkp_srv started with ps:
ps | grep python
