import time
import os
import vlc
from gpiozero import Button, LED

video_folder = "/home/cyrillappert/videos"

button = Button(2) #3

led_green = LED(17) #11
led_blue = LED(27) #13

# GROUND #6
# GROUND #14


video_files = sorted([os.path.join(video_folder, f) for f in os.listdir(video_folder) if f.endswith(('.mp4', '.avi', '.mkv'))])
black_image = "/home/cyrillappert/black.jpg"

instance = vlc.Instance()
player = instance.media_player_new()

while True:

    led_green.on()
    led_blue.off()

    media = vlc.Media(black_image)
    player.set_media(media)
    player.play()
    time.sleep(1)

    button.wait_for_press()

    led_green.off()
    led_blue.on()

    if (video_files):
        for video_file in video_files:
            media = vlc.Media(video_file)
            player.set_media(media)
            player.play()
            time.sleep(1)
            while player.is_playing():
                pass  # Warte, bis das aktuelle Video zu Ende ist
    else:
        print('No files on Memory Stick')
