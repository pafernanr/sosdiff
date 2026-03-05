import json
import os
import re
import subprocess
import sys


class Util:

    def __init__(self, conf):
        self.conf = conf
        # exluded to avoid "Too many levels of symbolic links" errors.
        self.excluded_href = [
            r'^/sys/class/.*$',
            r'^/sys/devices/.*$',]

    def print_out(self, severity, message, pluginname,
                  entity=None, propval=None):
        sep = " :: "
        color = ""
        reset = ""
        if not self.conf.text:
            sep = f"{Style.GREEN}{sep}{Style.RESET}"
            color = self.set_out_color(severity)
            reset = Style.RESET

        out = f"{color}[{message}]{reset}"
        out += f"{sep}{pluginname}"
        if entity:
            out += f"{sep}{entity}"
        if propval:
            out += f"{sep}{propval}"
        print(out)

    def print_diff(self, diff):
        # diff = '    ' + diff.replace('\n', '\n    ')
        if self.conf.text:
            print(f"{diff}")
        else:
            print(f"{Style.GRAY}{diff}{Style.RESET}")

    def set_out_color(self, severity):
        if severity == 4:
            return Style.RED
        if severity == 3:
            return Style.ORANGE
        if severity == 2:
            return Style.YELLOW
        if severity == 1:
            return Style.PURPLE
        return Style.BLUE

    def is_plugin_included(self, plugin_name):
        if len(self.conf.only_plugins) > 0:
            if plugin_name not in self.conf.only_plugins:
                return False
        if len(self.conf.skip_plugins) > 0:
            if plugin_name in self.conf.skip_plugins:
                return False
        return True

    def is_href_excluded(self, href):
        for exp in self.excluded_href + self.conf.exclude_files:
            if re.match(exp, href):
                return True
        return False

    def list_files_in_href(self, basedir, relpath):
        files = []
        abspath = f"{basedir}{relpath}"
        if os.path.isdir(abspath):
            with os.scandir(abspath) as entries:
                for entry in entries:
                    relpath = entry.path.replace(basedir, '', 1)
                    if entry.is_file():
                        print(f"_file_{relpath}")
                        files.append(relpath)
                    elif entry.is_dir():
                        print(f"_dir_{relpath}")
                        files += self.list_files_in_href(basedir, relpath)
        else:
            files.append(relpath)
        return files

    def get_plugins(self, sos):
        sos = self.transform_plugin_list_to_dict(sos)
        out = dict(sos)
        for plugin_name, plugin_data in sos.items():
            if not self.is_plugin_included(plugin_name):
                out.pop(plugin_name)
                continue
            for name, data in plugin_data.items():
                if name in ["commands", "copied_files", "created_files"]:
                    out[plugin_name][name] = self.transform_list_to_dict(
                        data)
                else:
                    print(f"ERR: {name}")
        return out

    def load_sos_report(self, sosreport_path):
        try:
            return self.get_plugins(json.loads(
                self.read_file(f"{sosreport_path}/sos_reports/sos.json")
                ))
        except Exception as e:
            print(e)
        return False

    def read_file(self, file_path):
        try:
            if self.file_is_binary(file_path):
                with open(f"{file_path}", "rb") as f:
                    return f.read()
            else:
                with open(f"{file_path}", "r", encoding="utf-8") as f:
                    return f.read()
        except Exception as e:
            print(f"Error reading file {file_path}\n{e}")

    def transform_plugin_list_to_dict(self, items):
        out = {}
        for i in items:
            out[i[0]] = i[1]
        return out

    def transform_list_to_dict(self, items):
        out = {}
        for c in items:
            name = c['name']
            c.pop('name')
            out[name] = c
        return out

    def file_is_binary(self, fname):
        with open(fname, 'tr', encoding='utf-8') as tfile:
            try:
                # when opened as above (tr), reading binary content will raise
                # an exception
                tfile.read(1)
                return False
            except UnicodeDecodeError:
                return True

    def exec_command(self, cmd):
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        stdout = str(stdout.decode("utf-8"))
        stderr = str(stderr.decode("utf-8"))
        if stderr != "":
            print(cmd + "\n" + stderr)
            sys.exit(1)
        return stdout


class Style:
    BLUE = '\033[0;34m'
    CYAN = '\033[01;36m'
    GRAY = '\033[0;90m'
    GREEN = '\033[0;32m'
    ORANGE = '\033[01;33m'
    RED = '\033[0;31m'
    PURPLE = '\033[0;35m'
    YELLOW = '\033[01;93m'

    BOLD = '\033[1m'
    NEW_LINE = '\n'
    RESET = '\033[0m'
    RESET_NEW_LINE = '\033[0m\n'
