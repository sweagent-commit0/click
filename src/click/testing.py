import contextlib
import io
import os
import shlex
import shutil
import sys
import tempfile
import typing as t
from types import TracebackType
from . import formatting
from . import termui
from . import utils
from ._compat import _find_binary_reader
if t.TYPE_CHECKING:
    from .core import BaseCommand

class EchoingStdin:

    def __init__(self, input: t.BinaryIO, output: t.BinaryIO) -> None:
        self._input = input
        self._output = output
        self._paused = False

    def __getattr__(self, x: str) -> t.Any:
        return getattr(self._input, x)

    def __iter__(self) -> t.Iterator[bytes]:
        return iter((self._echo(x) for x in self._input))

    def __repr__(self) -> str:
        return repr(self._input)

class _NamedTextIOWrapper(io.TextIOWrapper):

    def __init__(self, buffer: t.BinaryIO, name: str, mode: str, **kwargs: t.Any) -> None:
        super().__init__(buffer, **kwargs)
        self._name = name
        self._mode = mode

class Result:
    """Holds the captured result of an invoked CLI script."""

    def __init__(self, runner: 'CliRunner', stdout_bytes: bytes, stderr_bytes: t.Optional[bytes], return_value: t.Any, exit_code: int, exception: t.Optional[BaseException], exc_info: t.Optional[t.Tuple[t.Type[BaseException], BaseException, TracebackType]]=None):
        self.runner = runner
        self.stdout_bytes = stdout_bytes
        self.stderr_bytes = stderr_bytes
        self.return_value = return_value
        self.exit_code = exit_code
        self.exception = exception
        self.exc_info = exc_info

    @property
    def output(self) -> str:
        """The (standard) output as unicode string."""
        pass

    @property
    def stdout(self) -> str:
        """The standard output as unicode string."""
        pass

    @property
    def stderr(self) -> str:
        """The standard error as unicode string."""
        pass

    def __repr__(self) -> str:
        exc_str = repr(self.exception) if self.exception else 'okay'
        return f'<{type(self).__name__} {exc_str}>'

class CliRunner:
    """The CLI runner provides functionality to invoke a Click command line
    script for unittesting purposes in a isolated environment.  This only
    works in single-threaded systems without any concurrency as it changes the
    global interpreter state.

    :param charset: the character set for the input and output data.
    :param env: a dictionary with environment variables for overriding.
    :param echo_stdin: if this is set to `True`, then reading from stdin writes
                       to stdout.  This is useful for showing examples in
                       some circumstances.  Note that regular prompts
                       will automatically echo the input.
    :param mix_stderr: if this is set to `False`, then stdout and stderr are
                       preserved as independent streams.  This is useful for
                       Unix-philosophy apps that have predictable stdout and
                       noisy stderr, such that each may be measured
                       independently
    """

    def __init__(self, charset: str='utf-8', env: t.Optional[t.Mapping[str, t.Optional[str]]]=None, echo_stdin: bool=False, mix_stderr: bool=True) -> None:
        self.charset = charset
        self.env: t.Mapping[str, t.Optional[str]] = env or {}
        self.echo_stdin = echo_stdin
        self.mix_stderr = mix_stderr

    def get_default_prog_name(self, cli: 'BaseCommand') -> str:
        """Given a command object it will return the default program name
        for it.  The default is the `name` attribute or ``"root"`` if not
        set.
        """
        pass

    def make_env(self, overrides: t.Optional[t.Mapping[str, t.Optional[str]]]=None) -> t.Mapping[str, t.Optional[str]]:
        """Returns the environment overrides for invoking a script."""
        pass

    @contextlib.contextmanager
    def isolation(self, input: t.Optional[t.Union[str, bytes, t.IO[t.Any]]]=None, env: t.Optional[t.Mapping[str, t.Optional[str]]]=None, color: bool=False) -> t.Iterator[t.Tuple[io.BytesIO, t.Optional[io.BytesIO]]]:
        """A context manager that sets up the isolation for invoking of a
        command line tool.  This sets up stdin with the given input data
        and `os.environ` with the overrides from the given dictionary.
        This also rebinds some internals in Click to be mocked (like the
        prompt functionality).

        This is automatically done in the :meth:`invoke` method.

        :param input: the input stream to put into sys.stdin.
        :param env: the environment overrides as dictionary.
        :param color: whether the output should contain color codes. The
                      application can still override this explicitly.

        .. versionchanged:: 8.0
            ``stderr`` is opened with ``errors="backslashreplace"``
            instead of the default ``"strict"``.

        .. versionchanged:: 4.0
            Added the ``color`` parameter.
        """
        pass

    def invoke(self, cli: 'BaseCommand', args: t.Optional[t.Union[str, t.Sequence[str]]]=None, input: t.Optional[t.Union[str, bytes, t.IO[t.Any]]]=None, env: t.Optional[t.Mapping[str, t.Optional[str]]]=None, catch_exceptions: bool=True, color: bool=False, **extra: t.Any) -> Result:
        """Invokes a command in an isolated environment.  The arguments are
        forwarded directly to the command line script, the `extra` keyword
        arguments are passed to the :meth:`~clickpkg.Command.main` function of
        the command.

        This returns a :class:`Result` object.

        :param cli: the command to invoke
        :param args: the arguments to invoke. It may be given as an iterable
                     or a string. When given as string it will be interpreted
                     as a Unix shell command. More details at
                     :func:`shlex.split`.
        :param input: the input data for `sys.stdin`.
        :param env: the environment overrides.
        :param catch_exceptions: Whether to catch any other exceptions than
                                 ``SystemExit``.
        :param extra: the keyword arguments to pass to :meth:`main`.
        :param color: whether the output should contain color codes. The
                      application can still override this explicitly.

        .. versionchanged:: 8.0
            The result object has the ``return_value`` attribute with
            the value returned from the invoked command.

        .. versionchanged:: 4.0
            Added the ``color`` parameter.

        .. versionchanged:: 3.0
            Added the ``catch_exceptions`` parameter.

        .. versionchanged:: 3.0
            The result object has the ``exc_info`` attribute with the
            traceback if available.
        """
        pass

    @contextlib.contextmanager
    def isolated_filesystem(self, temp_dir: t.Optional[t.Union[str, 'os.PathLike[str]']]=None) -> t.Iterator[str]:
        """A context manager that creates a temporary directory and
        changes the current working directory to it. This isolates tests
        that affect the contents of the CWD to prevent them from
        interfering with each other.

        :param temp_dir: Create the temporary directory under this
            directory. If given, the created directory is not removed
            when exiting.

        .. versionchanged:: 8.0
            Added the ``temp_dir`` parameter.
        """
        pass