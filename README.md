# Poor mans BashBunny with RGB-LED

forked from x821938/PoorMansBashBunny

All credits belong there!

The purpose of this fork is to get a better support of the bunny script language.

## Read more about the original project here:

Read all about the project at https://www.cron.dk/poor-mans-bash-bunny/

For very little money (about 1/10th of the real BashBunny) you can make a clone with many of the same powerfull features.

## Changes I made in this fork:
- Changed GPIO-PINs
- RGB led instead of two single-color leds
- Support for a RGB-LED (compatible to bash bunnys LED-command)
- Added RUN command from hak5 (still porting it)
- Increased size of STORAGE to 256MB
- Set an alias Q=QUACK (for better bunnyscript support)
- Started adding a german keyboard layout

## Materials
- Raspberry Pi Zero (Wifi)
- Pi Zero USB Stem
- DIP switch with 4 switches
- 2 x Button
- RGB-LED
- 3 x 330R resistors (470R might work as well)

## GPIO-Layout:
(specified in bin/bunny-launcher.py)
- LED_RED with a 330 or 470 Ohm resistor to GPIO5 (I used two )
- LED_GREEN with a 330 or 470 Ohm resistor to GPIO11
- LED_BLUE with a 330 or 470 Ohm resistor to GPIO9
- button_green to GPIO13 and GND
- button_red to GPIO19 and GND
- DIP-Switches to GPIO2, GPIO3, GPIO4, GPIO17 and GND

## Install
```
> sudo su
# apt install -y git
# git clone https://github.com/x821938/PoorMansBashBunny.git /bunny
# cd /bunny
# ./setup.sh
```

## Cool ideas for the future:
- User zero pi w to open a wifi hotspot and allow some kind of remote control
- Add an i2c display

## Images

![PoorMansBashBunny with RGB LED](https://raw.githubusercontent.com/schneebonus/PoorMansBashBunny/master/images/poorbunny.jpg)
Image of my poorly soldered Bunny with a Frankenstein-Resistor-Constructions (3 x 470 Ohm would be a better solution).
Buttons and dip-switches are similar to the original project but I removed the two single-color leds and replaced them with one rgb led.



## PoorMansBashBunny vs real hak5 BashBunny:

#### Features

|   | pi zero w | bashbunny
| ------------- | ------------- | ------------- |
| Processor | 1GHz, single-core CPU | ? GHz, quad-core CPU |
| RAM | 512MB RAM | 512MB RAM |
| Storage | micro sd card | desktop-class 8 GB SSD |
| WiFi | Yes | No |
| Bluetooth 4.0 | Yes | No |
| free GPIOs | Yes | ? |
| Support | I don't offer any support! | Yes |
| Serious appearance | It's a lump soldered together | Nice and solid case |
| Reliability | It's a lump soldered together and combined with some scripts | It's a professional tool |
| Ducky Script Support | Yes | Yes |
| Bunny Script Support | Partially | Yes |

#### Conclusion
BashBunny:
- Faster
  - shorter boot times
  - faster attack
- more reliable
- better support
- does not look suspicious
- **should be your choice for real pentests!**

PoorMansBashBunny:
- very cheap
- might offer additional possibilities throuch wifi and bluetooth
- GPIOs for extentions
- **good for learning and building**
