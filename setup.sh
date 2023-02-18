#!/bin/bash

# update
sudo apt update -y 

# Install chromium / driver
sudo apt install chromium-browser chromium-chromedriver -y

# Install firefox driver
sudo apt install firefox firefox-geckodriver -y

# Install ffmpeg
sudo apt install ffmpeg -y

# Install aria2
sudo apt install aria2 -y

# Install python requirements
pip install -r requirements.txt