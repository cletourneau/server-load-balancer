from hamcrest.core.base_matcher import BaseMatcher

from virtual_machine import *

def a_vm(item):
  return isinstance(item, VirtualMachine)

class VmIsLoadedInServer(BaseMatcher):
  def __init__(self, expected_server):
    self.expected_server = expected_server

  def _matches(self, item):
    if not a_vm(item):
      return False
    return item in self.expected_server.vms

  def describe_to(self, description):
    description.append_text('a vm loaded in {id}'.format(id=self.expected_server.id))

  def describe_mismatch(self, item, mismatch_description):
    if not a_vm(item):
      mismatch_description.append_text('not a vm')
    else:
      mismatch_description.append_text('a vm not loaded in {id}'.format(self.expected_server.id))

def is_loaded_in(server):
  return VmIsLoadedInServer(server)
