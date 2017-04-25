import unittest
from table_extractor.extractor import Extractor


class TestSimpleExtractor(unittest.TestCase):
    def setUp(self):
        html = """
        <table>
            <tr>
              <td>1</td>
              <td>2</td>
            </tr>
            <tr>
              <td>3</td>
              <td>4</td>
            </tr>
        </table>
        """
        self.extractor = Extractor(html)
        self.extractor.parse()

    def test_return_list(self):
        self.assertEqual(
            self.extractor.return_list(),
            [[u'1', u'2'], [u'3', u'4']]
        )

    def test_config_transformer(self):
        self.extractor.config(transformer=int)
        self.extractor.parse()
        self.assertEqual(
            self.extractor.return_list(),
            [[1, 2], [3, 4]]
        )


class TestComplexExtractor(unittest.TestCase):
    def setUp(self):
        html = """
        <table>
            <tr>
                <td rowspan=2>1</td>
                <td>2</td>
                <td>3</td>
            </tr>
            <tr>
                <td colspan=2>4</td>
            </tr>
            <tr>
                <td colspan=3>5</td>
            </tr>
        </table>
        """
        self.extractor = Extractor(html)
        self.extractor.parse()

    def test_return_list(self):
        self.assertEqual(
            self.extractor.return_list(),
            [[u'1', u'2', u'3'], [u'1', u'4', u'4'], [u'5', u'5', u'5']]
        )


class TestConflictedExtractor(unittest.TestCase):
    def setUp(self):
        html = """
        <table>
            <tr>
                <td rowspan=2>1</td>
                <td>2</td>
                <td rowspan=3>3</td>
            </tr>
            <tr>
                <td colspan=2>4</td>
            </tr>
            <tr>
                <td colspan=2>5</td>
            </tr>
        </table>
        """
        self.extractor = Extractor(html)
        self.extractor.parse()

    def test_return_list(self):
        self.assertEqual(
            self.extractor.return_list(),
            [[u'1', u'2', u'3'], [u'1', None, u'3', u'4', u'4'], [u'5', u'5', u'3']]
        )

    def test_config_overwrite(self):
        self.extractor.config(overwrite=True)
        self.extractor.parse()
        self.assertEqual(
            self.extractor.return_list(),
            [[u'1', u'2', u'3'], [u'1', u'4', u'4'], [u'5', u'5', u'3']]
        )


if __name__ == '__main__':
    unittest.main()