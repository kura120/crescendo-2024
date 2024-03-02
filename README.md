<h1> FRC Team 3340 - Crescendo 2024 </h1>
Welcome to the FRC Team 3340 programming repository. This contains our code for the 2024 FIRST Robotics Competition.

<h2>Quick Start</h2>
<h3>Installing Python</h3>

-   Download Python from the Python Software Foundation website: python.org
-   Recommended versions: 3.12, 3.11.7 (the version the Thinkpads have)

<h3>Installing other software</h3>
Python is now a supported language for the competition. Because of its simpler syntax, we will be using Python this year.

What else do I install?
- Install an IDE. [**Visual Studio Code**](code.visualstudio.com) is preferred as it is the primary IDE on our Thinkpads.
        - Installed VS Code? Make sure to download the Python extension.
- Install [GitHub Desktop](https://desktop.github.com/) or an alternative (like GitKraken). 
- (optional) Install [Git for your operating system](https://git-scm.com/) for native Git source control in Visual Studio Code.

<h3>Downloading required libraries<h3>

To download packages in Python, you use pip. You can choose to create a virtual environment to separate these packages from your install (see optional things).

- Firstly, clone this repository to your desktop using GitHub Desktop or the equivalent. 
- Next, open the project on VS Code.
- Then, create a new terminal (Terminal > New Terminal | Ctrl/Cmd + Shift + `)
- Finally, run the following command: `pip install -r requirements.txt`

<h1> Time to test your code. </h1>

There are two ways to send your code to the roboRIO:
    - via USB cable
    - via Wi-Fi or Ethernet (SSID: `3340_Quokka`)

<h6>Do keep in mind that the Python file must be named `robot.py`. It is best that you copy your code into the deploy folder to send your code over.</h6>

First-time setup for reference:
- ``robotpy init``
- ``robotpy sync`` syncs packages with roboRIO
- ``robotpy deploy`` sends robot.py file in directory to roboRIO

- ``robotpy installer download rev`` downloads rev library for roboRIO to PC
- ``robotpy installer download ctre`` downloads ctre library for roboRIO to PC
- ``robotpy installer install rev`` sends rev library for roboRIO to PC
- ``robotpy installer install ctre`` sends ctre library for roboRIO to PC

<h4> Optional Stuff </h4>

- Create a virtual environment using `python -m venv path/to/venv`
- Depending on how you installed Python, you may need to use the following:
    - `python3` - Default on Mac, on Windows if you installed from the Windows Store
    - `python`  - Windows only, does not work on Mac if I recall correctly. 
    - `py -3`   - Windows only (if you installed Python from python.org)
    - Append the version number if necessary to the end of python3 or py -3 (as in: python3.11, py -3.11)

[Detailed RobotPy Install Guide](https://docs.wpilib.org/en/stable/docs/zero-to-robot/step-2/python-setup.html)

<h2>Resources</h2>

[Tank drive xbox controller code + more](https://robotpy.readthedocs.io/en/stable/install/computer.html)

https://explore.partquest.com/blog/first-robotics-frc-motor-modeling-may-6-2016

https://github.com/Makerfabs/Maduino-CANbus-RS485/tree/main/CAN_Sender

<h1> Installing RobotPy Library </h1>
<h1> Deploying Code </h1>

1. Connect to 3340_Test3340 network
2. Make sure the file being deployed is named 'robot.py'

4. Open terminal
   
5. run `python3 robot.py deploy`
<h1> Rotating Motors - Code </h1>
<h2>Tasks</h2>
Lehansa - motor 1 sec forward

Ryan - encoder setup (tracking rotations)

Jasiere - motor 1 sec backwards

Angel - motor 1 sec back, 1 sec forward
<h1>  </h1>
