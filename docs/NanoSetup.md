# Setting up the NVIDIA Nano

This will describe the one step by step process you can use to setup
an NVIDIA Nano for the Firefly challenge. It tries to be complete and
explain the rationale for the choices made.

If you are using a Edimax ew-7811un USB Wifi then insert it into the
USB port now. If you are using another networking option then connect
it. We want this done early because if there is a network connection
available during the standard NVIDIA setup, it will initialize the
connection and update some software. This is a good thing to do.

We decided to use an external 4 amp power supply since we plan to
power several USB devices directly from the Nano and to push the GPU
hard. Before this supply will work you must insert a jumper on
J48. You can find more instructions
[here](https://devtalk.nvidia.com/default/topic/1048640/jetson-nano/power-supply-considerations-for-jetson-nano-developer-kit/).

Similarly, because we plan to push the GPU hard we suggest adding an
external fan to the heat sink. The fans definitely turn on when
installing OpenCV. You can either use screws or small zip ties to
attach the fan to the heatsink.

With the hardware set up complete, begin by following NVIDIA's official
[Getting Started With Jetson Nano Developer Kit](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit).

When using Edimax ew-7811un we have noticed it dropping connections as
discussed
[here](https://devtalk.nvidia.com/default/topic/1049303/jetson-nano/jetson-nano-wifi-/post/5329699/#5329699).
You might want to deal the the dropping connections early in your
setup and then reboot. We followed their recommended procedure of
adding the rtl8192cu driver to the blacklist. Open up a terminal and
type:

```
echo "blacklist rtl8192cu" | sudo tee -a /etc/modprobe.d/blacklist.conf
```


## Installing OpenCV 4.1.0

This following step installs a reasonably current version of OpenCV
and most important the contrib library which contains the Aruco
fiducial marker detector. The version pre-installed by NVIDIA lacks
both the contrib directory and Aruco in particular.

To install OpenCV 4.1.0 follow the plan outlined on this
[page](https://devtalk.nvidia.com/default/topic/1049296/jetson-nano/how-to-install-opencv-python-for-python3-6/2).

First we need to create a large enough swap file and add it to the
system. If you don't increase the swap file before starting the build
you get see low memory errors and the build will crawl to a stand
still:

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

Now get the OpenCV 4 install script:

```
git clone https://github.com/AastaNV/JEP
```

Copy the 4.0.0 into a 4.1.0:

```
cd JEP/script
cp install_opencv4.0.0_Nano.sh install_opencv4.1.0_Nano.sh
```

Edit `install_opencv4.1.0_Nano.sh` and globally replace 4.0.0 with 4.1.0.

Finally create a directory to build in and start the script:

```
mkdir ~/opencv
./install_opencv4.1.0_Nano.sh ~/opencv
```

The build and install process takes several hours to complete. You
will also notice that the external fan will come on at various times
during this process.

# Camera calibration

This is a good time to build the camera calibration code.  Following
the instructions
[here](https://docs.opencv.org/4.1.0/d4/d94/tutorial_camera_calibration.html)
we need to build the calibration program. In OpenCV's sample directory
is this program and it takes live video or a series of images from the
camera and infers the distortion coming from the camera.

Unfortunately you need to do several steps to get this executable
built. OpenCV 4.0 no longer creates the necessary information for
`pkg-config` eliminating the possibility of a simple, one-line,
command to build camera_calibration in its source directory. We must
instead us `cmake`. So we are going to copy the source into a
temporary directory, create the `CMakeLists.txt` and `default.xml`
file, build and finally calibrate.

If you checkout this repository to your Nano you can skip the setup
sets follow the build steps below.

## Quadcopter On Screen Display

Before running the camera calibration it might be a good idea to
disable the On Screen Display (OSD). This will give the image process
the maximum ability to process the incoming image without having any
part of the image obscured.

If you controller is using BetaFlight it is as easy as connecting the
quadcopter to your computer running the BetaFlight Configurator,
clicking the OSD tab, disabling all OSD outputs, and hitting save.

## Setup

Start by copying the source code into a working directory. This
example chooses the directory `~/calibrate`.

```
cp -r ~/opencv/opencv-4.1.0/samples/cpp/tutorial_code/calib3d/camera_calibration ~/calibrate
```

Create file `~/calibrate/CMakeLists.txt` and populate with:
```
cmake_minimum_required(VERSION 3.0)
project(camera_calibration)
find_package(OpenCV REQUIRED)
add_executable(camera_calibration camera_calibration.cpp)
target_link_libraries(camera_calibration ${OpenCV_LIBS})
```

Then copy `~/calibrate/in_VID5.xml` to `~/calibrate/default.xml` and
edit for your particle training choice. In this example we will
capture the images live from the camera and device location 0. So we
edit the `<Input>` to be zero `<Input>"0"</Input>`. Notice the quotes
around the 0, they seem to be required.

## Build

Now build it.

```
cd ~/calibrate
mkdir build
cd build
cmake ..
make
```

## Run camera_calibration

At this time follow the instructions on using the calibration program
as described
[here](https://docs.opencv.org/4.1.0/d4/d94/tutorial_camera_calibration.html).

# Load packages

## screen to testing

```
sudo apt-get install screen
```

## Pip and then pyserial

NEED TO DOUBLE CHECK THIS ON A FRESHLY install flash drive. First make sure that

The `pyserial` package need to be installed so that we can command the
transmitter. First we will install the `pip` command.

```
wget https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
rm get-pip.py
```

Next install `pyserial`:

```
pip3 install pyserial
```

or maybe

```
sudo pip3 install pyserial
```

Now test that it is installed

```
python3
>>> import serial
```


# Add user to dialout group

We need to add the user to the `dialout` group so that they can open a
serial line without requiring root permissions:

```
sudo usermod -a -G dialout $USER
```
