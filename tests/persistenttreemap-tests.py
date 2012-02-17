import unittest

from py.clojure.lang.persistenttreemap import PersistentTreeMap


class PresistentTreeMapTests(unittest.TestCase):
    def testAssoc(self):
        m = PersistentTreeMap()
        m2 = m.assoc('a', 1)
        self.assertTrue(m2.containsKey('a'))

    def testWithout(self):
        m = PersistentTreeMap()
        m2 = m.assoc('a', 1)
        m3 = m2.without('a')
        self.assertFalse(m3.containsKey('a'))

    def testSeq(self):
        self.assertEqual(PersistentTreeMap().seq(), None)

        m = PersistentTreeMap()
        m1 = m.assoc('a', 1)
        self.assertEqual(m1.seq().first().key, 'a')