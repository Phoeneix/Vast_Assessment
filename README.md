# Vast Take-Home Coding Challenge

- Objective:
You are tasked with developing a simulation for a lunar Helium-3 space mining operation. This
simulation will manage and track the efficiency of mining trucks and unload stations over a
continuous 72-hour operation.

- How to execute in Github:
On the github action's tab, use either the "Manual Test executor" or the "Execute built-in tests" actions.
User needs to provide number of mining trucks and mining stations for "Manual Test executor" action.
(Optional) User can also modify the operation length, that may differ from the default ones.
(Optional) User can also modify the log level to get details of the inner workings in case of debug.

- How to execute the manual test on local computer:
Input arguments:
	- n = number of mining trucks
    - m = number of mining stations
    - o = operation length
    - l = level of log (INFO, DEBUG), default is INFO

>```python start.py -n 50 -m 5 -o 4320 -l DEBUG```

- How to execute the built in tests on local computer:

>```python run_tests.py```