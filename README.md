# ArtNet to CSV recorder

Quick Python script that records ArtNet data to CSV, made for personal usage.

This script will:

- Record all (or specific) DMX channels of a given ArtNet universe
- Write the results to a CSV file, with the DMX channels as the first row. Only the channels you selected are recorded.

Uses https://github.com/cpvalente/stupidArtnet

## Creating the virtual environment

`$ python3.8 -m venv artnet-recorder-venv`

## Starting the virtual environment

Python project built on Python 3.8

`$ source artnet-recorder-venv/bin/activate`

## Installing dependencies

Install inside the virtual environment:

```
$ python3.8 -m pip install --upgrade pip --no-cache-dir
$ pip install stupidartnet
$ pip install pyyaml
$ pip install sshkeyboard
$ pip install tabulate
```

## Modifying config.yaml

Copy the dist file and set your preferences:

`cp config.yaml.dist config.yaml`

## Starting the script

`$ python3.8 -m main`

Arguments:

```

--help  # Show this help message and exit
--artnet-universe 60  # Simplified ArtNet universe number that you want to record from, a value between 0 - 255. A value of 17 is equivalent to universe 1 of subnet 1
--dmx-channels='1,4-6,8-10,11'  # DMX channels you want to include in the recording
--recording-file-prefix='color'  # A prefix that will be added to the CSV recording filenames, useful to group recordings together
```

To start a recording, press `r` on the keyboard. To stop, press `r` again.
