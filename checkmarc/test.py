import unittest
import check as c
import map as m 

class TestCheckClass(unittest.TestCase):

    def setUp(self):
        j0 = '{"empty" : "for testing unset value handling", "operator" : "equals"}'
        j1 = '{"leader": "11", "field": "", "subfield": "", "operator" : "equals", "value" : "N"}'
        j2 = '{"leader": "", "field": "1", "subfield" : "A", "operator" : "equals"}'
        j3 = '{"leader": "", "field": "245", "indicator" : "indicator1", "operator" : "equals", "values":"false"}'
        self.emptyCheck = c.Check(j0)
        self.check1 = c.Check(j1)
        self.check2 = c.Check(j2)
        self.check3 = c.Check(j3)

    def test_check_class_exists(self):
        self.assertIsInstance(self.check1, c.Check, "The Check class should exist")

    def test_check_unpack_json(self):
        self.assertEqual(self.check2.raw['field'],'1', 'Check should unpack json passed to it')

    def test_set_leader(self):
        self.assertEqual(self.emptyCheck.leader, '', 'Sets missing leader to empty string')
        self.assertEqual(self.check1.leader, '11',  "Check.leader should be set")
        self.assertEqual(self.check2.leader, '',  "Empty Header should remain empty")
        invalidLeader = '{"leader": "35", "field": "", "subfield": ""}'
        with self.assertRaises(ValueError):
            c.Check(invalidLeader)

    def test_set_field(self):
        self.assertEqual(self.emptyCheck.field, '', 'Sets missing field to empty string')
        self.assertEqual(self.check2.field, '001', "Check should format field as MARC expects")

    def test_set_subfield(self):
        self.assertEqual(self.emptyCheck.subfield, '', "Sets nonexistent subfield to empty string")
        self.assertEqual(self.check2.subfield, 'a', "Sets upper case subfield to lowercase")

    def test_set_indicator(self):
        self.assertEqual(self.emptyCheck.indicator, '', 'Sets missing indicator to empty string')
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

    def test_set_values(self):
        self.assertEqual(self.check3.values, "false", "Sets valid value correctly")



class TestMapClass(unittest.TestCase):

    def setUp(self):
        self.jsonMap = '[1,{"op":"or","checks":[{"op":"and","checks":[1,2]},{"op":"and","checks":[3,4]}]}]'
        self.map = m.Map(self.jsonMap)


    def test_init_unpack_json(self):
        self.assertEqual(self.map.raw[1]['op'],'or',"Json converted to python object")

    def test_get_map_list(self):
      self.assertEqual(self.map.mapping.next(), '1', self.map.mapping)


if __name__ == '__main__':
    unittest.main()
