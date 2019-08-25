# Setting up the NVIDIA Nano

This will describe the one step by step process you can use to setup
an NVIDIA Nano for the Firefly challenge. It tries to be complete and
explain the rationale for the choices made.

If you are using a Edimax ew-7811un USB Wifi then insert it into the
USB port now. If you are using another networking option then connect
it. We want this done early because if there is a network connection
available during the standard NVIDIA setup, it will initial the
connection and update the software. This is a good thing to do.

Because we plan to power several USB devices directly from the Nano
and push the GPU hard, we decided to use an external 4 amp power
supply. Before this supply will work you must insert a jumper on
J48. You can find more instructions
[here](https://devtalk.nvidia.com/default/topic/1048640/jetson-nano/power-supply-considerations-for-jetson-nano-developer-kit/).

Similarly, because we plan to push the GPU hard we suggest adding an
external fan to the heat sink. The fans definitely turn on when
installing OpenCV. You can either use screws or small zip ties to
attach it to the heatsink.

With the hardware set up complete, begin by following NVIDIA's offical
[Getting Started With Jetson Nano Developer Kit](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit).

When using Edimax ew-7811un we have noticed it dropping connections as
discussed
[here](https://devtalk.nvidia.com/default/topic/1049303/jetson-nano/jetson-nano-wifi-/post/5329699/#5329699). You
might want to do this early in your setup and then reboot. We followed
their recommended procedure of adding the rtl8192cu driver to the
blacklist. Open up a terminal and type:

```
echo "blacklist rtl8192cu" | sudo tee -a /etc/modprobe.d/blacklist.conf
```


## Installing OpenCV 4.1.0

To install OpenCV 4.1.0 follow the plan outlined on this
[page](https://devtalk.nvidia.com/default/topic/1049296/jetson-nano/how-to-install-opencv-python-for-python3-6/2).

First we need to create a large enough swap file and add it to the system:

```
sudo fallocate -l 4.0G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

Then enable swapfile after reboot, sudo edit `/etc/fstab` and add:

```
/swapfile none swap 0 0
```

Now get the script to delete the old OpenCV and install the new:

```
git clone https://github.com/AastaNV/JEP
```

Copy the 4.0.0 into a 4.1.0:

```
cd JEP/script
cp install_opencv4.0.0_Nano.sh install_opencv4.1.0_Nano.sh
```

Edit `install_opencv4.1.0_Nano.sh` and globally replace 4.0.0 with 4.1.0.

Now create a directory to build in and start the script:

```
mkdir ~/opencv4.1.0
./install_opencv4.1.0_Nano.sh ~/opencv4.1.0
```
