"""
Test evaluation of code that is evaluated straighforwardly when
``strict=False`` and produces a `NonLiteralAssignmentError` when
``strict=True``, with the value of ``delete_nonliteral`` never making a
difference
"""

from   literal_exec import literal_exec

def test_strict_nonliteral(strict_xfail, delete_nonliteral):
    assert literal_exec(
        "foo = 'bar'\nbar = range(42)\nbaz = 42\n",
        strict=strict_xfail,
        delete_nonliteral=delete_nonliteral,
    ) == {"foo": "bar", "baz": 42}

def test_list_assign_strict_nonliteral(strict_xfail, delete_nonliteral):
    assert literal_exec(
        'foo, bar, baz = "quux", range(42), "glarch"',
        strict=strict_xfail,
        delete_nonliteral=delete_nonliteral,
    ) == {"foo": "quux", "baz": "glarch"}

def test_faux_docstring_after_import(strict_xfail, delete_nonliteral):
    assert literal_exec('''
import sys
""" This is not a module docstring.  It is not stored in __doc__. """
''', strict=strict_xfail, delete_nonliteral=delete_nonliteral) == {}

def test_faux_unicode_literals_docstring(strict_xfail, delete_nonliteral):
    vals = literal_exec('''
""" This is a module docstring.  It is stored in __doc__. """
from .__future__ import unicode_literals
''', strict=strict_xfail, delete_nonliteral=delete_nonliteral)
    assert vals == {
        "__doc__": " This is a module docstring.  It is stored in __doc__. "
    }
    assert isinstance(vals["__doc__"], str)

def test_re_reassignment_nonliteral(strict_xfail, delete_nonliteral):
    assert literal_exec(
        "foo = 'value #1'\nfoo = range(42)\nfoo = 'value #2'\n",
        strict=strict_xfail,
        delete_nonliteral=delete_nonliteral,
    ) == {"foo": "value #2"}

def test_parse_print_function(strict_xfail, delete_nonliteral):
    assert literal_exec(
        "from __future__ import print_function\n"
        "def echo(*args):\n"
        "    print(*args, sep='')\n",
        strict=strict_xfail,
        delete_nonliteral=delete_nonliteral,
    ) == {}

def test_import(strict_xfail, delete_nonliteral):
    assert literal_exec(
        "foo = 'bar'\nimport baz\n",
        strict=strict_xfail,
        delete_nonliteral=delete_nonliteral,
    ) == {"foo": "bar"}

def test_reassign_import(strict_xfail, delete_nonliteral):
    assert literal_exec(
        "import foo\nfoo = 'bar'\n",
        strict=strict_xfail,
        delete_nonliteral=delete_nonliteral,
    ) == {"foo": "bar"}

def test_import_as_no_reassign(strict_xfail, delete_nonliteral):
    assert literal_exec(
        "foo = 'bar'\nimport foo as baz\n",
        strict=strict_xfail,
        delete_nonliteral=delete_nonliteral,
    ) == {"foo": "bar"}

def test_from_import_no_reassign(strict_xfail, delete_nonliteral):
    assert literal_exec(
        "foo = 'bar'\nfrom foo import quux\n",
        strict=strict_xfail,
        delete_nonliteral=delete_nonliteral,
    ) == {"foo": "bar"}

# function & class definitions
# raising/causing an error in the middle of the source?
# variables that are only ever assigned nonliteral expressions
