# Textualog

Display, filter and search logging messages in the terminal.

This project is powered by [rich](https://github.com/Textualize/rich) and [textual](https://github.com/Textualize/textual).

Some of the ideas and code in this project are based on:

* [kaskade](https://github.com/sauljabin/kaskade)
* textual example code, e.g. code_viewer
* [cutelog](https://github.com/busimus/cutelog/)

## Log file formats

The current support is for a key-value type of log file. The log line shall have a fixed format, which is what I 
currently use in my main other projects. The following key=value pairs shall be there in the following order:

* `level=<logging level>`
* `ts=<'%Y-%m-%dT%H:%M:%S,%f'>`
* `process=<process name>`
* `process_id=<PID>`
* `caller=<calling function:lineno>`
* `msg=<logging message>`

In the future other formats can be supported by implementing a plugin class. Planned formats are the JSON format, ...
