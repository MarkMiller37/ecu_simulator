# openSYDE ECU Simulator

Based on a generic UDS implementation by Luis Alberto Benthin Sanguino.
See base GitHub repository for details.

Modified to mock an ECU using the UDS-based openSYDE protocol.

## What's implemented

Connect from openSYDE Dashboard basically works:

* get current session
* activate extended session
* request seed and send key
* extract datapool names and versions
* check data pool version
* send data rates
* confirmed read
* cyclic and event based read

## Ideas for improvement

Datapool configuration is currently hard-coded in services.py.
This could be created from an openSYDE project by creating a derivative of
 the SYDE Coder which could create constant tables.
 
Add further services for Dashboard:
* write to Datapool

Support services for System Update
Support services for Device Configuration; a special TP frame type is used

## Requirements

* Linux
* Python3
* [SocketCAN](https://www.kernel.org/doc/Documentation/networking/can.txt) Implementation of the CAN protocol. This kernel module is part of Linux. 
* [python-can](https://python-can.readthedocs.io/en/master/installation.html) 

## Usage 

Install required python library.
I did so using a virtual python environment.
Install the python-can package via pip.
Configure server's openSYDE node-id to use in ecu_config.json
Configure CAN interface to use in ecu_config.json (verified only with virtual vcan0)

Set up CAN hardware interface. e.g.
```
# Create the virtual CAN interface.
ip link add dev vcan0 type vcan
# Bring the virtual CAN interface online.
ip link set up vcan0
```

## License 

MIT License

Copyright (c) 2020 Luis Alberto Benthin Sanguino
Copyright (c) 2023 Mark Miller

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.



