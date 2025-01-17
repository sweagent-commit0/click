import typing as t
from contextlib import contextmanager
from gettext import gettext as _
from ._compat import term_len
from .parser import split_opt
FORCED_WIDTH: t.Optional[int] = None

def wrap_text(text: str, width: int=78, initial_indent: str='', subsequent_indent: str='', preserve_paragraphs: bool=False) -> str:
    """A helper function that intelligently wraps text.  By default, it
    assumes that it operates on a single paragraph of text but if the
    `preserve_paragraphs` parameter is provided it will intelligently
    handle paragraphs (defined by two empty lines).

    If paragraphs are handled, a paragraph can be prefixed with an empty
    line containing the ``\\b`` character (``\\x08``) to indicate that
    no rewrapping should happen in that block.

    :param text: the text that should be rewrapped.
    :param width: the maximum width for the text.
    :param initial_indent: the initial indent that should be placed on the
                           first line as a string.
    :param subsequent_indent: the indent string that should be placed on
                              each consecutive line.
    :param preserve_paragraphs: if this flag is set then the wrapping will
                                intelligently handle paragraphs.
    """
    pass

class HelpFormatter:
    """This class helps with formatting text-based help pages.  It's
    usually just needed for very special internal cases, but it's also
    exposed so that developers can write their own fancy outputs.

    At present, it always writes into memory.

    :param indent_increment: the additional increment for each level.
    :param width: the width for the text.  This defaults to the terminal
                  width clamped to a maximum of 78.
    """

    def __init__(self, indent_increment: int=2, width: t.Optional[int]=None, max_width: t.Optional[int]=None) -> None:
        import shutil
        self.indent_increment = indent_increment
        if max_width is None:
            max_width = 80
        if width is None:
            width = FORCED_WIDTH
            if width is None:
                width = max(min(shutil.get_terminal_size().columns, max_width) - 2, 50)
        self.width = width
        self.current_indent = 0
        self.buffer: t.List[str] = []

    def write(self, string: str) -> None:
        """Writes a unicode string into the internal buffer."""
        pass

    def indent(self) -> None:
        """Increases the indentation."""
        pass

    def dedent(self) -> None:
        """Decreases the indentation."""
        pass

    def write_usage(self, prog: str, args: str='', prefix: t.Optional[str]=None) -> None:
        """Writes a usage line into the buffer.

        :param prog: the program name.
        :param args: whitespace separated list of arguments.
        :param prefix: The prefix for the first line. Defaults to
            ``"Usage: "``.
        """
        pass

    def write_heading(self, heading: str) -> None:
        """Writes a heading into the buffer."""
        pass

    def write_paragraph(self) -> None:
        """Writes a paragraph into the buffer."""
        pass

    def write_text(self, text: str) -> None:
        """Writes re-indented text into the buffer.  This rewraps and
        preserves paragraphs.
        """
        pass

    def write_dl(self, rows: t.Sequence[t.Tuple[str, str]], col_max: int=30, col_spacing: int=2) -> None:
        """Writes a definition list into the buffer.  This is how options
        and commands are usually formatted.

        :param rows: a list of two item tuples for the terms and values.
        :param col_max: the maximum width of the first column.
        :param col_spacing: the number of spaces between the first and
                            second column.
        """
        pass

    @contextmanager
    def section(self, name: str) -> t.Iterator[None]:
        """Helpful context manager that writes a paragraph, a heading,
        and the indents.

        :param name: the section name that is written as heading.
        """
        pass

    @contextmanager
    def indentation(self) -> t.Iterator[None]:
        """A context manager that increases the indentation."""
        pass

    def getvalue(self) -> str:
        """Returns the buffer contents."""
        pass

def join_options(options: t.Sequence[str]) -> t.Tuple[str, bool]:
    """Given a list of option strings this joins them in the most appropriate
    way and returns them in the form ``(formatted_string,
    any_prefix_is_slash)`` where the second item in the tuple is a flag that
    indicates if any of the option prefixes was a slash.
    """
    pass