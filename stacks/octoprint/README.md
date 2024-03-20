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


https://www.reddit.com/r/OrangePI/comments/127vfid/orange_pi_4_lts_gpio_and_mainsailmoonrakerklipper/

To determine Orange pi pin, gpiod gpioinfo, take line number % 32. Whole number = /dev/gpiochipX remainder = line/pin #. Board pin 40 = line 121 % 32 = 3 R 25, /dev/gpiochip3 25
https://github.com/orangepi-xunlong/wiringOP

Had to run `sudo apt remove brltty`

https://github.com/juliagoda/CH341SER/issues/18

##### Orange Pi 3B+ Physical Pin -> /dev/gpiochip mapping

| Physical Pin | GPIO Line | Name     | /dev/gpiochipX | line/pin Y |
| ------------ | --------- | -------- | -------------- | ---------- |
| 1            | 3.3v      |          |                |            |
| 2            | 5v        |          |                |            |
| 3            | 140       | SDA.2    | 4              | 12         |
| 4            | 5v        |          |                |            |
| 5            | 141       | SCL.2    | 4              | 13         |
| 6            | GND       |          |                |            |
| 7            | 147       | PWM15    | 4              | 19         |
| 8            | 25        | RXD.2    | 0              | 25         |
| 9            | GND       |          |                |            |
| 10           | 24        | TXD.2    | 0              | 24         |
| 11           | 118       | GPIO3_C6 | 3              | 22         |
| 12           | 119       | GPIO3_C7 | 3              | 23         |
| 13           | 128       | GPIO4_A0 | 4              | 0          |
| 14           | GND       |          |                |            |
| 15           | 130       | TXD.7    | 4              | 2          |
| 16           | 131       | RXD.7    | 4              | 3          |
| 17           | 3.3v      |          |                |            |
| 18           | 129       | GPIO4_A1 | 4              | 1          |
| 19           | 138       | SPI3_TXD | 4              | 10         |
| 20           | GND       |          |                |            |
| 21           | 136       | SPI3_RXD | 4              | 8          |
| 22           | 132       | TXD.9    | 4              | 3          |
| 23           | 139       | SPI3_CLK | 4              | 11         |
| 24           | 134       | SPI3_CS1 | 4              | 6          |
| 25           | GND       |          |                |            |
| 26           | 135       | GPIO4_A7 | 4              | 7          |
| 27           | 32        | SDA.3    | 1              | 0?         |
| 28           | 33        | SCL.3    | 1              | 1?         |
| 29           | 133       | RXD.9    | 4              | 5          |
| 30           | GND       |          |                |            |
| 31           | 124       | GPIO3_D4 | 3              | 28         |
| 32           | 144       | PWM11    | 4              | 16         |
| 33           | 127       | GPIO3_D7 | 3              | 31         |
| 34           | GND       |          |                |            |
| 35           | 120       | GPIO3_D0 | 3              | 24         |
| 36           | 125       | GPIO3_D5 | 3              | 29         |
| 37           | 123       | GPIO3_D3 | 3              | 27         |
| 38           | 122       | GPIO3_D2 | 3              | 26         |
| 39           | GND       |          |                |            |
| 40           | 121       | GPIO3_D1 | 3              | 25         |

[filename](compose.yaml ':include :type=code')