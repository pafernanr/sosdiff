magic_mod = False
try:
    import magic
    magic.detect_from_filename(__file__)
    magic_mod = True
except (ImportError, AttributeError):
    from textwrap import fill


class Util:

    def show_diff(self, level, name, text):
        if level > 1:
            color = Style.CYAN_BOLD
        else:
            color = Style.YELLOW_BOLD
        print(f"{color}[{name}]{Style.RESET} {text}")

    def read_file(self, sospath, file_path):
        abs_path = f"{sospath}/{file_path[2:]}"
        try:
            if self.file_is_binary(abs_path):
                with open(f"{abs_path}", "rb") as f:
                    return f.read()
            else:
                with open(f"{abs_path}", "r", encoding="utf-8") as f:
                    return f.read()
        except Exception as e:
            print(f"Error reading file {abs_path}\n{e}")

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

    def file_is_binary(self, fname):
        ''' Method from https://github.com/sosreport/sos/blob/main/sos/utilities.py '''  # noqa E501
        if magic_mod:
            try:
                _ftup = magic.detect_from_filename(fname)
                _mimes = ['text/', 'inode/']
                return (
                    _ftup.encoding == 'binary' and not
                    any(_ftup.mime_type.startswith(_mt) for _mt in _mimes)
                )
            except Exception:
                pass
        # if for some reason the above check fails or magic>=0.4.20 is not
        # present, fail over to checking the very first byte of the file
        # content
        with open(fname, 'tr', encoding='utf-8') as tfile:
            try:
                # when opened as above (tr), reading binary content will raise
                # an exception
                tfile.read(1)
                return False
            except UnicodeDecodeError:
                return True


class Style:
    GREEN = '\033[0;32m'
    GREEN_BOLD = '\033[0;32m\033[1m'
    RED = '\033[0;31m'
    RED_BOLD = '\033[0;31m'
    YELLOW = '\033[01;33m'
    YELLOW_BOLD = '\033[01;33m\033[1m'
    BLUE = '\033[0;34m'
    BLUE_BOLD = '\033[0;34m\033[1m'
    CYAN = '\033[01;36m'
    CYAN_BOLD = '\033[01;36m\033[1m'
    PURPLE = '\033[0;35m'
    PURPLE_BOLD = '\033[0;35m\033[1m'
    BOLD = '\033[1m'
    RESET = '\033[0m'
    NEW_LINE = '\n'
    RESET_NEW_LINE = '\033[0m\n'
