# RasPiML
A person tracker using a RaspberryPi

## Hardware Requirements
- RaspberryPi 3B+ and above with minimum 1GB of Memory
- A servo motor with 5 volts
- Any camera module for the RaspberryPi
- Female-to-Male jumper cables

## Software Requirements
- Wiring Pi
- OpenCV 4
- ONNX runtime

## Setup
#### Hardware Setup
#### Software Setup
OpenCV is needed to control our camera module. To install OpenCV for the Raspberry Pi, run the following line on your terminal:
```
sudo apt-get install libopencv-dev
```

Wiring Pi is needed for controlling the servo motor. To install Wiring Pi, run the following commands:
```
sudo apt-get purge wiringpi
hash -r
sudo apt-get install git

git clone https://github.com/WiringPi/WiringPi.git
cd WiringPi
./build
```
## Building and Executing Software
