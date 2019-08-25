# Hardware

There are many ways to build and compete in the Firefly Challenge. The
hardware outlined here is what we have chosen. We know this
configuration works as a complete system. However you are welcome to
change any or all of these components.

You can get all of these components from multiple vendors and it pays
to shop around. For convenience will supply Amazon links and prices at
the time of this writing (August 2019).

## Tiny Whoop

The most basic component of the system is the quadcopters itself. We
have focussed on the Tiny Whoop class quadcopters because they are
small, reasonable cheap and generally safe around humans.

While the Firefly technology can easily control larger quadcopters,
actually flying larger quadcopters rapidly increases the danger to
participants and spectators. Think very carefully before you automate
a larger quadcopter. We make no safety warranties on any quadcopter
including Tiny Whoops. You need to factor in human safety into all of
your plans for testing and in competitions.

There an many tens of different Tiny Whoops to choose from and while
the spec'ed system can support many of them you will need to make sure
the quadcopter's command protocol is compatible with the hardware you
choose. We have chosen the BETAFPV for our initial quadcopter and that
means we are supporting the Frsky protocol. If you choose a quadcopter
using a different protocol you may have to make modifications to your
hardware and software. If you do this please share your configuration
and experience with us to add to the list of supported hardware.

| Part                                                                                                      | Cost |
| --- | --- |
|[BETAFPV Beta65 Pro 2 Frsky 2S Brushless Tiny Whoop](https://www.amazon.com/gp/product/B07MNG2J6D)|$99.99|
|[BETAFPV battery charger](https://www.amazon.com/BETAFPV-Charger-Board-Battery-Adapter/dp/B072BXBSX5)|$29.99|
|[Additional BETAFPV batteries](https://www.amazon.com/BETAFPV-Battery-Powerwhoop-Connector-Inductrix/dp/B07FFTVB8C)|$27.59|


## NVIDIA Jetson Nano

To perform image processing and make flight path decisions we are
using an NVIDIA Nano. We decided to use an external 4 amp power supply
since we plan to power several USB devices directly from the Nano and
to push the GPU hard. Before this supply will work you must insert a
jumper on J48. You can find more instructions
[here](https://devtalk.nvidia.com/default/topic/1048640/jetson-nano/power-supply-considerations-for-jetson-nano-developer-kit/).

Similarly, because we plan to push the GPU hard we suggest adding an
external fan to the heat sink. The fans definitely turn on when
installing OpenCV. You can either use screws or small zip ties to
attach the fan to the heatsink.

| Part                                                                                                      | Cost |
| --- | --- |
|[NVIDIA Jetson Nano Developer Kit](https://www.amazon.com/gp/product/B07PZHBDKT)|$99.00|
|[SMAKN DC 5V/4A 20W Switching Power Supply](https://www.amazon.com/gp/product/B01N4HYWAM)|$8.99|
|[Samsung 128GB MicroSDXC Memory Card](https://www.amazon.com/gp/product/B06XWZWYVP)|$19.99|
|[Edimax Wi-Fi USB Adapter](https://www.amazon.com/Edimax-EW-7811Un-150Mbps-Raspberry-Supports/dp/B003MTTJOY)|$9.99|
|[Noctua NF-A4x20 5V PWM, Premium Quiet Fan](https://www.amazon.com/gp/product/B071FNHVXN)|$14.95|


## FPV Video Receiver

To capture the first person video coming from the quadcopter we use a
FPV receiver. This converted the video into a digital signal and send
to to the computer over USB.

| Part                                                                                                      | Cost |
| --- | --- |
|[EACHINE ROTG02 FPV Receiver](https://www.amazon.com/gp/product/B07NNH93NX)|$36.99|


## Multi-protocol Transmitter

To command the quadcopter's flight path we use a Multi-protocol
Transmitter module. The module we use requires a 5V serial signal. To
convert from the 5V signal into the USB needed by the NVIDIA Nano we
use a Arduino Leonardo. The Leonardo is programed to translate the
commands from the NVIDIA Nano into the correct signaling to the
Multi-protocol Transmitter Module.

Right now we are only supporting Frsky, but this hardware can command
most types of quadcopters on the market today.

| Part                                                                                                      | Cost |
| --- | --- |
|[4-in-1 2.4G Mutlti-Protocol Transmitter Module](https://www.amazon.com/ARRIS-Jumper-Mutltiprotocol-Transmitter-Module/dp/B07D76QRNS)|$59.98|
|[Arduino Leonardo](https://www.amazon.com/Solu-Leonardo-Compatible-Revision-Atmega32u4)|$9.99|
