import sys
sys.path.insert(1, '.')

import pytest

import utils


# User x3m55y68 (unban_norris) is banned and has few runs
# - the result will be unchanged and processed quickly.
@pytest.mark.parametrize("func, result", [
    (utils.wrs, 3),
    (utils.runs, 11),
    (utils.gp, 1),
    (utils.cp, 3),
    (utils.pod, 7)
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
    assert utils.mods(userId) == result
