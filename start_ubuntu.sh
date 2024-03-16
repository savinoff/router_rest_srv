echo start mqttbkp_srv...

source ./venv/bin/activate && nohup python3 ./mqttbkp_srv.py >mqttbkp_srv_log.txt 2>&1 &
echo started ok

sleep 3

echo mqttbkp_srv started with ps:
ps | grep python


sleep 2
echo start rest_srv...

source ./venv/bin/activate && nohup python3 ./rest_srv.py >rest_srv_log.txt 2>&1 &
echo started ok

sleep 3

echo servers started with ps:
ps | grep python

echo TODO: change ps grepping to pgrep
