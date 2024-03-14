[Back to main README.md](../../README.md)

# Octoprint

3D printer automation/monitoring

<https://github.com/OctoPrint/OctoPrint>

<https://github.com/OctoPrint/octoprint-docker>

<https://hub.docker.com/r/octoprint/octoprint>

## Architecture Compatibility

![x64 Version](https://img.shields.io/docker/v/octoprint/octoprint/latest?arch=amd64&label=x64) ![Arm64 Version](https://img.shields.io/docker/v/octoprint/octoprint/latest?arch=arm64&label=arm64)

### WebUI Dashboard

![Octoprint UI](../../resources/screenshots/octoprint.webp)

#### IP Camera

The internal MJPEG-streamer can be accessed outside of the container (ie: by homeassistant as an IP camera).

`http://<host_ip>:<octprint_port>/webcam/?action=stream`

`http://<host_ip>:<octprint_port>/webcam/?action=snapshot`
https://manpages.ubuntu.com/manpages/jammy/man1/ustreamer.1.html

https://github.com/pikvm/ustreamer

https://www.reddit.com/r/OrangePI/comments/127vfid/orange_pi_4_lts_gpio_and_mainsailmoonrakerklipper/

To determine Orange pi pin, gpiod gpioinfo, take line number % 32. Whole number = /dev/gpiochipX remainder = line/pin #. Board pin 40 = line 121 % 32 = 3 R 25, /dev/gpiochip3 25

Had to run `sudo apt remove brltty`
https://github.com/juliagoda/CH341SER/issues/18
