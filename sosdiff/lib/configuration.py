import argparse
from configparser import ConfigParser
import os
import re


class Conf:

    def __init__(self):
        self.configparser = ConfigParser()
        self.default_config_dir = str(os.path.expanduser('~')) + "/.sosdiff"
        self.default_config_file = (
            f"{self.default_config_dir}/configuration.ini")
        self.text = False
        self.diff = False
        self.exclude_files = []
        self.include_files = []
        self.skip_plugins = []
        self.only_plugins = []

        self.parser = argparse.ArgumentParser(
            description=("Compare two sosreports and show \
                         the differences.")
            )
        self.parser.add_argument(
            '-c',
            '--configuration',
            metavar="<config_file>",
            help=f"Configuration file. Defaults to \
                `{self.default_config_file}`",
            default=self.default_config_file,
            type=self.valid_configuration_file
            )
        self.parser.add_argument(
            '-d',
            '--diff',
            help="Show `diff` when file content don't match.",
            action='store_true'
            )
        self.parser.add_argument(
            '-e',
            '--exclude-files',
            help="Exclude files matching this regexp. \
                Can be used multiple times.",
            default=[],
            action='append'
            )
        self.parser.add_argument(
            '-i',
            '--include-files',
            help="Include files matching this regexp. \
                Can be used multiple times.",
            default=[],
            action='append'
            )
        self.parser.add_argument(
            '-n',
            '--skip-plugins',
            metavar="SKIP_PLUGINS",
            help="Disable these plugins. Can be used multiple times.",
            default=[],
            action='append'
            )
        self.parser.add_argument(
            '-o',
            '--only-plugins',
            metavar="ONLY_PLUGINS",
            help="Enable these plugins only. Can be used multiple times.",
            default=[],
            action='append'
            )
        self.parser.add_argument(
            '-t',
            '--text',
            help="Print plain text without colors.",
            action='store_true'
            )
        self.parser.add_argument(
            'sospath1',
            help='Path to first sosreport folder.',
            type=self.valid_sosreport_path
            )
        self.parser.add_argument(
            'sospath2',
            help='Path to second sosreport folder.',
            type=self.valid_sosreport_path
            )
        self.args = self.parser.parse_args()

        # if (len(self.args.include) > 0
        #         and len(self.args.exclude) > 0):
        #     self.parser.error(
        #         "`--include` and `--exclude` are mutually exclusive.")

        self.set_configuration()

    def set_configuration(self):
        self.configparser.read(self.args.configuration)
        self.diff = self.get_config_boolean("diff")
        self.text = self.get_config_boolean("text")
        self.exclude_files = self.get_config_list("exclude_files")
        self.include_files = self.get_config_list("include_files")
        self.only_plugins = self.get_config_list("only_plugins")
        self.skip_plugins = self.get_config_list("skip_plugins")

    def get_config_boolean(self, name):
        if self.configparser.has_option('main', name):
            return self.configparser.getboolean('main', name)
        else:
            return self.args.__getattribute__(name)

    def get_config_list(self, name):
        if len(self.args.__getattribute__(name)) > 0:
            return self.args.__getattribute__(name)
        elif self.configparser.has_option('main', name):
            return self.option_to_list(self.configparser.get('main', name))
        else:
            return self.__getattribute__(name)

    def option_to_list(self, option):
        out = []
        try:
            out = re.findall(r"'(?<!\\)([^,]*?)'", option)
        except Exception as e:
            print(f"option_to_list error: {e}")
        return out

    def valid_configuration_file(self, path):
        if not os.path.exists(self.default_config_file):
            self.create_config_file()
        if os.path.exists(path):
            if os.path.isfile(path):
                return path
            else:
                raise argparse.ArgumentTypeError(
                    f"`{path!r}` is not valid.")
        else:
            raise argparse.ArgumentTypeError(
                f"`{path!r}` does not exist.")

    def create_config_file(self):
        if not os.path.exists(self.default_config_dir):
            os.mkdir(self.default_config_dir)
        if not os.path.exists(self.default_config_file):
            pwd = os.path.dirname(__file__)
            with open(f"{pwd}/../templates/configuration.ini", 'r',
                      encoding='utf-8') as f:
                with open(self.default_config_file, 'w',
                          encoding='utf-8') as c:
                    c.write(f.read())

    def valid_sosreport_path(self, path):
        if path[-1] == "/":
            path = path[:-1]
        p = path + "/sos_reports/sos.json"
        if os.path.exists(p):
            return path
        else:
            raise argparse.ArgumentTypeError(
                f"{p!r} doesn't exist.")
