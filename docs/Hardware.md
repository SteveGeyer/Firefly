# Hardware

There many ways to build and compete in the Firefly Challenge. The
hardware outlined here is what we have chosen. We also know it works
as a complete system. However you are welcome to change any or all of
these components.

While we will supply a list of parts and their cost on Amazon at the
time of this writing (August 2019), you can get all of these
components elsewhere and maybe at a better price. Shop around.


## Tiny Whoop

The most basic component of the system is the drone itself. We have
focussed on the Tiny Whoop class quadcopters because they are small,
reasonable cheap and are safe around humans. While the Firefly
technology can easily control a larger drone it does increase the
danger to participants and spectators. Think carefully before you
automate a larger drone.

There an many tens of different Tiny Whoops to choose from and while
the spec'ed system can support many of them you will need to make sure
the drone command protocol is compatible with your hardware. We have
choosen the BETAFPV for our initial drone and that means we are
supporting the Frsky protocol. If you choose a drone using a different
protocol you may have to make modifications to your hardware and
software. If you do this please share your configuration and
experience with us to add to the list of supported hardware.

| Part                                                                                   | Cost |
| --- | --- |
|[BETAFPV Beta65 Pro 2 Frsky 2S Brushless Tiny Whoop](https://www.amazon.com/gp/product/B07MNG2J6D)|$99.99|
|[BETAFPV battery charger](https://www.amazon.com/BETAFPV-Charger-Board-Battery-Adapter/dp/B072BXBSX5)|$29.99|
|[Additional BETAFPV batteries](https://www.amazon.com/BETAFPV-Battery-Powerwhoop-Connector-Inductrix/dp/B07FFTVB8C)|$27.59|


## NVIDIA Jetson Nano

To perform image processing and make flight path decisions we are
using an NVIDIA Nano. Because we plan to power several USB devices
directly from the Nano and push the GPU hard, we decided to use an
external 4 amp power supply. Before this supply will work you must
insert a jumper on J48. You can find more instructions
[here](https://devtalk.nvidia.com/default/topic/1048640/jetson-nano/power-supply-considerations-for-jetson-nano-developer-kit/).

Similarly, because we plan to push the GPU hard we suggest adding an
external fan to the heat sink. The fans definitely turn on when
installing OpenCV. You can either use screws or small zip ties to
attach it to the heatsink.

| Part                                                                                   | Cost |
| --- | --- |
|[NVIDIA Jetson Nano Developer Kit](https://www.amazon.com/gp/product/B07PZHBDKT)|$99.00|
|[SMAKN DC 5V/4A 20W Switching Power Supply](https://www.amazon.com/gp/product/B01N4HYWAM)|$8.99|
|[Samsung 128GB MicroSDXC Memory Card](https://www.amazon.com/gp/product/B06XWZWYVP)|$19.99|
|[Edimax Wi-Fi USB Adapter](https://www.amazon.com/Edimax-EW-7811Un-150Mbps-Raspberry-Supports/dp/B003MTTJOY)|$9.99|
|[Noctua NF-A4x20 5V PWM, Premium Quiet Fan](https://www.amazon.com/gp/product/B071FNHVXN)|$14.95|


## FPV Video Receiver

To capture the first person video coming from the drone we use a FPV
reviever. This converted the video into a digital signal and send to
to the computer over USB.

| Part                                                                                   | Cost |
| --- | --- |
|[EACHINE ROTG02 FPV Receiver](https://www.amazon.com/gp/product/B07NNH93NX)|$36.99|


## Multi-protocol Transmitter

To command the drone's flight path we use a Multi-protocol Transmitter
module. It module we use requires a 5V serial signal. To convert from
the 5V signal into the USB needed by the NVIDIA Nano we use a Arduino
Leonardo. The Leonardo is programed to translate the commands from the
NVIDIA Nano into the correct signalling to the Multi-protocol
Transmitter Module.

Right now we are only supporting Frsky, but this hardware can command
most types of drones on the market today.

| Part                                                                                   | Cost |
| --- | --- |
|[4-in-1 2.4G Mutlti-Protocol Transmitter Module](https://www.amazon.com/ARRIS-Jumper-Mutltiprotocol-Transmitter-Module/dp/B07D76QRNS)|$59.98|
|[Arduino Leonardo](https://www.amazon.com/Solu-Leonardo-Compatible-Revision-Atmega32u4)|$9.99|
