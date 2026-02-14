import json
import re

from sosdiff.lib.configuration import Conf
from sosdiff.lib.util import Util


class SosDiff:

    def __init__(self):
        self.conf = Conf()
        self.util = Util()
        self.sospath1 = self.conf.args.sospath1
        self.sospath2 = self.conf.args.sospath2
        self.included_plugins = self.conf.args.include
        self.excluded_plugins = self.conf.args.exclude
        self.sos1 = False
        self.sos2 = False
        self.excluded_href = [
            r'^\.\./var/log/.*$',
            r'^\.\./sos_strings/.*var\.log.*\.tailed$']

    def is_plugin_included(self, plugin_name):
        if len(self.included_plugins) > 0:
            if plugin_name not in self.included_plugins:
                return False
        if len(self.excluded_plugins) > 0:
            if plugin_name in self.excluded_plugins:
                return False
        return True

    def is_href_excluded(self, href):
        for exp in self.excluded_href:
            if re.match(exp, href):
                return True
        return False

    def get_plugins(self, sos):
        sos = self.util.transform_plugin_list_to_dict(sos)
        out = dict(sos)
        for plugin_name, plugin_data in sos.items():
            if not self.is_plugin_included(plugin_name):
                out.pop(plugin_name)
                continue
            for name, data in plugin_data.items():
                if name in ["commands", "copied_files", "created_files"]:
                    out[plugin_name][name] = self.util.transform_list_to_dict(
                        data)
                else:
                    print(f"ERR: {name}")
        return out

    def load_sos_report(self, sosreport_path):
        try:
            return self.get_plugins(json.loads(
                self.util.read_file(sosreport_path, "../sos_reports/sos.json")
                ))
        except Exception as e:
            print(e)
        return False

    def compare(self, s1, s2):
        for plugin_name, plugin_data in s1.items():
            if plugin_name not in s2:
                self.util.show_diff(1, "plugin missing", plugin_name)
                continue
            for name, data in plugin_data.items():
                if name not in s2[plugin_name]:
                    self.util.show_diff(1, "name missing",
                                        f"{plugin_name} :: {name}")
                    continue
                for k, v in data.items():
                    if "href" in v and self.is_href_excluded(v["href"]):
                        continue
                    else:
                        if k not in s2[plugin_name][name]:
                            self.util.show_diff(1, "file missing",
                                           f"{plugin_name} :: {name} :: {k}")
                            continue
                        if "href" in v:
                            self.contentdiff(plugin_name, name, v["href"])

    def contentdiff(self, plugin_name, name, file_path):
        c1 = self.util.read_file(self.sospath1, file_path)
        c2 = self.util.read_file(self.sospath2, file_path)
        if c1 != c2:
            self.util.show_diff(2, "file content",
                                f"{plugin_name} :: {name} :: {file_path[2:]}")

    def main(self):
        self.sos1 = self.load_sos_report(self.sospath1)
        self.sos2 = self.load_sos_report(self.sospath2)
        self.compare(self.sos1, self.sos2)
