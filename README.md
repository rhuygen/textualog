# Textualog

Display, filter and search logging messages in the terminal.

![screenshot](textualog.png)

This project is powered by [rich](https://github.com/Textualize/rich) and [textual](https://github.com/Textualize/textual).

Some of the ideas and code in this project are based on:

* [kaskade](https://github.com/sauljabin/kaskade)
* textual example code, e.g. code_viewer
* [cutelog](https://github.com/busimus/cutelog/)

## Installation

The easiest way to install the package is by running the `pip` command in the Python virtual environment of your project:
```
$ python -m pip install textualog
```

## Usage

The `textualog` app should have been installed in your environment, then run the following command:
```
$ textualog --log <path to the log file>
```
In the `examples` directory of this project, you can find an example log file to inspect and play with.

## Log file formats

The current support is for a key-value type of log file. The log line shall have a fixed format, which is what I 
currently use in my main other projects. The following key=value pairs shall be there in the given order:

* `level=<logging level>`
* `ts=<'%Y-%m-%dT%H:%M:%S,%f'>`
* `process=<process name>`
* `process_id=<PID>`
* `caller=<calling function:lineno>`
* `msg=<logging message>`

In the future other formats can be supported by implementing a plugin class. Planned formats are the JSON format, ...
