"""
This module contains implementations for the termui module. To keep the
import time of Click down, some infrequently used functionality is
placed in this module and only imported as needed.
"""
import contextlib
import math
import os
import sys
import time
import typing as t
from gettext import gettext as _
from io import StringIO
from types import TracebackType
from ._compat import _default_text_stdout
from ._compat import CYGWIN
from ._compat import get_best_encoding
from ._compat import isatty
from ._compat import open_stream
from ._compat import strip_ansi
from ._compat import term_len
from ._compat import WIN
from .exceptions import ClickException
from .utils import echo
V = t.TypeVar('V')
if os.name == 'nt':
    BEFORE_BAR = '\r'
    AFTER_BAR = '\n'
else:
    BEFORE_BAR = '\r\x1b[?25l'
    AFTER_BAR = '\x1b[?25h\n'

class ProgressBar(t.Generic[V]):

    def __init__(self, iterable: t.Optional[t.Iterable[V]], length: t.Optional[int]=None, fill_char: str='#', empty_char: str=' ', bar_template: str='%(bar)s', info_sep: str='  ', show_eta: bool=True, show_percent: t.Optional[bool]=None, show_pos: bool=False, item_show_func: t.Optional[t.Callable[[t.Optional[V]], t.Optional[str]]]=None, label: t.Optional[str]=None, file: t.Optional[t.TextIO]=None, color: t.Optional[bool]=None, update_min_steps: int=1, width: int=30) -> None:
        self.fill_char = fill_char
        self.empty_char = empty_char
        self.bar_template = bar_template
        self.info_sep = info_sep
        self.show_eta = show_eta
        self.show_percent = show_percent
        self.show_pos = show_pos
        self.item_show_func = item_show_func
        self.label: str = label or ''
        if file is None:
            file = _default_text_stdout()
            if file is None:
                file = StringIO()
        self.file = file
        self.color = color
        self.update_min_steps = update_min_steps
        self._completed_intervals = 0
        self.width: int = width
        self.autowidth: bool = width == 0
        if length is None:
            from operator import length_hint
            length = length_hint(iterable, -1)
            if length == -1:
                length = None
        if iterable is None:
            if length is None:
                raise TypeError('iterable or length is required')
            iterable = t.cast(t.Iterable[V], range(length))
        self.iter: t.Iterable[V] = iter(iterable)
        self.length = length
        self.pos = 0
        self.avg: t.List[float] = []
        self.last_eta: float
        self.start: float
        self.start = self.last_eta = time.time()
        self.eta_known: bool = False
        self.finished: bool = False
        self.max_width: t.Optional[int] = None
        self.entered: bool = False
        self.current_item: t.Optional[V] = None
        self.is_hidden: bool = not isatty(self.file)
        self._last_line: t.Optional[str] = None

    def __enter__(self) -> 'ProgressBar[V]':
        self.entered = True
        self.render_progress()
        return self

    def __exit__(self, exc_type: t.Optional[t.Type[BaseException]], exc_value: t.Optional[BaseException], tb: t.Optional[TracebackType]) -> None:
        self.render_finish()

    def __iter__(self) -> t.Iterator[V]:
        if not self.entered:
            raise RuntimeError('You need to use progress bars in a with block.')
        self.render_progress()
        return self.generator()

    def __next__(self) -> V:
        return next(iter(self))

    def update(self, n_steps: int, current_item: t.Optional[V]=None) -> None:
        """Update the progress bar by advancing a specified number of
        steps, and optionally set the ``current_item`` for this new
        position.

        :param n_steps: Number of steps to advance.
        :param current_item: Optional item to set as ``current_item``
            for the updated position.

        .. versionchanged:: 8.0
            Added the ``current_item`` optional parameter.

        .. versionchanged:: 8.0
            Only render when the number of steps meets the
            ``update_min_steps`` threshold.
        """
        pass

    def generator(self) -> t.Iterator[V]:
        """Return a generator which yields the items added to the bar
        during construction, and updates the progress bar *after* the
        yielded block returns.
        """
        pass

def pager(generator: t.Iterable[str], color: t.Optional[bool]=None) -> None:
    """Decide what method to use for paging through text."""
    pass

def _pipepager(generator: t.Iterable[str], cmd: str, color: t.Optional[bool]) -> None:
    """Page through text by feeding it to another program.  Invoking a
    pager through this might support colors.
    """
    pass

def _tempfilepager(generator: t.Iterable[str], cmd: str, color: t.Optional[bool]) -> None:
    """Page through text by invoking a program on a temporary file."""
    pass

def _nullpager(stream: t.TextIO, generator: t.Iterable[str], color: t.Optional[bool]) -> None:
    """Simply print unformatted text.  This is the ultimate fallback."""
    pass

class Editor:

    def __init__(self, editor: t.Optional[str]=None, env: t.Optional[t.Mapping[str, str]]=None, require_save: bool=True, extension: str='.txt') -> None:
        self.editor = editor
        self.env = env
        self.require_save = require_save
        self.extension = extension
if WIN:
    import msvcrt
else:
    import tty
    import termios