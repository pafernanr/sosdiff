import argparse
import os
import yaml


class Conf:

    def __init__(self):
        self.default_config_dir = str(os.path.expanduser('~')) + "/.sosdiff"
        self.default_config_file = (
            f"{self.default_config_dir}/configuration.yaml")
        self.text = False
        self.diff = False
        self.exclude_files = []

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
            '--exclude',
            metavar="PluginName",
            help="Exclude this PluginName. Can be used multiple times.",
            default=[],
            action='append'
            )
        self.parser.add_argument(
            '-i',
            '--include',
            metavar="PluginName",
            help="Include only this PluginName. Can be used multiple times.",
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

        if (len(self.args.include) > 0
                and len(self.args.exclude) > 0):
            self.parser.error(
                "`--include` and `--exclude` are mutually exclusive.")

        self.read_configuration_file()

    def read_configuration_file(self):
        with open(self.args.configuration, 'r', encoding='utf-8') as stream:
            try:
                conf = yaml.safe_load(stream)
                self.diff = self.set_config(conf['main']['diff'],
                                            self.args.diff)
                self.text = self.set_config(conf['main']['text'],
                                            self.args.text)
                if conf['exclude_files']:
                    self.exclude_files = conf['exclude_files']
            except Exception as e:
                print(e)

    def set_config(self, conf, arg):
        if arg:
            return arg
        return conf

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
            with open(f"{pwd}/../templates/configuration.yaml", 'r',
                      encoding='utf-8') as f:
                with open(self.default_config_file, 'w',
                          encoding='utf-8') as c:
                    c.write(f.read())

    def get_custom_exclude_files(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read().split("\n")

    def valid_sosreport_path(self, path):
        if path[-1] == "/":
            path = path[:-1]
        p = path + "/sos_reports/sos.json"
        if os.path.exists(p):
            return path
        else:
            raise argparse.ArgumentTypeError(
                f"{p!r} doesn't exist.")
