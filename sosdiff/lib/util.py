import json
import re
import subprocess
import sys

magic_mod = False
try:
    import magic
    magic.detect_from_filename(__file__)
    magic_mod = True
except (ImportError, AttributeError):
    from textwrap import fill


class Util:

    def __init__(self, conf):
        self.conf = conf
        self.excluded_href = [
            r'^\.\./var/log/.*$',
            r'^\.\./sos_strings/.*var\.log.*\.tailed$']

    def print_out(self, severity, message, pluginname, entity=None, file=None):
        sep = " :: "
        color = ""
        reset = ""
        if not self.conf.args.text:
            sep = f"{Style.GREEN_BOLD}{sep}{Style.RESET}"
            color = self.set_out_color(severity)
            reset = Style.RESET

        out = f"{color}[{message}]{reset}"
        out += f"{sep}{pluginname}"
        if entity:
            out += f"{sep}{entity}"
        if file:
            out += f"{sep}{file}"
        print(out)

    def print_diff(self, diff):
        print(f"{diff}")

    def set_out_color(self, severity):
        if severity == 4:
            return Style.RED_BOLD
        if severity == 3:
            return Style.ORANGE_BOLD
        if severity == 2:
            return Style.YELLOW_BOLD
        if severity == 1:
            return Style.PURPLE_BOLD
        return Style.BLUE_BOLD

    def is_plugin_included(self, plugin_name):
        if len(self.conf.args.include) > 0:
            if plugin_name not in self.conf.args.include:
                return False
        if len(self.conf.args.exclude) > 0:
            if plugin_name in self.conf.args.exclude:
                return False
        return True

    def is_href_excluded(self, href):
        for exp in self.excluded_href:
            if re.match(exp, href):
                return True
        return False

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
                self.read_file(sosreport_path, "../sos_reports/sos.json")
                ))
        except Exception as e:
            print(e)
        return False

    def read_file(self, sospath, file_path):
        abs_path = f"{sospath}/{file_path[2:]}"
        try:
            if self.file_is_binary(abs_path):
                with open(f"{abs_path}", "rb") as f:
                    return f.read()
            else:
                with open(f"{abs_path}", "r", encoding="utf-8") as f:
                    return f.read()
        except Exception as e:
            print(f"Error reading file {abs_path}\n{e}")

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
        ''' Method from https://github.com/sosreport/sos/blob/main/sos/utilities.py '''  # noqa E501
        if magic_mod:
            try:
                _ftup = magic.detect_from_filename(fname)
                _mimes = ['text/', 'inode/']
                return (
                    _ftup.encoding == 'binary' and not
                    any(_ftup.mime_type.startswith(_mt) for _mt in _mimes)
                )
            except Exception:
                pass
        # if for some reason the above check fails or magic>=0.4.20 is not
        # present, fail over to checking the very first byte of the file
        # content
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
    GREEN = '\033[0;32m'
    GREEN_BOLD = '\033[0;32m\033[1m'
    RED = '\033[0;31m'
    RED_BOLD = '\033[0;31m'
    ORANGE = '\033[01;103m'
    ORANGE_BOLD = '\033[01;103m\033[1m'
    YELLOW = '\033[01;33m'
    YELLOW_BOLD = '\033[01;33m\033[1m'
    BLUE = '\033[0;34m'
    BLUE_BOLD = '\033[0;34m\033[1m'
    CYAN = '\033[01;36m'
    CYAN_BOLD = '\033[01;36m\033[1m'
    PURPLE = '\033[0;35m'
    PURPLE_BOLD = '\033[0;35m\033[1m'
    BOLD = '\033[1m'
    RESET = '\033[0m'
    NEW_LINE = '\n'
    RESET_NEW_LINE = '\033[0m\n'
