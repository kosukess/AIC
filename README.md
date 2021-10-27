# Drawing tool by hand gestures
The project made by `Team A : KEIO University Project by KEIO University (KEIO AIC) x NVIDIA collaboration`<br>
We implemented a drawing tool by hand gestures. We use TRT Pose Hand to detect hand poses. <br>
The project includes
- drawing tool which runs in your PC connecting your Jetson nano

## Working Example
<center>
<table align="center" border="1">
<tr>
<td><img src="images/pen_app.gif" alt="Pen" width="300"></td>
<td><img src="images/eraser_app.gif" alt="Eraser" width="300"></td>
<td><img src="images/zoom_app.gif" alt="Zoom" width="300"></td>
</tr>
<tr>
<td>Pen and change size</td>
<td>Eraser</td>
<td>Zoom</td>
</tr>
</table>
</center>
<br>

## Gesture
<center>
<img src="images/gesture.png" alt="Gesture" width="900" border="1">
</center>
<br>

1. None
1. Draw or Erase
1. change mode (pen or eraser) and choose size
1. zoom in
1. zoom out

## Requirement
- jetpack 4.5.1 for 2GB ( https://developer.nvidia.com/jetpack-sdk-451-archive )
- Jetson nano 2GB model (can work with any Jetson devices but we did not check)
- USB cable (MicroB to typeA)
- Web camera
- your PC which can run exe file

## Getting started (Jetson)
### How to make docker image and container
At first, you need to connect your web camera to your Jetson. <br>
After connecting, run the below commands:
```bash
$ git clone https://github.com/kosukess/AIC.git
$ cd AIC
$ sh docker/build.sh
$ sh docker/run.sh
```

### Install required libraries to docker container
After you start the docker container first time, you need to install requirements. 
```bash
$ sh environment/trt_pose_hand_env.sh
```

### Start docker container second time or after
```bash
$ sh docker/open.sh
```

## Getting started (your PC)
Download `client_computer/show_output.exe`

## Usage
**At first, you have to connect your Jetson to your PC.**<br>
### Jetson
After you start the docker container which has required libraries, you can run:
```bash
cd project
python3 main.py
```
`main.py` estimates your hand position and gesture class, and send them to your PC.<br>
Jetson begins sending data to your PC about 3 minutes after you execute `python3 main.py`.

### your PC
Run `client_computer/show_output.exe`.<br>
After your PC receives data from Jetson, a whiteboard which you can draw shows on your PC.