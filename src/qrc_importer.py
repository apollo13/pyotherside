#
# PyOtherSide: Asynchronous Python 3 Bindings for Qt 5 and Qt 6
# Copyright (c) 2014, Thomas Perl <m@thp.io>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
# OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.
#

import sys
from importlib import abc
from importlib.util import spec_from_loader

import pyotherside


class PyOtherSideQtRCLoader(abc.Loader):
    def __init__(self, filepath):
        self.filepath = filepath

    def create_module(self, spec):
        return

    def exec_module(self, module):
        data = pyotherside.qrc_get_file_contents(self.filepath[len('qrc:') :])
        code = compile(data, self.filepath, 'exec')
        exec(code, module.__dict__)


class PyOtherSideQtRCImporter(abc.MetaPathFinder, abc.SourceLoader):
    def find_spec(self, fullname, path, target=None):
        if path is None:
            fname = self.get_filename(fullname)
            if fname:
                return spec_from_loader(fullname, PyOtherSideQtRCLoader(fname))
        return

    def find_module(self, fullname, path):
        if path is None or all(x.startswith('qrc:') for x in path):
            if self.get_filename(fullname):
                return self

    def get_filename(self, fullname):
        basename = fullname.replace('.', '/')

        for import_path in sys.path:
            if not import_path.startswith('qrc:'):
                continue

            for candidate in ('{}/{}.py', '{}/{}/__init__.py'):
                filename = candidate.format(import_path, basename)
                if pyotherside.qrc_is_file(filename[len('qrc:'):]):
                    return filename

    def get_data(self, path):
        return pyotherside.qrc_get_file_contents(path[len('qrc:'):])

    def module_repr(self, m):
        return "<module '{}' from '{}'>".format(m.__name__, m.__file__)

sys.meta_path.append(PyOtherSideQtRCImporter())
