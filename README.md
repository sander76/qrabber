# QGrabber

Scan QR codes using your webcam, pyzbar and wxpython. No usage of opencv

There are many tuturials available that explain how to scan a barcode with python.
Unfortunately they all make use of opencv for camera access. To me, the downside is the size of opencv.
So I tried to find an alternative. Which was hard.

I finallly settled with the solution provided by pygame. Usage of videocapture http://videocapture.sourceforge.net/

The available version on pypi does not work unfortunately. So I included the required wheels in this repo.
You can also find them online: 
Currently it is vendored inside this repo until a version will be available on pypi.

## Installation

In your project using this lib make sure you install the appropriate VideoCapture wheels.
Then:

`pip install qgrabber`

## Usage

See the demo.py file.
