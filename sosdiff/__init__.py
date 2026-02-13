import re
import json

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

    def load_sos_report(self, sosreport_path):
        try:
            return self.get_plugins(json.loads(
                self.read_file(sosreport_path, "../sos_reports/sos.json")
                ))
        except Exception as e:
            print(e)
        return False

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
        sos = self.transform_plugin_list_to_dict(sos)
        out = dict(sos)
        for plugin_name, plugin_data in sos.items():
            if not self.is_plugin_included(plugin_name):
                out.pop(plugin_name)
                continue
            for name, data in plugin_data.items():
                if name in ["commands", "copied_files", "created_files"]:
                    out[plugin_name][name] = self.transform_list_to_dict(data)
                else:
                    print(f"ERR: {name}")
        return out

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

    def compare(self, s1, s2):
        for plugin_name, plugin_data in s1.items():
            if plugin_name not in s2:
                print(f"[MISS_P] {plugin_name}")
                continue
            for name, data in plugin_data.items():
                if name not in s2[plugin_name]:
                    print(f"[MISS_N] {plugin_name} :: {name}")
                    continue
                for k, v in data.items():
                    if "href" in v and self.is_href_excluded(v["href"]):
                        continue
                    else:
                        if k not in s2[plugin_name][name]:
                            print(f"[MISS_I] {plugin_name} :: {name} :: {k}")
                            continue
                        if "href" in v:
                            self.contentdiff(plugin_name, name, v["href"])

    def contentdiff(self, plugin_name, name, file_path):
        c1 = self.read_file(self.sospath1, file_path)
        c2 = self.read_file(self.sospath2, file_path)
        if c1 != c2:
            print(f"[DIFFER] {plugin_name} :: {name} :: {file_path[2:]}")

    def read_file(self, sospath, file_path):
        abs_path = f"{sospath}/{file_path[2:]}"
        try:
            if self.util.file_is_binary(abs_path):
                with open(f"{abs_path}", "rb") as f:
                    return f.read()
            else:
                with open(f"{abs_path}", "r", encoding="utf-8") as f:
                    return f.read()
        except Exception as e:
            print(f"Error reading file {abs_path}\n{e}")

    def main(self):
        self.sos1 = self.load_sos_report(self.sospath1)
        self.sos2 = self.load_sos_report(self.sospath2)
        self.compare(self.sos1, self.sos2)
