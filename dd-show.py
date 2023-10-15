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

import sys
from dd_burner import shell_exec, BlockDevice, ImageFile


def usage():
    print('Usage:  dd-show ImageFile OR dd-show Device')


def die(msg, ret=1):
    print(msg)
    usage()
    exit(ret)


# no params mode (fdisk -l)
if len(sys.argv) == 1:
    print('Show all available block devices')
    shell_exec('Devices', 'sudo fdisk -l')


# single param mode: image file or block device
elif len(sys.argv) == 2:
    arg = sys.argv[1]

    try:
        dev = BlockDevice(arg)
        dev.show_info()
        exit(0)
    except RuntimeError:
        pass

    try:
        image = ImageFile(arg)
        image.show_info()
        exit(0)
    except RuntimeError:
        pass

    die('ERROR: param must be a regular file or a block device')

# wrong params
else:
    die('ERROR: Wrong params')

exit(0)
