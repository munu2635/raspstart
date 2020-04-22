#! /bin/bash
echo "setting start..."
echo "network_setting"

sed -e "19 i/sudo sh home/pi/raspstart/initSettin/setting1.sh" /etc/rc.local

shdo wpa_passpherase KT_GiGA_2G_Wave2_EE87 ceabdz9996
shdo wpa_passpherase raspberry test1234

sudo reboot 