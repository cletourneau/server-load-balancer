from hamcrest.core.base_matcher import BaseMatcher

from server import *
from virtual_machine import *

def a_server(item):
  return isinstance(item, Server)

def a_vm(item):
  return isinstance(item, VirtualMachine)

class CurrentLoadPercentageOfServer(BaseMatcher):
  def __init__(self, expected_load_percentage):
    self.expected_load_percentage = expected_load_percentage

  def _matches(self, item):
    if not a_server(item):
      return False
    return item.current_load_percentage == self.expected_load_percentage

  def describe_to(self, description):
    description.append_text('a server with current load percentage of %s' % self.expected_load_percentage)

  def describe_mismatch(self, item, mismatch_description):
    if not a_server(item):
      mismatch_description.append_text('not a server')
    else:
      mismatch_description.append_text('a server with current load percentage of %s' % item.current_load_percentage)

def has_current_load_percentage_of(expected_load_percentage):
  return CurrentLoadPercentageOfServer(expected_load_percentage)

class VmCountOfServer(BaseMatcher):
  def __init__(self, expected_vm_count):
    self.expected_vm_count = expected_vm_count

  def _matches(self, item):
    if not a_server(item):
      return False
    return len(item.vms) == self.expected_vm_count

  def describe_to(self, description):
    description.append_text('a server with a vm count of ') \
               .append_text(str(self.expected_vm_count))

  def describe_mismatch(self, item, mismatch_description):
    if not a_server(item):
      mismatch_description.append_text('not a server')
    else:
      mismatch_description.append_text('a server with a vm count of %s' % len(item.vms))

def has_a_vm_count_of(expected_vm_count):
  return VmCountOfServer(expected_vm_count)

class VmIsLoadedInServer(BaseMatcher):
  def __init__(self, expected_server):
    self.expected_server = expected_server

  def _matches(self, item):
    if not a_vm(item):
      return False
    return item in self.expected_server.vms

  def describe_to(self, description):
    description.append_text('a vm loaded in %s' % self.expected_server.id)

  def describe_mismatch(self, item, mismatch_description):
    if not a_vm(item):
      mismatch_description.append_text('not a vm')
    else:
      mismatch_description.append_text('a vm not loaded in %s' % self.expected_server.id)

def is_loaded_in(server):
  return VmIsLoadedInServer(server)
