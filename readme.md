# About

mqtt db client
db to rest server

# run in ubuntu
edit and copy service (user, paths)

    cat rest_srv.service
    nano ~/applications/router_rest_srv/rest_srv.service
    cp ~/applications/router_rest_srv/rest_srv.service /etc/systemd/system

working with rest_srv.service

    sudo systemctl status rest_srv
    sudo systemctl enable rest_srv
    sudo systemctl start rest_srv
    sudo systemctl status rest_srv
    systemctl daemon-reload

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
