#!/usr/bin/env bash

docker build -f released -t webrtc_ros/released:latest .
docker build -f develop -t webrtc_ros/develop:latest .
docker build -f dev_awsc14 -t webrtc_ros/dev_awsc14:latest .

prior=$(pwd)
bn=$(basename "`pwd`")
if [ "$bn" = "dockerfiles" ]
    then
    cd ..
    echo "moving up to copy in files"
elif [ "bn" = "webrtc_ros" ]
    then
    echo "Already in correct context"
else
    echo "no clue where you are: $bn"
fi
docker build -f dockerfiles/full_build --build-arg ROS_VERSION=melodic -t webrtc_ros/develop-fullbuild:melodic .
docker build -f dockerfiles/full_build --build-arg ROS_VERSION=noetic -t webrtc_ros/develop-fullbuild:noetic .
cd $prior
