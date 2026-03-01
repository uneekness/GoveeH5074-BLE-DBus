#!/bin/bash
pip3 install --user bleak dbus-next govee_ble

cat <<EOT > /etc/systemd/system/govee_ble.service
[Unit]
Description=Govee H5074 BLE sensor auto-scan service
After=network.target

[Service]
ExecStart=/usr/bin/python3 /data/govee_ble_service.py
Restart=always
User=root

[Install]
WantedBy=multi-user.target
EOT

systemctl daemon-reload
systemctl enable govee_ble.service
systemctl start govee_ble.service

echo "Govee H5074 BLE → DBus auto-scan service installed and started."
