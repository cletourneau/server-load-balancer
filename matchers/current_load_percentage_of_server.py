from hamcrest.core.base_matcher import BaseMatcher

from server import *

def a_server(item):
  return isinstance(item, Server)

class CurrentLoadPercentageOfServer(BaseMatcher):
  def __init__(self, expected_load_percentage):
    self.expected_load_percentage = expected_load_percentage

  def _matches(self, item):
    if not a_server(item):
      return False
    return item.current_load_percentage == self.expected_load_percentage

  def describe_to(self, description):
    description.append_text('a server with current load percentage of {load}'.format(load=self.expected_load_percentage))

  def describe_mismatch(self, item, mismatch_description):
    if not a_server(item):
      mismatch_description.append_text('not a server')
    else:
      mismatch_description.append_text('a server with current load percentage of {load}'.format(load=item.current_load_percentage))

def has_current_load_percentage_of(expected_load_percentage):
  return CurrentLoadPercentageOfServer(expected_load_percentage)
