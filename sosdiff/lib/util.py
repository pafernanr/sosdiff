import datetime
import subprocess
import sys

magic_mod = False
try:
    import magic
    magic.detect_from_filename(__file__)
    magic_mod = True
except (ImportError, AttributeError):
    from textwrap import fill


class Util:

    def file_is_binary(self, fname):
        ''' Method from https://github.com/sosreport/sos/blob/main/sos/utilities.py '''
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
        # if for some reason the above check fails or magic>=0.4.20 is not present,
        # fail over to checking the very first byte of the file content
        with open(fname, 'tr', encoding='utf-8') as tfile:
            try:
                # when opened as above (tr), reading binary content will raise
                # an exception
                tfile.read(1)
                return False
            except UnicodeDecodeError:
                return True
