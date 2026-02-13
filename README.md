### PulpBrowser
Compare two sosreports and show the differences.
[sosreport](https://github.com/sosreport/sos).

#### `sosdiff` Usage
~~~
usage: sosdiff [-h] [-e PluginName] [-i PluginName] sospath1 sospath2

Compare two more sosreports and show the differences.

positional arguments:
  sospath1              Paths to first sosreport folder.
  sospath2              Path to second sosreport folder.

options:
  -h, --help            show this help message and exit
  -e PluginName, --exclude PluginName
                        Exclude this PluginName. Can be used multiple times.
  -i PluginName, --include PluginName
                        Include only this PluginName. Can be used multiple times.
~~~
