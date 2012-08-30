from hamcrest.core.base_matcher import BaseMatcher

from server import *
from virtual_machine import *

def a_server(item):
  return isinstance(item, Server)

def a_vm(item):
  return isinstance(item, VirtualMachine)

def a_list(item):
  return isinstance(item, (tuple, list))

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

class ServerListContains(BaseMatcher):
  def __init__(self, expected_id, expected_slot_capacity):
    self.expected_id = expected_id
    self.expected_slot_capacity = expected_slot_capacity

  def _matches(self, item):
    if not a_list(item):
      return False

    for server in item:
      if server.id == self.expected_id and server.slot_capacity == self.expected_slot_capacity:
        return True

    return False

  def describe_to(self, description):
    description.append_text('a server list containing a server with id {id} and slot_capacity of {capacity}'.format(
      id=self.expected_id,
      capacity=self.expected_slot_capacity))

  def describe_mismatch(self, item, mismatch_description):
    if not a_list(item):
      mismatch_description.append_text('not a list')
    else:
      mismatch_description.append_text('a server list not containing a server with id {id} and slot_capacity of {capacity}'.format(
        id=self.expected_id,
        capacity=self.expected_slot_capacity))

def contains_a_server_with(id, slot_capacity):
  return ServerListContains(id, slot_capacity)

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
