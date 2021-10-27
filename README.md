# Drawing tool by hand gestures
The project made by `Team A : KEIO University Project by KEIO University (KEIO AIC) x NVIDIA collaboration`<br>
We implemented a drawing tool by our hand gestures. We use TRT Pose Hand to detect hand poses. <br>
The project includes
- drawing tool which runs in our PC connecting your Jetson nano

## Function of this drawing tool
<center> 
<img src="images/pen.gif"
alt="Pen" width="1000" border="1" />
<br>
<img src="images/eraser.gif"
alt="Eraser" width="1000" border="1" />
<br>
<img src="images/zoom.gif"
alt="Zoom" width="1000" border="1" />
</center>

## Getting started
### Requirement
- jetpack 4.5.1 for 2GB ( https://developer.nvidia.com/jetpack-sdk-451-archive )
- Jetson nano 2GB model (can work with any Jetson devices but we did not check)
- USB cable (MicroB to typeA)
- Web camera

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

## Usage
### Jetson
After you start the docker container with required libraries, you can run:
```bash
cd project
python3 main.py
```
`main.py` estimates your hand position and gesture class, and send them to our computer.<br>

### our computer
Run `dist/show_output.exe`.
