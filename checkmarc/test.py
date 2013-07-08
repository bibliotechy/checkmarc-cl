import unittest
import pymarc
import check as c

class TestCheckClass(unittest.TestCase):

    def setUp(self):
        j0 = '{"empty" : "for testing unset value handling", "operator" : "equals"}'
        j1 = '{"header": "11", "field": "", "subfield": "", "operator" : "equals"}'
        j2 = '{"header": "", "field": "1", "subfield" : "A", "operator" : "equals"}'
        j3 = '{"header": "", "field": "245", "indicator" : "indicator1", "operator" : "equals"}'
        self.check0 = c.Check(j0)
        self.check1 = c.Check(j1)
        self.check2 = c.Check(j2)
        self.check3 = c.Check(j3)

    def test_check_class_exists(self):
        self.assertIsInstance(self.check1, c.Check, "The Check class should exist")

    def test_check_unpack_json(self):
        self.assertEqual(self.check2.raw['field'],'1', 'Check should unpack json passed to it')

    def test_set_header(self):
        self.assertEqual(self.check0.header, '', 'Sets missing header to empty string')
        self.assertEqual(self.check1.header, '11',  "Check.header should be set")
        self.assertEqual(self.check2.header, '',  "Empty Header should remain empty")
        invalidHeader = '{"header": "22", "field": "", "subfield": ""}'
        with self.assertRaises(ValueError):
            c.Check(invalidHeader)

    def test_set_field(self):
        self.assertEqual(self.check0.field, '', 'Sets missing field to empty string')
        self.assertEqual(self.check2.field, '001', "Check should format field as MARC expects")

    def test_set_subfield(self):
        self.assertEqual(self.check0.subfield, '', "Sets nonexistent subfield to empty string")
        self.assertEqual(self.check2.subfield, 'a', "Sets upper case subfield to lowercase")

    def test_set_indicator(self):
        self.assertEqual(self.check0.indicator, '', 'Sets missing indicator to empty string')
        self.assertEqual(self.check3.indicator, "1", "Sets indicator value to either 1 or 2")

    def test_set_operator(self):
        missingOperator = '{}'
        with self.assertRaises(ValueError):
            c.Check(missingOperator)
        emptyOperator   = '{"operator" : ""}'
        with self.assertRaises(ValueError):
            c.Check(emptyOperator)
        invalidOperator = '{"operator" : "isBooleanFor"}'
        with self.assertRaises(ValueError):
            c.Check(invalidOperator)
        self.assertEqual(self.check1.operator,'equals','Sets valid operator correctly')
if __name__ == '__main__':
    unittest.main()