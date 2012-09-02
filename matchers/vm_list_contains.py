from hamcrest.core.base_matcher import BaseMatcher

from virtual_machine import *

def a_vm(item):
  return isinstance(item, VirtualMachine)

def a_list(item):
  return isinstance(item, (tuple, list))

class VmListContains(BaseMatcher):
  def __init__(self, expected_id, expected_size):
    self.expected_id = expected_id
    self.expected_size = expected_size

  def _matches(self, item):
    if not a_list(item):
      return False

    for vm in item:
      if vm.id == self.expected_id and vm.size == self.expected_size:
        return True

    return False

  def describe_to(self, description):
    description.append_text('a vm list containing a vm with id {id} and size of {size}'.format(
      id=self.expected_id,
      size=self.expected_size))

  def describe_mismatch(self, item, mismatch_description):
    if not a_list(item):
      mismatch_description.append_text('not a list')
    else:
      mismatch_description.append_text('a vm list not containing a vm with id {id} and size of {size}'.format(
        id=self.expected_id,
        size=self.expected_size))

def contains_a_vm_with(id, size):
  return VmListContains(id, size)
