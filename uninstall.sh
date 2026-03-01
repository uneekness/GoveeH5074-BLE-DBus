#!/bin/bash
systemctl stop govee_ble.service
systemctl disable govee_ble.service
rm /etc/systemd/system/govee_ble.service
systemctl daemon-reload
echo "Govee H5074 BLE → DBus auto-scan service removed."
