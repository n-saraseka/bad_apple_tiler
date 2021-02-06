# bad_apple-tiler
 A script for tiling the Bad Apple!! clip with 2 images.

# Required apps
Python ver. 3.0 or later.

# Setting up
You will need 3 files to run the tiling app: **the video** and **2 images** that will be used for tiling. There are example video and images in the repository, but you may replace them with your own.

## Video restrictions
The video has to be at least 240p, otherwise the code will work incorrectly. There are no restrictions on video's FPS, though.

## Tile restrictions
The tile images have to be of same resolution and your video's dimensions must be divisible by the tiles's dimensions, otherwise the code will work incorrectly.

# How to use
Run the **convert.bat** file. It will automatically install the necessary modules and run the code. Follow the instructions on screen and wait until it finishes tiling. The tiled video will be saved to a file called **converted.mp4**.
