import os
import sys

from sosdiff.lib.configuration import Conf
from sosdiff.lib.util import Util


class SosDiff:

    def __init__(self):
        self.conf = Conf()
        self.util = Util(self.conf)
        self.sospath1 = self.conf.args.sospath1
        self.sospath2 = self.conf.args.sospath2
        self.sos1 = False
        self.sos2 = False

    def compare_plugins(self, s1, s2):
        for plugin_name, plugin_data in s1.items():
            if plugin_name not in s2:
                self.util.print_out(4, "-", plugin_name)
                continue
            self.compare_entities(plugin_name, plugin_data, s2)

    def compare_entities(self, plugin_name, plugin_data, s2):
        for entity, data in plugin_data.items():
            if entity not in s2[plugin_name]:
                self.util.print_out(3, "--", plugin_name, entity=entity)
                continue
            self.compare_properties(plugin_name, entity, data, s2)

    def compare_properties(self, plugin_name, entity, properties, s2):
        for k, v in properties.items():
            if "href" in v and self.util.is_href_excluded(v["href"][2:]):
                continue
            if k not in s2[plugin_name][entity]:
                self.util.print_out(2, "---", plugin_name,
                                    entity=entity, propval=k)
                continue
            self.compare_values(plugin_name, entity, v)

    def compare_values(self, plugin_name, entity, v):
        if entity in ["copied_files", "created_files", "commands"]:
            self.compare_file_content(plugin_name, entity, v["href"][2:])
        else:
            print(f"ERROR: Unknown Entity {entity}")
            sys.exit(1)

    def compare_file_content(self, plugin_name, entity, file_path):
        path1 = f"{self.sospath1}/{file_path}"
        path2 = f"{self.sospath2}/{file_path}"
        if not os.path.exists(path1) or not os.path.exists(path2):
            self.util.print_out(1, "/", plugin_name,
                                entity=entity, propval=file_path)
        else:
            if self.util.read_file(path1) != self.util.read_file(path2):
                self.util.print_out(1, "/", plugin_name,
                                    entity=entity, propval=file_path)
                if self.conf.args.diff:
                    self.util.print_diff(self.util.exec_command(
                        f"diff {self.sospath1}/{file_path} \
                            {self.sospath2}/{file_path}"))

    def show_extra_plugins(self, s1, s2):
        extra = []
        for k in s2.keys():
            if k not in s1.keys():
                extra.append(k)
            else:
                self.show_extra_entities(s1[k], s2[k], k)
        for e in extra:
            self.util.print_out(3, "+", e)

    def show_extra_entities(self, e1, e2, plugin_name):
        extra = []
        for entity in e2.keys():
            if entity not in e1.keys():
                extra.append(entity)
            else:
                self.show_extra_properties(e1[entity], e2[entity],
                                           plugin_name, entity)
        for e in extra:
            self.util.print_out(3, "++", plugin_name, entity=e)

    def show_extra_properties(self, p1, p2, plugin_name, entity):
        extra = []
        for prop in p2.keys():
            if entity not in p1.keys():
                extra.append(prop)
        for e in extra:
            self.util.print_out(3, "+++", plugin_name,
                                entity=entity, propval=e,)

    def main(self):
        self.sos1 = self.util.load_sos_report(self.sospath1)
        self.sos2 = self.util.load_sos_report(self.sospath2)
        self.compare_plugins(self.sos1, self.sos2)
        self.show_extra_plugins(self.sos1, self.sos2)
