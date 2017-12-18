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


import argparse
from dd_burner import shell_exec, BlockDevice, ImageFile


parser = argparse.ArgumentParser(description='Write image file to device')
parser.add_argument('srcimg',
                    help='The image file to read data from')
parser.add_argument('dstdev',
                    help='The destination block device to write data into')
args = parser.parse_args()


# check source image and destination image
img = ImageFile(args.srcimg)
dev = BlockDevice(args.dstdev)

# zipped, gzipped or plain image
if img.gzipped:
    cmd = 'pv %s | gunzip | dd of=%s bs=4M' % (img.file_path, dev.device_path)
elif img.zipped:
    cmd = 'pv %s | funzip | dd of=%s bs=4M' % (img.file_path, dev.device_path)
else:
    cmd = 'pv %s | dd of=%s bs=4M' % (img.file_path, dev.device_path)

## Burn (with sudo)
print('From image: %s\nTo device:  %s\n' % (img.file_path, dev.device_path))
print('ARE YOU REALLY SURE? Type your sudo password to confirm.')
shell_exec('Burn', 'sudo -k sh -c "%s"' % cmd)
shell_exec('Sync', 'sync; sync;')

exit(0)