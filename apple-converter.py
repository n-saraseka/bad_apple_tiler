from moviepy.editor import *
from PIL import Image
import numpy
import shutil

default_path = os.path.split(os.path.abspath(__file__))[0]
frames_dir = os.path.join(default_path, 'frames')
frames = [] #for conversion without saving frames to disk
converted_video = 0
video_title=input('Input the name of the video (including the file extension): ')
clip = VideoFileClip(video_title)
frame_count = int(clip.duration*clip.fps)
audio = clip.audio
if (clip.w%10!=0):
        clip = clip.crop(x1=0, x2=clip.w-clip.w%10) #for weird situations when the w:h ratio isn't actually 4:3

tile1=input('Input the name of the first tile (including the file extension). It will be used for replacing white pixels: ')
tile1 = Image.open(os.path.join(default_path, tile1))
tile2=input('Input the name of the second tile (including the file extension). It will be used for replacing black pixels: ')
tile2 = Image.open(os.path.join(default_path, tile2))

# works with any tiles of same size
t_w, t_h = tile1.size

class TileError(Exception):
    print('')

if (tile1.size==tile2.size and clip.w%t_w==0 and clip.h%t_h==0)==False:
    raise TileError("The tiles don't follow at least one of these requirements:\n Tiles must have equal resolution and the video's dimensions should be divisible by tiles's dimensions.")

def tile(frame):
    w, h = frame.size

    resized_frame = frame.resize((w // t_w, h // t_h), resample=quality)
    resized_frame = resized_frame.convert(mode='1')
    w_r, h_r = resized_frame.size

    pixels = resized_frame.load()

    for j in range(h_r):
        for k in range(w_r):
            cpixel = pixels[k,j]
            if cpixel==255:
                frame.paste(tile1, (k*t_w, j*t_h))
            else:
                frame.paste(tile2, (k*t_w, j*t_h))
    return frame

def numpy_convert():
    for i in range(frame_count):
        frame = Image.fromarray(clip.get_frame((1/clip.fps)*i))
        frame = tile(frame)
        frame = numpy.array(frame)
        frames.append(frame)
    print('Writing the converted video file, this may take some time...')
    return ImageSequenceClip(frames, fps=clip.fps)

def pil_convert():
    os.mkdir(frames_dir)
    for i in range(frame_count):
        clip.save_frame(os.path.join(frames_dir, f'{i}.jpg'), t=(1/clip.fps)*i)
        frame = Image.open(os.path.join(frames_dir, f'{i}.jpg'))
        frame = tile(frame)
        frame.save(os.path.join(frames_dir, f'{i}.jpg'))
    print('Writing the converted video file, this may take some time...')
    return ImageSequenceClip([os.path.join(frames_dir, f'{i}.jpg') for i in range(len(os.listdir(frames_dir)))], fps=clip.fps)

quality=int(input('Choose converting quality from 0 to 5 (0 = worst, 5 = best): '))
choice=input('Convert without saving frames to disk (not recommended)? (Y/N) ')
print('Converting...')

if choice=='Y' or choice=='y':
    converted_video = numpy_convert()
elif choice=='N' or choice=='n':
    converted_video = pil_convert()

if (audio!=None):
    audio.duration = clip.duration
    converted_video.audio = audio
converted_video.write_videofile('converted.mp4', audio=True)
shutil.rmtree(frames_dir, ignore_errors=True)