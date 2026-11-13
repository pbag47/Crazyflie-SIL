# Software-in-the-Loop simulation of a Crazyflie UAV

This project builds on top of [Bitcraze's initiative](https://www.bitcraze.io/2021/04/successful-emulation/) which succeeded in passing the firmware self-test on an emulated hardware.
Starting from their Renode forks: 
- [Renode](https://github.com/bitcraze/renode)
- [Renode infrastructure](https://github.com/bitcraze/renode-infrastructure)

This project is an attempt to migrate existing code to a newer version of Renode (1.17.0).
Once this step is reached, the plan is to setup a UDP communication link in order to connect the emulated hardware to a physics/graphics engine such as Godot, Unity or Unreal Engine.

The ultimate goal is to fly a virtual Crazyflie using its actual firmware and flight controller.
