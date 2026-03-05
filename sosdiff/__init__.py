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
            if "href" in v:
                if not self.util.is_file_included(v["href"][2:]):
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
        paths = self.util.list_files_in_href(self.sospath1, file_path)
        for p in paths:
            path1 = f"{self.sospath1}/{p}"
            path2 = f"{self.sospath2}/{p}"
            if not os.path.exists(path1) or not os.path.exists(path2):
                self.util.print_out(1, "/", plugin_name,
                                    entity=entity, propval=p)
            else:
                if self.util.read_file(path1) != self.util.read_file(path2):
                    self.util.print_out(1, "/", plugin_name,
                                        entity=entity, propval=p)
                    if self.conf.diff:
                        self.util.print_diff(self.util.exec_command(
                            f"diff {self.sospath1}/{p} \
                                {self.sospath2}/{p}"))

    def show_extra_plugins(self, s1, s2):
        extra = []
        for k in s2.keys():
            if k not in s1.keys():
                extra.append(k)
            else:
                self.show_extra_entities(k, s1[k], s2[k])
        for e in extra:
            self.util.print_out(3, "+", e)

    def show_extra_entities(self, plugin_name, entities1, entities2):
        extra = []
        for entity in entities2.keys():
            if entity not in entities1.keys():
                extra.append(entity)
            else:
                self.show_extra_properties(plugin_name, entity,
                                           entities1[entity],
                                           entities2[entity])
        for e in extra:
            self.util.print_out(3, "++", plugin_name, entity=e)

    def show_extra_properties(self, plugin_name, entity,
                              properties1, properties2):
        for prop in properties2.keys():
            if prop not in properties1.keys():
                if not self.util.is_file_included(prop):
                    continue
                self.util.print_out(3, "+++", plugin_name,
                                    entity=entity, propval=prop)

    def main(self):
        self.sos1 = self.util.load_sos_report(self.sospath1)
        self.sos2 = self.util.load_sos_report(self.sospath2)
        self.compare_plugins(self.sos1, self.sos2)
        self.show_extra_plugins(self.sos1, self.sos2)
