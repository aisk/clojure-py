import unittest
from clojure.util.treadle.treadle import *
from clojure.util.treadle.treadle_exceptions import *


class ConstTests(unittest.TestCase):
    def setUp(self):
        pass
    def test_Const(self):
        self.assertEqual(Const(42).toFunc()(), 42)
        self.assertEqual(Const("foo").toFunc()(), "foo")
    def test_Arg(self):
        self.assertRaises(ExpressionNotAllowedException, Const, Const(3))


class ReturnTests(unittest.TestCase):
    def test_Arg(self):
        self.assertRaises(ExpressionRequiredException, Return, 42)

class IfTests(unittest.TestCase):
    def test_If(self):
        self.assertEqual(If(Const(True), Const(1), Const(0)).toFunc()(), 1)
        self.assertEqual(If(Const(False), Const(1), Const(0)).toFunc()(), 0)
        self.assertEqual(If(Const(False), Const(1)).toFunc()(), None)

    def test_Args(self):
        self.assertRaises(ExpressionRequiredException, If, Const(False), 1)


class AbstractExpression(unittest.TestCase):
    def test_Init(self):
        AExpression()
    def test_UnbalanedStack(self):
        class UnbalancedStackExpression(AExpression):
            def __init__(self):
                pass
            def size(self, current, max_seen):
                return 2, 2
            def emit(self, ctx):
                pass

        self.assertRaises(UnbalancedStackException, UnbalancedStackExpression().toCode)

class AddExpression(unittest.TestCase):
    def test_Add(self):
        self.assertEqual(Add(Const(1), Const(2)).toFunc()(), 3)

class SubExpression(unittest.TestCase):
    def test_Sub(self):
        self.assertEqual(Subtract(Const(3), Const(2)).toFunc()(), 1)

class DoExpresion(unittest.TestCase):
    def test_Do(self):
        self.assertEqual(Do(Const(0), Const(1), Const(2)).toFunc()(), 2)
        self.assertEqual(Do(Const(0), Const(1)).toFunc()(), 1)
        self.assertEqual(Do(Const(0)).toFunc()(), 0)
        self.assertEqual(Do().toFunc()(), None)

    def test_Args(self):
        self.assertRaises(ExpressionRequiredException, Do, Const(False), 1)

class FuncTests(unittest.TestCase):
    def test_Func(self):
        self.assertEqual(Func([], Const(1)).toFunc()(), 1)

class ArgTests(unittest.TestCase):
    def test_Argument(self):
        a = Argument("a")
        self.assertEqual(Func([a], a).toFunc()(42), 42)

class StoreLocalTests(unittest.TestCase):
    def test_StoreLocal(self):
        a = Local("a")
        self.assertEqual(StoreLocal(a, Const(42)).toFunc()(), 42)


compare_tests = {"Lesser": [[1, 2, True],
                            [2, 1, False],
                            [2, 2, False]],
                 "LesserOrEqual": [[1, 2, True],
                                   [2, 1, False],
                                   [2, 2, True]],
                 "Equal": [[1, 2, False],
                     [2, 1, False],
                     [2, 2, True]],
                 "NotEqual": [[1, 2, True],
                     [2, 1, True],
                     [2, 2, False]],
                 "Greater": [[1, 2, False],
                     [2, 1, True],
                     [2, 2, False]],
                 "GreaterOrEqual": [[1, 2, False],
                     [2, 1, True],
                     [2, 2, True]],
                 "In": [[1, [1, 2, 2], True],
                     [2, [1], False],
                     [2, [], False]],
                 "NotIn": [[1, [1, 2, 2], False],
                     [2, [1, 1], True],
                     [2, [], True]],
                 "Is": [[False, None, False],
                     [False, False, True],
                     [False, True, False]],
                 "IsNot": [[False, None, True],
                     [False, False, False],
                     [False, True, True]],
}

class TestCompareOps(unittest.TestCase):
    def test_Ops(self):
        for k in compare_tests:
            op = globals()[k]
            for t in compare_tests[k]:
                [v1, v2, result] = t
                self.assertEqual(op(Const(v1), Const(v2)).toFunc()(), result)

class CallTests(unittest.TestCase):
    def test_Call(self):
        fun = Func([], Const(42))
        self.assertEqual(Call(fun).toFunc()(), 42)

def pr(itm):
    print(itm)
    return itm

class RecurTests(unittest.TestCase):
    def test_Recur(self):
        accum = Argument("accum")

        f = Func([accum],
                If(NotEqual(accum, Const(10)),
                Recur(Add(accum, Const(1))),
                accum))

        #import dis
        #dis.dis(f.toFunc())
        c = f.toFunc()
        self.assertEqual(c(1), 10)

class TupleTests(unittest.TestCase):
    def test_Tuple(self):
        tp = Tuple(Const(1), Const(2)).toFunc()()

        self.assertEqual(tp, (1, 2))
        self.assertEqual(type(tp), tuple)

class ListTests(unittest.TestCase):
    def test_List(self):
        tp = List(Const(1), Const(2)).toFunc()()

        self.assertEqual(tp, [1, 2])
        self.assertEqual(type(tp), list)
        
        
class DictTests(unittest.TestCase):
    def test_Dict(self):
        tp = Dict(Const(1), Const(2), Const(3), Const(4)).toFunc()()

        self.assertEqual(tp, {1:2, 3: 4})
        self.assertEqual(type(tp), dict)        


class T(object):
    def foo(self):
        return 42

class AttrTests(unittest.TestCase):
    def test_List(self):
        num = Call(Attr(Const(T()), "foo")).toFunc()()

        self.assertEqual(num, 42)


class RaiseTests(unittest.TestCase):
    def test_Raise(self):
        r = Raise(Call(Const(Exception))).toFunc()

        self.assertRaises(Exception, r)

r = None

class FinallyTests(unittest.TestCase):
    def test_Finally(self):
        global r
        r = None
        def Foo():
            global r
            r = 2
            return r

        fb = Finally(Const(1), Call(Const(Foo))).toFunc()

        self.assertEquals(r, None)
        self.assertEquals(fb(), 1)
        self.assertEquals(r, 2)
