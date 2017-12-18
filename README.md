# dd_burner
A simple dd frontend to easily clone, burn, mount and manage image files

Installation
------------
For the moment just copy (or link) the five python files somewhere in your path,
a proper setup.py script will come soon.

dd-mount
--------
```
usage: dd-mount.py [-h] imagefile mountpoint

Mount an image file to folder

positional arguments:
  imagefile   Image file to mount, can contain multiple partitions
  mountpoint  An empty folder to mount all the image partitions to
```

dd-clone
--------
```
usage: dd-clone.py [-h] srcdev dstimg

Save a device into an image file

positional arguments:
  srcdev      The device to read from
  dstimg      The name of the image file to be created
```

dd-burn
-------
```
usage: dd-burn.py [-h] srcimg dstdev

Write image file to device

positional arguments:
  srcimg      The image file to read data from
  dstdev      The destination block device to write data into

```

dd-show
-------
TODO
