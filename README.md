### sosdiff
Compare two [sosreport](https://github.com/sosreport/sos) by parsing `sos_reports/sos.json` to show the differences on collected files and optionally the diff for those files.

- The configuration file is `~/.sosdiff/configuration.ini`.
- Alternative configuration can be used. E.g: `sosdiff -c ~/.sosdiff/troubleshoot_netwoking.ini`.
- Some paths are exluded to avoid "Too many levels of symbolic links" errors. `[r'^/sys/class/.*$', r'^/sys/devices/.*$',]`
  - Refer to [excluded_href](https://github.com/pafernanr/sosdiff/blob/main/sosdiff/lib/util.py)

### Output

| Output | Description | 
|---|---|
| ***[-] | Plugin is missing on sosreport2. | 
| ***[--]  | Entity is missing on sosreport2. |
| ***[---] | File is missing on sosreport2. |
| ***[/] | File content is different. Optionally show `diff` command output. |
| ***[+] | Plugin is present on sosreport2 and missing on sosreport1. |
| ***[++] | Entity is present on sosreport2 and missing on sosreport1. |
| ***[+++] | File is present on sosreport2 and missing on sosreport1. |
   
#### Installation

- Install using `pip` or the prebuild packages at [Latest Release](https://github.com/pafernanr/sosdiff/releases/latest)
  ~~~
  pip install sosdiff
  ~~~

#### Usage
~~~
usage: sosdiff [-h] [-c <config_file>] [-d] [-f] [-e EXCLUDE_FILES] [-i INCLUDE_FILES] [-n SKIP_PLUGINS] [-o ONLY_PLUGINS] [-s] [-t]
               sospath1 sospath2

Compare two sosreport by parsing `sos_reports/sos.json` and show the differences on collected files.

positional arguments:
  sospath1              Path to first sosreport folder.
  sospath2              Path to second sosreport folder.

options:
  -h, --help            show this help message and exit
  -c <config_file>, --configuration <config_file>
                        Configuration file. Defaults to `~/.sosdiff/configuration.ini`
  -d, --diff            Show `diff` when files content don't match.
  -f, --no-diff         Hide `diff` when files content don't match.
  -e EXCLUDE_FILES, --exclude-files EXCLUDE_FILES
                        Exclude files matching this regexp. Can be used multiple times.
  -i INCLUDE_FILES, --include-files INCLUDE_FILES
                        Include files matching this regexp. Can be used multiple times.
  -n SKIP_PLUGINS, --skip-plugins SKIP_PLUGINS
                        Disable these plugins. Can be used multiple times.
  -o ONLY_PLUGINS, --only-plugins ONLY_PLUGINS
                        Enable these plugins only. Can be used multiple times.
  -s, --no-text         Show colors in the output.
  -t, --text            Hide colors in the outuput.
~~~
