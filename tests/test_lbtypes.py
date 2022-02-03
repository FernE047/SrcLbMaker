#!/usr/bin/env python3
import sys
sys.path.insert(1, '.')

import pytest

import lbtypes


# User x3m55y68 (unban_norris) is banned and has few runs
# - the result will be unchanged and processed quickly.
@pytest.mark.parametrize("func, result", [
    (lbtypes.wrs, 3),
    (lbtypes.runs, 11),
    (lbtypes.gp, 1),
    (lbtypes.cp, 3),
    (lbtypes.pod, 7)
])
def test_funcs(func, result):
    assert func("x3m55y68") == result


# User 18vr6lex (Toby_Butcher) is offline and has 1 game moderated
# - the result will be unchanged and processed quickly.
@pytest.mark.parametrize("userId, result", [
    ("x3m55y68", 0),
    ("18vr6lex", 1)
])
def test_mods(userId, result):
    assert lbtypes.mods(userId) == result
