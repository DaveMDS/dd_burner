#!/usr/bin/env python
# encoding: utf-8

# Copyright (C) 2017-2024 Davide Andreoli <dave@gurumeditation.it>
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
import argparse
from dd_burner import shell_exec, BlockDevice, ExecutionTimer


parser = argparse.ArgumentParser(description='Save a device into an image file')
parser.add_argument('srcdev',
                    help='The device to read from')
parser.add_argument('dstimg',
                    help='The name of the image file to be created')
args = parser.parse_args()


# check source device
dev = BlockDevice(args.srcdev)

# check destination image
if os.path.exists(args.dstimg):
    print('Destination already exists, not going to overwrite your file!')
    exit(1)

# gzipped or not command
if args.dstimg.endswith(('.gz', '.GZ')):
    cmd = 'pv %s | gzip | dd of=%s bs=4M' % (args.srcdev, args.dstimg)
else:
    cmd = 'pv %s | dd of=%s bs=4M' % (args.srcdev, args.dstimg)

# Clone (with sudo)
print('From device: %s\nTo image:    %s\n' % (args.srcdev, args.dstimg))
t = ExecutionTimer()
shell_exec('Clone', 'sudo -k sh -c "%s"' % cmd)
print('Operation completed in %s (include password prompt)' % t.readable)

exit(0)
