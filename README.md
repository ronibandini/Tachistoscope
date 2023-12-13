# Tachistoscope
Indoctrination video machine based on James Vicary experiment. 

# Parts
Raspberry Pi 2 or 3 https://www.dfrobot.com/product-1703.html?tracking=hOuIhw4fDaJRTdy4abz04npbQC78dqxBkqVt7XMFYxEXj2s0ukWgm71wbut0ewUP
7 segment 4 digit display https://www.dfrobot.com/product-1966.html?tracking=hOuIhw4fDaJRTdy4abz04npbQC78dqxBkqVt7XMFYxEXj2s0ukWgm71wbut0ewUP
1 x push button https://www.seeedstudio.com/16mm-Anti-vandal-Metal-Push-Button-Glory-Gold-p-1314.html?queryID=360c5e3a2e22ac8297fe9b923678956a&objectID=1557&indexName=bazaar_retailer_products
2 x selector switch 
3d printed enclosure https://cults3d.com/en/3d-model/gadget/tachistoscope
3.5 jack to RCA cable
CCTV CRT monitor 
3A Power Supply https://www.dfrobot.com/product-1937.html?tracking=hOuIhw4fDaJRTdy4abz04npbQC78dqxBkqVt7XMFYxEXj2s0ukWgm71wbut0ewUP

# Circuit
7 seg display to GND y VCC. Clk pin to GPIO5, DIO pint to GPIO4
LED to GPIO2 and GND
Play switchPin to GPIO3 and GND
Download button to GPIO17 and GND.
ChatGPT switch to GPIO27 and GND.

# Instructions
Install Raspberry Pi OS Desktop. Then run:
sudo pip3 install openai
pip install raspberrypi-tm1637
python -m pip install pytube
pip3 install youtube-search-python

Create 3 folders at root
root/frames
root/images
root/videos

# Demo

https://www.youtube.com/watch?v=ekUkft61Jwg

# More information
English https://hackaday.io/project/194031-tachistoscope
Spanish https://bandini.medium.com/indoctrinator-notas-para-fabricar-la-m%C3%A1quina-de-adoctrinamiento-673c6211b670

# Limitation
This version is fully functional but does not include automatic video download and ChatGPT frame inserts.
You should download a video first and rename it as /videos/episode1.mp4
You can edit the frame insert at images/insertframesource.png

# Contact 
Roni Bandini, @RoniBandini
