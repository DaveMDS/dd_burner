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
import glob
import subprocess
from stat import S_ISBLK, S_ISREG


if __name__ == '__main__':
    print("DONT RUN THIS SCRIPT DIRECTLY, IT MUST BE IMPORTED")
    exit(1)


def shell_exec(title, command):
    print('\n====  %s (%s)  ===============' % (title, command))
    return os.system(command)

def shell_output(args):
    try:
        out = subprocess.check_output(args)
        return out.decode('utf-8')
    except subprocess.CalledProcessError:
        return None


class BlockDevice(object):
    def __init__(self, device):
        """ Function doc """

        if not os.path.exists(device):
            raise RuntimeError('Cannot find device "%s"' % device)

        mode = os.stat(device).st_mode
        if not S_ISBLK(mode):
            raise RuntimeError('"%s" is not a valid block device' % device)

        self._device = device

    @property
    def device_path(self):
        return self._device
    
    @property
    def readable(self):
        return os.access(self._device, os.R_OK)

    @property
    def writeable(self):
        return os.access(self._device, os.W_OK)

    def show_info(self):
        print('Show device: %s' % self._device)
        shell_exec('Udev Info', 'udevadm info -n %s' % self._device)
        shell_exec('Partitions', 'sudo fdisk -l %s' % self._device)

    


class ImageFile(object):
    def __init__(self, fname):
        """ Function doc """

        if not os.path.exists(fname):
            raise RuntimeError('Cannot find image "%s"' % fname)

        mode = os.stat(fname).st_mode
        if not S_ISREG(mode):
            raise RuntimeError('"%s" is not a regular file' % fname)

        """
        not file -zb $imgfile | grep "DOS/MBR boot sector" >> /dev/null
            and echo "ERROR: Image file type not recognized"
            and return  # is a real image file? (maybe support more types here)
        """
        
        self._fname = fname

    def show_info(self):
        print('Show image: %s  (fdisk-l)' % self._fname)
        if self.fname.endswith(('gz', 'GZ', 'zip', 'ZIP')):
            raise NotImplemented('Cannot show a zipped image')
        else:
            shell_exec('Partitions', 'fdisk -l %s' % self._fname)

    @property
    def file_path(self):
        return self._fname
    
    @property
    def readable(self):
        return os.access(self._fname, os.R_OK)

    @property
    def writable(self):
        return os.access(self._fname, os.W_OK)

    @property
    def zipped(self):
        return self._fname.endswith(('.gz', '.GZ'))

    @property
    def gzipped(self):
        return self._fname.endswith(('.zip', '.ZIP'))

    def mount(self, mount_point):
        print('Mounting image:  %s' % self._fname)
        print('Mount point:     %s' % mount_point)

        if not os.path.isdir(mount_point) or os.listdir(mount_point):
            print('Mount point is not an empty directory')
            return False

        # TODO check mount_point is writable

        loop_device = shell_output(('losetup', '--find'))
        if loop_device is None:
            print('Cannot find an unused loop device')
            return False
        loop_device = loop_device.strip('\n')
        print('Loopback device: %s' % loop_device)

        ret = shell_exec('Loopback Setup',
                         'sudo losetup -P %s %s' % (loop_device, self._fname))

        for f in glob.glob(loop_device + 'p*'):
            part_name = f[len(loop_device):]
            pmount_point = os.path.join(mount_point, part_name)
            os.mkdir(pmount_point)
            shell_exec('Mounting %s' % part_name,
                       'sudo mount "%s" "%s"' % (f, pmount_point))

    def umount(self):
        pass

