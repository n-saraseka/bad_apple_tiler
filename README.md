# bad_apple-tiler
 A script for tiling the Bad Apple!! clip with 2 images.

# Required apps
Python ver. 3.0 or later.

# Setting up
Download the code using the *Clone or Download/Download as ZIP* button and extract the archive to your chosen directory. 
You will need 3 files to run the tiling script: **the video** and **2 images** that will be used for tiling. There are example video and images in the repository, but you may replace them with your own.

## Video restrictions
The video has to be at least 240p. There are no restrictions on video's FPS, though.

## Tile restrictions
Tiles must have equal resolution and the video's dimensions should be divisible by tiles's dimensions.

# How to use
Open a command line window in the folder where you've saved the code and input the following:
* Windows:
```
py -m pip install -r requirements.txt
py apple-converter.py
```
* Linux:
```
python3 -m pip install -r requirements.txt
python3 apple-converter.py
```
Follow the instructions given on screen and wait until it finishes tiling. The tiled video will then be saved to a file called **converted.mp4**.
