import json

class Map():

  def __init__(self, json_object):
    self.raw = json.loads(json_object)
    self.mapping = self.get_map_units()
  
  def get_map_units(self):
    for unit in self.raw:
      yield self.evaluate_unit(unit)

  def evaluate_unit(self,unit):
    if type(unit) == int:
      return unit
    if type(unit) == dict:
      if unit['op'] == 'and':
        for check in unit['checks']:
          self.evaluate_unit(unit)
