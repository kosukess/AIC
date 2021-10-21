# Drawing tool by hand gestures
We implement a drawing tool by our hand gestures. We use TRT Pose Hand to detect our hand pose. <br>
The project includes
- drawing tool which is run in our PC 

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
`main.py` estimates your hand position and gesture class. 