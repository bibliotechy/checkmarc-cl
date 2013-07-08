import json
from ops import OPS

class Check():
    def __init__(self, json_object='{}'):
        self.raw = json.loads(json_object)
        self.header = self.setHeader()
        self.field = self.setField()
        self.subfield = self.setSubfield()
        self.indicator = self.setIndicator()
        self.operator = self.setOperator()
        self.values   = self.setValues()


    def setHeader(self):
        value = self.raw.get('header', None)
        if not value:
            return ''
        if 1<= int(value) <= 17:
            return value
        else:
            raise ValueError('invalid MARC header')

    def setField(self):
        value = self.raw.get('field', None)
        if not value:
            return ''
        if 1 <= int(value) <= 999:
            return self._formatNumber(value)
        else:
            raise ValueError('Invalid MARC field')

    def setSubfield(self):
        value = self.raw.get('subfield', None)
        if not value:
            return ''
        return value.lower()

    def setIndicator(self):
        value = self.raw.get('indicator', None)
        if not value:
            return ''
        if len(value) > 1:
            if value.find('1') != -1:
                return '1'
            if value.find('2') != -1:
                return '2'
            else:
                raise ValueError("Invalid Indicator value")
        return value

    def setOperator(self):
        value = self.raw.get('operator', None)
        if not value:
            raise ValueError('Empty of missing Operator value: all checks must contain an operator')
        if value not in OPS:
            raise ValueError('Invalid Operator Value: not in listed of supported operators')
        return value

    def setValues(self):
        value = self.raw.get('values', None)
        if not value:
          return ''
        return value


    def _formatNumber(self, value):
        """
        MARC header and field numbers are always three digits. ie 001.
        Format a number provided to the MARC standard.
        """
        if len(value) == 1:
            value = "00" + value
        if len(value) == 2:
            value = "0" + value
        return value
