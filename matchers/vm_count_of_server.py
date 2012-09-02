from hamcrest.core.base_matcher import BaseMatcher

from server import *

def a_server(item):
  return isinstance(item, Server)

class VmCountOfServer(BaseMatcher):
  def __init__(self, expected_vm_count):
    self.expected_vm_count = expected_vm_count

  def _matches(self, item):
    if not a_server(item):
      return False
    return len(item.vms) == self.expected_vm_count

  def describe_to(self, description):
    description.append_text('a server with a vm count of {count}'.format(count=str(self.expected_vm_count)))

  def describe_mismatch(self, item, mismatch_description):
    if not a_server(item):
      mismatch_description.append_text('not a server')
    else:
      mismatch_description.append_text('a server with a vm count of {count}'.format(len(item.vms)))

def has_a_vm_count_of(expected_vm_count):
  return VmCountOfServer(expected_vm_count)
