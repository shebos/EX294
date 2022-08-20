#!/bin/bash

ansible all -m yum_repository -a ' name=EX294_BASE description="EX294 Base software" baseurl=http://materials.example.com/yum/repository/ gpgcheck=yes enabled=yes ' -b



ansible all -m yum_repository -a ' name=EX294_STREAM description="EX294 Stream software" baseurl=http://materials.example.com/yum/repository/ gpgcheck=yes enabled=yes ' -b


ansible all -m rpm_key -a ' key=http://materials.example.com/yum/repository/RPM-GPG-KEY-example state=present ' -b

