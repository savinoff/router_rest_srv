# About

mqtt db client
db to rest server

# install in opkg
install python, curl, git

    opkg update
    opkg upgrade
    opkg install python3
    opkg install curl
    opkg install git
    opkg install git-http

clone repo

    mkdir ~/applications
    cd ~/applications
    git clone https://github.com/savinoff/router_rest_srv.git
    cd router_rest_srv
    
make venv
    
    python -m venv --without-pip venv
    source venv/bin/activate
    curl https://bootstrap.pypa.io/get-pip.py | python
    deactivate

activate and install dependencies

    ~/applications/router_rest_srv # source venv/bin/activate
    (venv) ~/applications/router_rest_srv # python -m pip install -r requirements.txt

configure

    (venv) ~/applications/router_rest_srv # cp config.example.py config.py 
    (venv) ~/applications/router_rest_srv # vim config.py 

run service

    ~/applications/router_rest_srv # ./start.sh

