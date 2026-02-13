#!/usr/bin/python3
import os
import sys

sys.path.insert(0, "/usr/lib/tools/")

try:
    sys.path.insert(0, os.getcwd())
    from sosdiff import SosDiff
except KeyboardInterrupt as exc:
    raise SystemExit() from exc


def main():
    SosDiff().main()
    os._exit(0)


if __name__ == '__main__':
    main()
