Hotspot
=======
Setup hotspot without network using your card.

## Setup
1. copy `./configs/hostapd.conf` to `/etc/hostapd/hostapd.conf`
1. copy `./configs/udhcpd.conf` to `/etc/udhcpd.conf`
1. comment out `DHCPD_ENABLED="no"` in `/etc/default/udhcpd`
