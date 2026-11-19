# Software-in-the-Loop simulation of a Crazyflie UAV

This project builds on top of [Bitcraze's initiative](https://www.bitcraze.io/2021/04/successful-emulation/) which succeeded in passing the firmware self-test on an emulated hardware.
Starting from their Renode forks: 
- [Renode](https://github.com/bitcraze/renode/tree/crazyflie)
- [Renode infrastructure](https://github.com/bitcraze/renode-infrastructure/tree/crazyflie)

The plan is to setup a UDP communication link in order to connect the emulated hardware to a physics/graphics engine such as Godot, Unity or Unreal Engine.
The ultimate goal is to fly a virtual Crazyflie using its actual firmware and flight controller.


Project roadmap:
| Step | Validation | Status |
| --- | --- | --- |
| Renode: Migrate existing code to a newer version of Renode (1.17.0) | Pass the system self-test | ✅ |
| Renode: Provide synthetic data to sensors | Reach ready-to-fly state | ✅ |
| cflib: Create interface to send CRTP packets over UDP to nRF syslink-usart6 | Connect to the virtual Crazyflie with cflib-python | :small_orange_diamond: |
| Renode: Provide pilot input | Observe motor PWM commands | :small_orange_diamond: | 
| Renode: Setup UDP communication to provide data to sensors and retrieve motor PWM commands | Feed sensor data and observe motor PWM from another process |  |
| Physics Engine: Model the Crazyflie, its motors and its sensors |  |  |
| Physics Engine: Setup UDP communication | Fly the Crazyflie model using its emulated hardware in Renode | |

