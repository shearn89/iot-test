# IOT-EnviroPi #

Simple python script to send data to https://app.initialstate.com

Collects all data from the Enviro pHAT and sends it up to the cloud.

## Installation ##

* Copy `enviropi.service` to `/etc/systemd/system/`
* `systemctl enable enviropi.service`
* `systemctl start enviropi.service`
