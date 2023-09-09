#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import sys
import time
import logging
import spidev as SPI
from PIL import Image, ImageDraw, ImageFont, ImageSequence

sys.path.append("..")
from lib import LCD_2inch

RST = 27
DC = 25
BL = 18
bus = 0
device = 0

logging.basicConfig(level=logging.DEBUG)

try:
    disp = LCD_2inch.LCD_2inch()
    disp.Init()
    disp.clear()

    # Get list of GIFs in the folder
    folder_path = '../pic/imgs'
    gif_files = [f for f in os.listdir(folder_path) if f.endswith('.gif')]

    # Loop indefinitely
    while True:
        for gif_file in gif_files:
            gif_path = os.path.join(folder_path, gif_file)
            gif_image = Image.open(gif_path)
            
            start_time = time.time()
            
            # Loop through each frame in the GIF
            for frame in ImageSequence.Iterator(gif_image):
                frame = frame.convert("RGB")
                frame = frame.resize((disp.height, disp.width))
                frame = frame.rotate(180)
                disp.ShowImage(frame)
                time.sleep(0.02)  # Adjust this to change frame speed

                # Break if 20 seconds have passed
                if time.time() - start_time >= 20:
                    break

except IOError as e:
    logging.info(e)
except KeyboardInterrupt:
    disp.module_exit()
    logging.info("quit:")
    exit()
