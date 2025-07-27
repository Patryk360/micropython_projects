from camera import Camera, GrabMode, PixelFormat, FrameSize, GainCeiling
from machine import SDCard
from time import sleep, localtime
import os
sd = SDCard(slot=0, sck=39, cmd=38, data=(40,))
os.mount(sd, "/sd")
t = localtime()

folder = "/sd/{:04d}-{:02d}-{:02d}".format(t[0], t[1], t[2])
filename = "{:02d}-{:02d}-{:02d}.jpg".format(t[3], t[4], t[5])
full_path = "{}/{}".format(folder, filename)

if folder[4:] not in os.listdir("/sd"):
    os.mkdir(folder)

cam = Camera(frame_size = FrameSize.WQXGA, pixel_format=PixelFormat.JPEG, grab_mode=GrabMode.LATEST, jpeg_quality=98, fb_count=2)

cam.init()

img = cam.capture()

with open(full_path, "wb") as f:
    f.write(img)

cam.free_buffer()