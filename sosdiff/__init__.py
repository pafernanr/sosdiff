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

    def compare(self, s1, s2):
        for plugin_name, plugin_data in s1.items():
            if plugin_name not in s2:
                self.util.print_out(severity=4, message="plugin missing",
                                    pluginname=plugin_name)
                continue
            for name, data in plugin_data.items():
                if name not in s2[plugin_name]:
                    self.util.print_out(severity=3, message="name missing",
                                        pluginname=plugin_name, name=name)
                    continue
                for k, v in data.items():
                    if "href" in v and self.util.is_href_excluded(v["href"]):
                        continue
                    else:
                        if k not in s2[plugin_name][name]:
                            self.util.print_out(
                                severity=2, message="file missing",
                                pluginname=plugin_name, name=name,
                                file=k)
                            continue
                        if "href" in v:
                            self.content_diff(plugin_name, name, v["href"])

    def content_diff(self, plugin_name, name, file_path):
        c1 = self.util.read_file(self.sospath1, file_path)
        c2 = self.util.read_file(self.sospath2, file_path)
        if c1 != c2:
            self.util.print_out(severity=1, message="file content",
                                pluginname=plugin_name, name=name,
                                file=file_path[2:])
            if self.conf.args.diff:
                self.util.print_diff(self.util.exec_command(
                    f"diff {self.sospath1}/{file_path[2:]} \
                        {self.sospath2}/{file_path[2:]}"))

    def main(self):
        self.sos1 = self.util.load_sos_report(self.sospath1)
        self.sos2 = self.util.load_sos_report(self.sospath2)
        self.compare(self.sos1, self.sos2)
