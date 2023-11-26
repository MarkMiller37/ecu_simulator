# openSYDE ECU Simulator

Based on a generic UDS implementation by Luis Alberto Benthin Sanguino.
See base GitHub repository for details.

Modified to mock an ECU using the UDS-based openSYDE protocol.

## What's implemented

Connect from openSYDE Dashboard basically works.

## Ideas for improvement

Datapool configuration is currently hard-coded in services.py.
This could be created from an openSYDE project by creating a derivative of
 the SYDE Coder which could create constant tables.
 
Add further services for Dashboard:
* write to Datapool
* read from Datapool event driven; not feasible with isotp kernel module as a special frame type is used

Support services for System Update
Support services for Device Configuration; not feasible with isotp kernel module as a special frame type is used

Maybe there is a way to inject the special openSYDE frame types into python isotp.
So the first step would be to switch to the Python SW implementation instead from the kernel module.
This would also remove the main Linux dependency.

## Requirements

* Linux
* Python3
* [SocketCAN](https://www.kernel.org/doc/Documentation/networking/can.txt) Implementation of the CAN protocol. This kernel module is part of Linux. 
* [ISO-TP kernel module](https://github.com/hartkopp/can-isotp) It is part of linux since kernel 5.10.
* [isotp](https://can-isotp.readthedocs.io/en/latest/) The `ecu-simulator` only uses [isotp.socket](https://can-isotp.readthedocs.io/en/latest/isotp/socket.html), which is a wrapper for the ISO-TP kernel module.
* [python-can](https://python-can.readthedocs.io/en/master/installation.html) The `ecu-simulator` uses this library to log CAN messages (see `loggers\logger_can.py`). **Note**: The bus type `socketcan` is used.  

## Usage 

Install required python libraries.
I did so using a virtual python environment.
Install the python-can and python-isotp packages via pip.
Configure CAN-IDs to use in ecu_config.json
Configure CAN interface to use in ecu_config.json (verified only with virtual vcan0)

Set up CAN hardware interface. e.g.
```
# Create the virtual CAN interface.
ip link add dev vcan0 type vcan
# Bring the virtual CAN interface online.
ip link set up vcan0
```


## Logging 

The `ecu-simulator` provides 3 levels of logging: CAN, ISO-TP, and application level. For example, when the VIN is requested, the following is logged:

* In `can_[Timestamp].log`

```
2020-02-05T13:08:39.188 can0 0x7df 0x0209020000000000
2020-02-05T13:08:39.192 can0 0x7e8 0x1014490200544553
2020-02-05T13:08:39.192 can0 0x7e0 0x3000050000000000
2020-02-05T13:08:39.198 can0 0x7e8 0x215456494e303132
2020-02-05T13:08:39.203 can0 0x7e8 0x2233343536373839
```
* In `isotp_[Timestamp].log`

```
2020-02-05T13:08:39.498 can0 0x7df 0x0902
2020-02-05T13:08:39.499 can0 0x7e8 0x4902005445535456494e30313233343536373839
```
* In `ecu_simulator.log`

```
2020-02-05T13:08:39.189 - ecu_simulator - INFO - Receiving on OBD address 0x7df from 0x7e8 Request: 0x0902
2020-02-05T13:08:39.190 - ecu_simulator - INFO - Requested OBD SID 0x9: Request vehicle information
2020-02-05T13:08:39.191 - ecu_simulator - INFO - Requested PID 0x2: Vehicle Identification Number(VIN)
2020-02-05T13:08:39.191 - ecu_simulator - INFO - Sending to 0x7e8 Response: 0x4902005445535456494e30313233343536373839
```

The log files have a max size of **1.5 M**. A new log file is generated when this size is reached.
 


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



