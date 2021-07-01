#!/bin/bash

userdel dog
rm -rf /home/dog

ARGS=$(echo "$@" | tr "\\\\()<>\`" " ")

groupadd dog
useradd -g dog $ARGS -g dog -G dog -m -d /home/dog dog
