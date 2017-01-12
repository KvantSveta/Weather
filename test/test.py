import unittest2 as unittest


class TestGeneratorSpeed(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        from random import randint
        self.a = []
        self.b = []
        minus = chr(8722)
        for _ in range(10**7):
            i = randint(-100, 100)
            if i < 0:
                i = str(i)
                i = i.replace('-', minus)
            else:
                i = str(i)
            self.a.append(i)
            self.b.append(i)

    def test_1(self):
        import time

        s = time.time()
        [c.replace(chr(8722), '-') for c in self.a]
        print('test 1:', time.time() - s)

    def test_2(self):
        import time

        s = time.time()
        minus = chr(8722)
        [c.replace(minus, '-') for c in self.b]
        print('test 2:', time.time() - s)

    @classmethod
    def tearDownClass(self):
        del self.a
        del self.b
