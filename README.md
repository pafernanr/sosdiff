### sosdiff
Compare two [sosreport](https://github.com/sosreport/sos) and show the differences.

To compare them `sosdiff` reads the file `sos_reports/sos.json` and lists the differences:
- [-] Plugin is missing on sosreport2. 
- [--] Entity is missing on sosreport2. 
- [---] File is missing on sosreport2.
- [/] File content is different. Optionally show `diff` command output.
- [+] Plugin is present on sosreport2 but it isn't on sosreport1.
- [++] Entity is present on sosreport2 but it isn't on sosreport1.
- [+++] File is present on sosreport2 but it isn't on sosreport1.

#### Dependencies
Required python libraries:
- pyyaml

#### Installation
There are multiple ways to to install `sosdiff`.

- Using `pip`.
  ~~~
  pip install sosdiff
  ~~~

- Using the prebuild packages at [Latest Release](https://github.com/pafernanr/sosdiff/releases/latest)

#### Usage
~~~
usage: sosdiff [-h] [-c <Path to configuration file>] [-d] [-e PluginName] [-i PluginName] [-t] sospath1 sospath2

Compare two sosreports and show the differences.

positional arguments:
  sospath1              Path to first sosreport folder.
  sospath2              Path to second sosreport folder.

options:
  -h, --help            show this help message and exit
  -c <Path to configuration file>, --configuration <Path to configuration file>
                        Configuration file. Defaults to `/home/pablofr/.sosdiff/configuration.yaml`
  -d, --diff            Show `diff` when file content don't match.
  -e PluginName, --exclude PluginName
                        Exclude this PluginName. Can be used multiple times.
  -i PluginName, --include PluginName
                        Include only this PluginName. Can be used multiple times.
  -t, --text            Print plain text without colors.
~~~
