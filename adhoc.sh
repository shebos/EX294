#!/bin/bash

ansible all -m yum_repository -a ' name=EX294_BASE description="EX294 base software" baseurl=http://materials.example.com/yum/repository/ gpgcheck=yes gpgkey=http://materials.example.com/yum/repository/RPM-GPG-KEY-example enabled=yes '

ansible all -m yum_repository -a ' name=EX294_STREAM description="EX294 stream software" baseurl=http://materials.example.com/yum/repository/ gpgcheck=yes gpgkey=http://materials.example.com/yum/repository/RPM-GPG-KEY-example enabled=yes '


