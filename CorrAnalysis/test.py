#  Copyright (c) Jakob Erpf 2020
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
#  documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
#  and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of
#  the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
#  THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
#  TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
#
#  Written by Jakob Erpf <contact@jakoberpf.de>, 2020.

import unittest

import pandas

from func_correlation import associations, compute_correlations, kruskal_wallis_h


class MyTestCase(unittest.TestCase):
    def test_pearson(self):
        data = {'C01': [1, 2, 3, 4],
                'C02': [1, 2, 3, 4],
                'C03': [4, 3, 2, 1],
                'C04': [4, 3, 2, 1],
                'C05': [1, 2, 3, 4],
                'C06': [4, 3, 2, 1]
                }
        df = pandas.DataFrame(data, columns=['C01', 'C02', 'C03', 'C04', 'C05', 'C06'])
        corr, sign, columns, nominal_columns, inf_nan, single_value_columns = compute_correlations(df)
        print(corr)
        print(sign)
        # assert diagonal = 1.0
        self.assertEqual(corr.at['C01', 'C01'], 1.0)
        self.assertEqual(corr.at['C02', 'C02'], 1.0)
        self.assertEqual(corr.at['C03', 'C03'], 1.0)
        self.assertEqual(corr.at['C04', 'C04'], 1.0)
        # assert some others also = 1.0
        self.assertEqual(corr.at['C01', 'C02'], 1.0)
        self.assertEqual(corr.at['C02', 'C01'], 1.0)
        self.assertEqual(corr.at['C02', 'C03'], 1.0)
        self.assertEqual(corr.at['C03', 'C02'], 1.0)
        self.assertEqual(corr.at['C03', 'C04'], 1.0)
        self.assertEqual(corr.at['C03', 'C04'], 1.0)

    def test_kruskal_00(self):
        # test with 0.5 correlated
        x = [1, 2, 3, 4, 1, 2, 3, 4]
        y = [11, 11, 22, 22, 11, 11, 22, 22]

        corr, sign = kruskal_wallis_h(x, y)
        print('')
        print(corr)
        print(sign)

    def test_kruskal_01(self):
        # test with 1.0 correlated
        x = [1, 2, 3, 4, 1, 2, 3, 4]
        y = [11, 22, 33, 44, 11, 22, 33, 44]

        corr, sign = kruskal_wallis_h(x, y)
        print('')
        print(corr)
        print(sign)

    def test_kruskal_02(self):
        x = [1, 2, 3, 4, 1, 2, 3, 4]
        y = [11, 22, 33, 44, 55, 66, 77, 88]

        corr, sign = kruskal_wallis_h(x, y)
        print('')
        print(corr)
        print(sign)

    def test_kruskal_03(self):
        x = [1, 3, 5, 7, 9]
        y = [2, 4, 6, 8, 10]

        corr, sign = kruskal_wallis_h(x, y)
        print('')
        print(corr)
        print(sign)

    def test_kruskal_04(self):
        x = [1, 1, 2, 3, 3]
        y = [11, 11, 22, 33, 33]

        corr, sign = kruskal_wallis_h(x, y)
        print('')
        print(corr)
        print(sign)


if __name__ == '__main__':
    unittest.main()
