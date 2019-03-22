Access log metrics
==================

Python program for parsing apache/nginx access.logs
1. Filtering bots/indexers using IP blacklist
2. Outputting usage metrics with geolocation

Installation
------------

Download and unzip <a href="http://geolite.maxmind.com/download/geoip/database/GeoLite2-City.mmdb.gz">GeoLite2-City.mmdb.gz</a>

Clone or download git repo. Install python packages using  

```
pip install -r requirements
```

Acknowledgements
----------------

Based on Detecting Bots in Apache & Nginx Logs by Mark Litwintschik  
Blog: https://tech.marksblogg.com/detect-bots-apache-nginx-logs.html  
Gist: https://gist.github.com/marklit/80b875ccab8b215bfa0ecdfaa5000e7b

This product includes GeoLite2 data created by MaxMind, available from
<a href="https://www.maxmind.com">https://www.maxmind.com</a>.