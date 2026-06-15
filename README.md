# rpi3-player-button

Button-triggered video player for Raspberry Pi 3 using VLC and GPIO.

Plays a standby video in a loop. Pressing a button interrupts and plays the assigned video, then returns to standby.

## Pinout

| Button | GPIO | Video |
|--------|------|-------|
| 1 | GPIO 2 | cobalt.mp4 |
| 2 | GPIO 3 | rre.mp4 |
| 3 | GPIO 4 | tantalum.mp4 |

## Videos

Place videos in `media/`. Required files:

- `standby.mp4` — loops when idle
- `cobalt.mp4`, `rre.mp4`, `tantalum.mp4` — triggered by buttons

Videos must be **1080p or below**. The RPi3 hardware decoder maxes out at 1920x1080.

### Transcoding 4K source

4K (3840x1920) source must be scaled down. Transcode to 1920x960 to stay within
limits while keeping the 2:1 aspect ratio (use `scale=1280:640` if still choppy):

```bash
sudo apt install ffmpeg
for f in cobalt rre tantalum standby; do
  ffmpeg -i media/${f}.mp4 -vf scale=1920:960 \
    -c:v libx264 -profile:v main -level 4.0 -preset fast -crf 23 \
    -c:a aac media/${f}_scaled.mp4
  mv media/${f}_scaled.mp4 media/${f}.mp4
done
```

## Setup

```bash
sudo apt install vlc libvlc-dev liblgpio-dev python3-dev swig
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Service

Installs as a systemd service that starts on boot:

```bash
sudo cp player.service /etc/systemd/system/
sudo systemctl daemon-reload && sudo systemctl enable --now player
```
