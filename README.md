# PewDiePie-Doom-Countdown

Displays the difference between PewDiePie and T-Series' sub counts.

Simply run the python file using a python interpreter, or just double click the .pyw file. A window will open to display current numbers.

Currently only confirmed to be working with Windows and Linux - although I can't think why it wouldn't work with MacOS as well, but I have no way of testing it.

## Dependencies

* Python 3
* Tkinter

You can check if you have Tkinter by typing into a python interpreter:
`import tkinter`.
If there are no errors it is installed.

In linux, you may have to install it like this:
`sudo apt-get install python python3-tk`.

## Release

Just for fun, I've compiled a release of this program using PyInstaller. It only works with windows - although I've got it working on Linux through wine quite nicely.
You can build it yourself using [pyinstaller](https://www.pyinstaller.org/). I've made a build task for VS Code, but if you just want the command I use, it's: `pyinstaller pewdiepieDownfall.pyw -F -w`. This creates an executable for your system in a folder called `dist`.

## Known issues

* If you start without an internet connection, the program crashes.