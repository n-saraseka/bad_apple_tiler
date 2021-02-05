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

tile1=input('Input the name of the first tile (including the file extension). It will be used for replacing white pixels: ')
tile1 = Image.open(os.path.join(default_path, tile1))
tile2=input('Input the name of the second tile (including the file extension). It will be used for replacing black pixels: ')
tile2 = Image.open(os.path.join(default_path, tile2))

# works with any tiles of same size
t_w, t_h = tile1.size

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
                frame.paste(tile1, (k*10, j*10))
            else:
                frame.paste(tile2, (k*10, j*10))

def numpy_convert():
    for i in range(frame_count):
        frame = Image.fromarray(clip.get_frame((1/clip.fps)*i))
        tile(frame)
        w, h = frame.size
        if (w%120!=0):
            frame = frame.crop((0, 0, w-w%10, h)) #used to eliminate convertion glitches
        frame = numpy.array(frame)
        frames.append(frame)
    print('Writing the converted video file, this may take some time...')
    return ImageSequenceClip(frames, fps=clip.fps)

def PIL_convert():
    os.mkdir(frames_dir)
    for i in range(frame_count):
        clip.save_frame(os.path.join(frames_dir, f'{i}.jpg'), t=(1/clip.fps)*i)
        frame = Image.open(os.path.join(frames_dir, f'{i}.jpg'))
        tile(frame)
        w, h = frame.size
        if (w%10!=0):
            frame = frame.crop((0, 0, w-w%10, h)) #used to eliminate convertion glitches
        frame.save(os.path.join(frames_dir, f'{i}.jpg'))
    print('Writing the converted video file, this may take some time...')
    return ImageSequenceClip([os.path.join(frames_dir, f'{i}.jpg') for i in range(len(os.listdir(frames_dir)))], fps=clip.fps)

quality=int(input('Choose converting quality from 0 to 5 (0 = worst, 5 = best): '))
choice=input('Convert without saving frames to disk (not recommended)? (Y/N) ')
print('Converting...')

if choice=='Y' or choice=='y':
    converted_video = numpy_convert()
elif choice=='N' or choice=='n':
    converted_video = PIL_convert()

if (audio!=None):
    audio.duration = clip.duration
    converted_video.audio = audio
converted_video.write_videofile('converted.mp4', audio=True)
shutil.rmtree(frames_dir, ignore_errors=True)
print('The converted file is now saved to converted.mp4.')