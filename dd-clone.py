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
    print('Usage:  dd-clone DeviceToRead ImageFile')

def die(msg, ret=1, print_usage=True):
    print(msg)
    if print_usage:
        usage()
    exit(ret)


# check and get args
if len(sys.argv) != 3:
    die('Invalid arguments')
srcdev, dstimg = sys.argv[1:3]
print('From device: %s\nTo image:    %s\n' % (srcdev, dstimg))


# check source device
dev = BlockDevice(srcdev)


# check destination image
if os.path.exists(dstimg):
    die('Destination already exists, not going to overwrite your file!',
         print_usage=False)

## Clone (gzipped or not)
if dstimg.endswith(('.gz', '.GZ')):
    cmd = 'sudo -k sh -c "pv %s | gzip | dd of=%s bs=4M"' % (srcdev, dstimg)
else:
    cmd = 'sudo -k sh -c "pv %s | dd of=%s bs=4M"' % (srcdev, dstimg)
shell_exec('Clone', cmd)


exit(0)
