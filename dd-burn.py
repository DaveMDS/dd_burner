#!/usr/bin/env python
# encoding: utf-8

# Copyright (C) 2017-2018 Davide Andreoli <dave@gurumeditation.it>
#
# This file is part of dd-burner.
#
# dd-burner is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# dd-burner is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with dd-burner. If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import, print_function, division

import os
import sys
from dd_burner import shell_exec, BlockDevice, ImageFile


def usage():
    print('Usage:  dd-burn ImageFile DeviceToBurn')

def die(msg, ret=1, print_usage=True):
    print(msg)
    if print_usage:
        usage()
    exit(ret)


# check and get args
if len(sys.argv) != 3:
    die('Invalid arguments')
srcimg, dstdev = sys.argv[1:3]
print('From image: %s\nTo device:    %s\n' % (srcimg, dstdev))


# check source image
img = ImageFile(srcimg)


# check destination device
dev = BlockDevice(dstdev)


## Burn (zipped, gzipped or plain)
print('ARE YOU REALLY SURE? Type your sudo password to confirm.')
if srcimg.endswith(('.gz', '.GZ')):
    cmd = 'pv %s | gunzip | dd of=%s bs=4M' % (srcimg, dstdev)
elif srcimg.endswith(('.zip', '.ZIP')):
    cmd = 'pv %s | funzip | dd of=%s bs=4M' % (srcimg, dstdev)
else:
    cmd = 'pv %s | dd of=%s bs=4M' % (srcimg, dstdev)
shell_exec('Burn', 'sudo -k sh -c "%s"' % cmd)
shell_exec('Sync', 'sync; sync;')


exit(0)
