# PIPayload
Code for the SARP 2022 Pacific Impulse Launch

clone onto rpi

```pip3 install requirements.txt```

```python3 main.py```

## What Needs To Be Tested/Configured
```Camera.py``` -- figure out if we need threading, make sure it records to file

```Servo.py```  -- tweak/test pwm duty cycle calculations, add threading for the time it takes to move the servo


## What Needs To Be Implemented
Include ```Servo.py``` into ```main.py``` so the envelope servo can be actuated

Create and implement GPS code

Add mechanism to activate envelope weather it be based on speed or time (or both)

Parachute deployment?
