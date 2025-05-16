#!/bin/bash

echo "🔍 Updating package lists..."
sudo apt update

echo "📦 Installing ClamAV and ClamAV daemon..."
sudo apt install -y clamav clamav-daemon

echo "🛑 Stopping ClamAV services to update virus definitions..."
sudo systemctl stop clamav-freshclam

echo "🔄 Updating virus database..."
sudo freshclam

echo "✅ Restarting ClamAV services..."
sudo systemctl start clamav-freshclam
sudo systemctl enable clamav-freshclam
sudo systemctl enable clamav-daemon


