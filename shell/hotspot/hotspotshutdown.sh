#!/usr/bin/env bash

echo "Deleting iptables entries..."
iptables --table nat --delete POSTROUTING --out-interface new0 -j MASQUERADE
iptables --delete FORWARD --in-interface new1 -j ACCEPT
sleep 1

echo "Killing existing in-terminal services..."
kill $(ps a | grep "wpa_supplicant" | awk '{print $1}')
kill $(ps a | grep "hostapd" | awk '{print $1}')
kill $(ps a | grep "udhcpc" | awk '{print $1}')
sleep 5

echo "Disable IP forwarding & Network Adress Translating"
echo "0" > /proc/sys/net/ipv4/ip_forward
sleep 2

echo "Stopping udhcpd..."
service udhcpd stop

echo "Pulling down new0 new1 interfaces..."
ifconfig new0 down
ifconfig new1 down
iw dev new0 del
iw dev new1 del
sleep 1

echo "Unblocking phy0..."
rfkill unblock 3
sleep 5

echo "Starting Network Manager"
service network-manager start
