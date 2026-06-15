import time
import vlc
from gpiozero import Button, LED, Device
from gpiozero.pins.lgpio import LGPIOFactory

Device.pin_factory = LGPIOFactory()

# --- Configuration ---
STANDBY_VIDEO = "/home/eva/rpi3-player-button/media/standby.mp4"

VIDEO_1 = "/home/eva/rpi3-player-button/media/cobalt.mp4"
VIDEO_2 = "/home/eva/rpi3-player-button/media/rre.mp4"
VIDEO_3 = "/home/eva/rpi3-player-button/media/tantalum.mp4"

BUTTON_1_PIN = 2
BUTTON_2_PIN = 3
BUTTON_3_PIN = 4

LED_STANDBY_PIN = 17
LED_PLAYING_PIN = 27
# --- End Configuration ---

button1 = Button(BUTTON_1_PIN)
button2 = Button(BUTTON_2_PIN)
button3 = Button(BUTTON_3_PIN)

led_standby = LED(LED_STANDBY_PIN)
led_playing = LED(LED_PLAYING_PIN)

COOLDOWN = 2.0  # seconds before another video can be triggered

instance = vlc.Instance()
player = instance.media_player_new()

in_standby = True
last_trigger = 0.0


def show_standby():
    global in_standby
    in_standby = True
    led_standby.on()
    led_playing.off()
    media = instance.media_new(STANDBY_VIDEO)
    player.set_media(media)
    player.play()


def play_video(path):
    global in_standby, last_trigger
    now = time.time()
    if now - last_trigger < COOLDOWN:
        return
    last_trigger = now
    in_standby = False
    led_standby.off()
    led_playing.on()
    media = instance.media_new(path)
    player.set_media(media)
    player.play()


button1.when_pressed = lambda: play_video(VIDEO_1)
button2.when_pressed = lambda: play_video(VIDEO_2)
button3.when_pressed = lambda: play_video(VIDEO_3)

show_standby()

while True:
    time.sleep(0.1)
    state = player.get_state()
    if state == vlc.State.Ended:
        show_standby()
