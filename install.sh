sudo apt-get update
sudo apt-get install \
    python-dev \
    python-pip \
    python-virtualenv

virtualenv findbots
source findbots/bin/activate

curl -O http://geolite.maxmind.com/download/geoip/database/GeoLite2-City.mmdb.gz
gunzip GeoLite2-City.mmdb.gz

pip install -e git+https://github.com/rory/apache-log-parser.git#egg=apache-log-parser \
            -e git+https://github.com/selwin/python-user-agents.git#egg=python-user-agents \
            colorama \
            geoip2 \
            netaddr 