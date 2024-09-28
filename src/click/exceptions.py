import typing as t
from gettext import gettext as _
from gettext import ngettext
from ._compat import get_text_stderr
from .utils import echo
from .utils import format_filename
if t.TYPE_CHECKING:
    from .core import Command
    from .core import Context
    from .core import Parameter

class ClickException(Exception):
    """An exception that Click can handle and show to the user."""
    exit_code = 1

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        return self.message

class UsageError(ClickException):
    """An internal exception that signals a usage error.  This typically
    aborts any further handling.

    :param message: the error message to display.
    :param ctx: optionally the context that caused this error.  Click will
                fill in the context automatically in some situations.
    """
    exit_code = 2

    def __init__(self, message: str, ctx: t.Optional['Context']=None) -> None:
        super().__init__(message)
        self.ctx = ctx
        self.cmd: t.Optional['Command'] = self.ctx.command if self.ctx else None

class BadParameter(UsageError):
    """An exception that formats out a standardized error message for a
    bad parameter.  This is useful when thrown from a callback or type as
    Click will attach contextual information to it (for instance, which
    parameter it is).

    .. versionadded:: 2.0

    :param param: the parameter object that caused this error.  This can
                  be left out, and Click will attach this info itself
                  if possible.
    :param param_hint: a string that shows up as parameter name.  This
                       can be used as alternative to `param` in cases
                       where custom validation should happen.  If it is
                       a string it's used as such, if it's a list then
                       each item is quoted and separated.
    """

    def __init__(self, message: str, ctx: t.Optional['Context']=None, param: t.Optional['Parameter']=None, param_hint: t.Optional[str]=None) -> None:
        super().__init__(message, ctx)
        self.param = param
        self.param_hint = param_hint

class MissingParameter(BadParameter):
    """Raised if click required an option or argument but it was not
    provided when invoking the script.

    .. versionadded:: 4.0

    :param param_type: a string that indicates the type of the parameter.
                       The default is to inherit the parameter type from
                       the given `param`.  Valid values are ``'parameter'``,
                       ``'option'`` or ``'argument'``.
    """

    def __init__(self, message: t.Optional[str]=None, ctx: t.Optional['Context']=None, param: t.Optional['Parameter']=None, param_hint: t.Optional[str]=None, param_type: t.Optional[str]=None) -> None:
        super().__init__(message or '', ctx, param, param_hint)
        self.param_type = param_type

    def __str__(self) -> str:
        if not self.message:
            param_name = self.param.name if self.param else None
            return _('Missing parameter: {param_name}').format(param_name=param_name)
        else:
            return self.message

class NoSuchOption(UsageError):
    """Raised if click attempted to handle an option that does not
    exist.

    .. versionadded:: 4.0
    """

    def __init__(self, option_name: str, message: t.Optional[str]=None, possibilities: t.Optional[t.Sequence[str]]=None, ctx: t.Optional['Context']=None) -> None:
        if message is None:
            message = _('No such option: {name}').format(name=option_name)
        super().__init__(message, ctx)
        self.option_name = option_name
        self.possibilities = possibilities

class BadOptionUsage(UsageError):
    """Raised if an option is generally supplied but the use of the option
    was incorrect.  This is for instance raised if the number of arguments
    for an option is not correct.

    .. versionadded:: 4.0

    :param option_name: the name of the option being used incorrectly.
    """

    def __init__(self, option_name: str, message: str, ctx: t.Optional['Context']=None) -> None:
        super().__init__(message, ctx)
        self.option_name = option_name

class BadArgumentUsage(UsageError):
    """Raised if an argument is generally supplied but the use of the argument
    was incorrect.  This is for instance raised if the number of values
    for an argument is not correct.

    .. versionadded:: 6.0
    """

class FileError(ClickException):
    """Raised if a file cannot be opened."""

    def __init__(self, filename: str, hint: t.Optional[str]=None) -> None:
        if hint is None:
            hint = _('unknown error')
        super().__init__(hint)
        self.ui_filename: str = format_filename(filename)
        self.filename = filename

class Abort(RuntimeError):
    """An internal signalling exception that signals Click to abort."""

class Exit(RuntimeError):
    """An exception that indicates that the application should exit with some
    status code.

    :param code: the status code to exit with.
    """
    __slots__ = ('exit_code',)

    def __init__(self, code: int=0) -> None:
        self.exit_code: int = code