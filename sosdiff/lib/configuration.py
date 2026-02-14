import argparse
import os


class Conf:

    def __init__(self):
        self.cwd = os.getcwd()
        self.sos = {}

        self.parser = argparse.ArgumentParser(
            description=("Compare two sosreports and show \
                         the differences.")
            )
        self.parser.add_argument(
            '-d',
            '--diff',
            help="Show `diff` if a file content don't match.",
            default=False,
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
            help="Output text without colors.",
            default=False,
            action='store_true'
            )
        self.parser.add_argument(
            'sospath1',
            help='Paths to first sosreport folder.',
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

        # self.args.output_path = (
        #     f"{self.args.output_path}/sosdiff"
        #     .replace('//', '/')
        #     )

    def valid_sosreport_path(self, path):
        p = path + "/sos_reports/sos.json"
        if os.path.exists(p):
            return path
        else:
            raise argparse.ArgumentTypeError(
                f"{p!r} doesn't exist.")
