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
                self.util.print_out(3, "-", plugin_name, entity=entity)
                continue
            self.compare_properties(plugin_name, entity, data, s2)

    def compare_properties(self, plugin_name, entity, properties, s2):
        for k, v in properties.items():
            if "href" in v and self.util.is_href_excluded(v["href"]):
                continue
            if k not in s2[plugin_name][entity]:
                self.util.print_out(2, "-", plugin_name,
                                    entity=entity, file=k)
                continue
            if "href" in v:
                self.compare_file_content(plugin_name, entity, v["href"])

    def compare_file_content(self, plugin_name, entity, file_path):
        c1 = self.util.read_file(self.sospath1, file_path)
        c2 = self.util.read_file(self.sospath2, file_path)
        if c1 != c2:
            self.util.print_out(1, "%", plugin_name,
                                entity=entity, file=file_path[2:])
            if self.conf.args.diff:
                self.util.print_diff(self.util.exec_command(
                    f"diff {self.sospath1}/{file_path[2:]} \
                        {self.sospath2}/{file_path[2:]}"))

    def main(self):
        self.sos1 = self.util.load_sos_report(self.sospath1)
        self.sos2 = self.util.load_sos_report(self.sospath2)
        self.compare_plugins(self.sos1, self.sos2)
