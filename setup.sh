#!/bin/bash

# Install chromium
sudo apt update
sudo apt install chromium-browser

# Install chromedriver
# https://chromedriver.chromium.org/downloads
wget https://chromedriver.storage.googleapis.com/110.0.5481.77/chromedriver_linux64.zip
unzip chromedriver*
sudo chmod +x chromedriver
sudo cp chromedriver /usr/bin/chromedriver

# Install firefox
sudo apt update
sudo apt install firefox

# Install geckodriver
# 
wget https://github.com/mozilla/geckodriver/releases/download/v0.32.2/geckodriver-v0.32.2-linux64.tar.gz
tar -xvzf geckodriver*
sudo chmod +x geckodriver
sudo cp geckodriver /usr/local/bin/