# About

mqtt db client
db to rest server

# install in opkg
install python, curl, git

    opkg update
    opkg upgrade
    opkg install python
    opkg install curl
    opkg install git
    opkg install git-http

clone repo

    mkdir applications
    cd applications
    git clone https://github.com/savinoff/router_rest_srv.git
    cd router_rest_srv
    
make venv
    
    ~/applications/router_rest_srv # python -m venv --without-pip venv
    ~/applications/router_rest_srv # source venv/bin/activate
    (venv) ~/applications/router_rest_srv # curl https://bootstrap.pypa.io/get-pip.py | python
    (venv) ~/applications/router_rest_srv # deactivate
    ~/applications/router_rest_srv # source venv/bin/activate
    (venv) ~/applications/router_rest_srv # python -m pip install -r requirements.txt

run service

    (venv) ~/applications/router_rest_srv # ./start.sh

