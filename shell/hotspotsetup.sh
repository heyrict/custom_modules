#!/usr/bin/env bash

echo "Disabling wifi for compatibility problems with tlp..."
wifi off
sleep 1

echo "Stopping Network Manager..."
service network-manager stop
sleep 2

echo "Enabling wifi for compatibility problems with tlp..."
wifi on
sleep 1

#pkill -15 nm-applet
#sleep 1

echo "Pulling down wlp3s0..."
ifconfig wlp3s0 down
sleep 2

echo "Splitting wlp3s0 into two virtual interfaces..."
iw phy phy0 interface add new0 type station
iw phy phy0 interface add new1 type __ap

echo "Change MAC address of both interfaces..."
ifconfig new0 down
macchanger --mac 00:11:22:33:44:55 new0
ifconfig new1 down
macchanger --mac 00:11:22:33:44:66 new1
ifconfig new0 up
ifconfig new1 up
sleep 1

echo "Starting hostapd..."
ifconfig new1 192.168.27.1 up
hostapd /etc/hostapd/hostapd.conf &
sleep 5

echo "Starting udhcpd..."
service udhcpd restart

#echo "Starting wpa_supplicant..."
#wpa_supplicant -inew0 -c/etc/wpa_supplicant/wpa_supplicant.conf &
#sleep 5

echo "Starting udhcpc client..."
udhcpc -i new0 &
sleep 1

echo "Enable IP forwarding & Network Adress Translating"
echo "1" > /proc/sys/net/ipv4/ip_forward
iptables --table nat --append POSTROUTING --out-interface new0 -j MASQUERADE
iptables --append FORWARD --in-interface new1 -j ACCEPT
