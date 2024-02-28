#!/bin/bash

ampy --port /dev/ttyACM0 reset
ampy --port /dev/ttyACM0 run main.py

