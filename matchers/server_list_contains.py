from hamcrest.core.base_matcher import BaseMatcher

def a_list(item):
  return isinstance(item, (tuple, list))

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
